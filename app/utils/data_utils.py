import glob
import os
import re


def modify(spikestamps, pre_burst_extension, post_burst_extension):
    """Modify spikestamps with pre and post burst extensions."""
    # TODO: Implement this function based on your requirements
    return spikestamps


def get_subdirectories(workdir: str, tag: str):
    if not workdir or not os.path.exists(workdir):
        return []

    glob_pattern = os.path.join(workdir, "**", tag)
    paths = []
    full_paths = []
    for dir_path in glob.glob(glob_pattern, recursive=True):
        if os.path.isdir(dir_path):
            parent_dir = os.path.dirname(dir_path)
            paths.append(parent_dir.split(workdir)[1])
            full_paths.append(parent_dir)

    path_pairs = list(zip(paths, full_paths, strict=False))
    path_pairs.sort(key=lambda x: x[0])
    sorted_paths, sorted_full_paths = zip(*path_pairs, strict=False)

    return list(sorted_paths), list(sorted_full_paths)


def get_experiment_index(workdir: str, tag: str):
    matches = []
    # Extract the pattern from tag, assuming there is only one *
    re_pattern = tag.replace("*", r"(\d+)")
    # Find all matches in the directory
    for item in os.listdir(workdir):
        match = re.match(re_pattern, item)
        if match:
            matches.append(match.group(1))
    return sorted(matches)

    # Get relative paths to parent directories and extract identifiers
    relative_paths = []
    identifiers = []
    pattern = re.compile(f"{tag}(.*)")

    # Get the full paths first
    _, full_paths = get_subdirectories(workdir, tag)
    if not full_paths:
        return [], [], []

    for full_path in full_paths:
        parent_dir = os.path.dirname(full_path)
        rel_path = os.path.relpath(parent_dir, workdir)
        relative_paths.append(rel_path)

        # Extract the identifier after spike_detection_
        dir_name = os.path.basename(full_path)
        match = pattern.match(dir_name)
        if match:
            identifiers.append(match.group(1))
        else:
            identifiers.append(None)

    return full_paths, relative_paths, identifiers
