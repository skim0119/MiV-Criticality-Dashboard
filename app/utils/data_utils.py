import glob
import os
import re


def modify(spikestamps, pre_burst_extension, post_burst_extension):
    """Modify spikestamps with pre and post burst extensions."""
    # TODO: Implement this function based on your requirements
    return spikestamps


def get_subdirectories(workdir: str, tag: str):
    if not workdir or not os.path.exists(workdir):
        return [], []

    glob_pattern = os.path.join(workdir, "**", tag)
    paths = []
    full_paths = []
    for dir_path in glob.glob(glob_pattern, recursive=True):
        if os.path.isdir(dir_path):
            parent_dir = os.path.dirname(dir_path)
            if parent_dir == workdir:
                path = "."
            else:
                path = parent_dir.split(workdir)[1]
            paths.append(path)
            full_paths.append(parent_dir)

    path_pairs = list(zip(paths, full_paths, strict=False))
    path_pairs.sort(key=lambda x: x[0])
    if len(path_pairs) == 0:
        return [], []
    sorted_paths, sorted_full_paths = zip(*path_pairs, strict=False)

    return list(sorted_paths), list(sorted_full_paths)


def get_experiment_index(workdir: str, tag: str):
    matches = []
    if "*" in tag:
        # Extract the pattern from tag, assuming there is only one *
        re_pattern = tag.replace("*", r"(.*)")
        # Find all matches in the directory
        for item in os.listdir(workdir):
            match = re.match(re_pattern, item)
            if match:
                matches.append(match.group(1))
        return sorted(matches)
    else:
        if os.path.exists(os.path.join(workdir, tag)):
            return [tag]
        else:
            return []
