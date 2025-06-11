import logging
import os
import pickle as pkl
from dataclasses import dataclass

import numpy as np
from miv.core.pipeline import Pipeline
from miv.statistics.criticality import AvalancheAnalysis, AvalancheDetection
from scipy.optimize import curve_fit


@dataclass
class Config:
    """Configuration for criticality analysis."""

    class_id: str
    pipeline_run_path: str
    spike_data_path: str
    data_tag: str

    # Avalanche detection configurations
    bin_size: float = 0.002  # in seconds
    threshold_percentage: float = 2.0
    time_difference: float = 0.002
    allow_multiple_spike_per_bin: bool = False
    minimum_bins_in_avalanche: int = 10

    # Burst detection configurations
    min_interburst_interval_bound: float = 0.1  # sec
    pre_burst_extension: float = 0.0
    post_burst_extension: float = 0.0


class RunCriticalityAnalysis:
    def __call__(self, config: Config):
        with open(config.spike_data_path, "rb") as f:
            spikestamps = pkl.load(f)

        # Avalanche detection
        avalanche_detection = AvalancheDetection(
            bin_size=config.bin_size,
            threshold_percentage=config.threshold_percentage,
            time_difference=config.time_difference,
            allow_multiple_spike_per_bin=config.allow_multiple_spike_per_bin,
            minimum_bins_in_avalanche=config.minimum_bins_in_avalanche,
            min_interburst_interval_bound=config.min_interburst_interval_bound,
            pre_burst_extension=config.pre_burst_extension,
            post_burst_extension=config.post_burst_extension,
            tag=f"avalanche_detection_{config.data_tag}",
        )
        avalanche_analysis = AvalancheAnalysis(tag=f"avalanche_analysis_{config.data_tag}")
        spikestamps >> avalanche_detection >> avalanche_analysis
        # avalanche_detection.cacher.policy = "OFF"
        avalanche_analysis.cacher.policy = "OFF"  # This needs to be off

        result_path = os.path.join(config.pipeline_run_path, "dash_criticality", config.class_id)
        Pipeline(avalanche_analysis).run(result_path, skip_plot=True, verbose=True)

        self.output = {
            "avalanche_detection": avalanche_detection.output(),
            "avalanche_analysis": avalanche_analysis.output(),
        }

    def power_law_fitting(self):
        durations, size, branching_ratio, _, _ = self.output["avalanche_analysis"]

        def power(x, a, c):
            return c * (x**a)

        def neg_power(x, a, c):
            return c * (x ** (-a))

        col = []

        nbins = 50

        hist, bins = np.histogram(size, bins=nbins)
        logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
        # axes[0].hist(size, bins=logbins, histtype="step", label="data")
        # axes[0].set_xscale("log")
        # axes[0].set_yscale("log")
        # axes[0].set_xlabel("size (# channels)")
        # axes[0].set_ylabel("Event Frequency")
        hist, bins = np.histogram(size, bins=logbins)
        if hist[hist > 1].size > 0:
            try:
                popt, pcov = curve_fit(neg_power, bins[:-1][hist > 1], hist[hist > 1])
                tau = popt[0]
                size_fit = neg_power(logbins, *popt)
            except RuntimeError:
                tau = 0
                size_fit = np.ones_like(logbins)
                logging.warning("Power-fit failed. No fitted line will be plotted.")
            except TypeError:
                tau = 0
                size_fit = np.ones_like(logbins)
                logging.warning("Power-fit failed. No fitted line will be plotted.")
        else:
            size_fit = np.ones_like(logbins)
            tau = 0.0
        col.append([bins[:-1][hist > 1], hist[hist > 1], logbins, size_fit, tau])

        hist, bins = np.histogram(durations, bins=nbins)
        logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
        # axes[1].hist(durations, bins=logbins, histtype="step", label="data")
        # axes[1].set_xscale("log")
        # axes[1].set_yscale("log")
        # axes[1].set_xlabel("duration (s)")
        # axes[1].set_ylabel("Event Frequency")
        hist, bins = np.histogram(durations, bins=logbins)
        alpha = 0
        duration_fit = np.ones_like(logbins)
        try:
            if (hist > 1).sum() > 0:
                popt, pcov = curve_fit(neg_power, bins[:-1][hist > 1], hist[hist > 1])
                alpha = popt[0]
                # axes[1].plot(
                #    logbins, neg_power(logbins, *popt), label=f"fit {alpha=:.2f}"
                # )
                duration_fit = neg_power(logbins, *popt)
        except (RuntimeError, TypeError) as e:
            logging.warning(f"Power-fit failed: {e!s}. No fitted line will be plotted.")
        col.append([bins[:-1][hist > 1], hist[hist > 1], logbins, duration_fit, alpha])

        values = []
        avearges = []
        for value in np.unique(durations):
            values.append(value)
            avearges.append(np.mean(size[durations == value]))
        # axes[2].set_xscale("log")
        # axes[2].set_yscale("log")
        # axes[2].set_xlabel("duration (s)")
        # axes[2].set_ylabel("Average size (# channels)")
        svz = 0
        try:
            popt, pcov = curve_fit(power, values, avearges)
            svz = popt[0]
            # axes[2].plot(
            #    logbins, power(logbins, *popt), label=f"fit 1/svz={popt[0]:.2f}"
            # )
            average_fit = power(logbins, *popt)
        except RuntimeError:
            average_fit = np.ones_like(logbins)
            logging.warning("Power-fit failed. No fitted line will be plotted.")
        except TypeError:
            average_fit = np.ones_like(logbins)
            logging.warning("Power-fit failed. No fitted line will be plotted.")
        # axes[2].set_title(f"({(alpha-1)/(tau-1)=:.2f})")
        svz_estim_ratio = (alpha - 1) / (tau - 1)
        col.append([values, avearges, logbins, average_fit, svz, svz_estim_ratio])

        return col

    def branching_ratio_histogram(self):
        _, _, branching_ratio, _, _ = self.output["avalanche_analysis"]
        branching_ratio = branching_ratio[np.nonzero(branching_ratio)]
        mean_branching_ratio = branching_ratio.mean()
        return branching_ratio, mean_branching_ratio
