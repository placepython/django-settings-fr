from pathlib import Path

import environ

def search_dir(from_dir, *items, exclude_dirs=None, stop_when=None, max_parents=None):
    """
    Recursively searches for specified items (files or directories) starting from the given directory
    and its parent directories, up to a specified limit of parent levels. If one of the stop conditions
    is met, the search halts.

    Parameters:
    - from_dir (str or Path): The starting directory to begin the search.
    - *items (str): The names of files or directories to search for.
    - exclude_dirs (str or list, optional): Directory or directories to exclude from the search.
    - stop_when (str or list, optional): A file or directory name (or list of names) that,
      if found, stops the upward traversal of directories.
    - max_parents (int, optional): The maximum number of parent directories to search through.
      If None, it will traverse all the way to the root.

    Returns:
    - Path or None: If an item is found, returns the absolute path of the directory containing it
      (or the directory itself if the item is a directory). If no item is found, returns None.
    """

    # Convert from_dir to Path and resolve it to an absolute path
    start_path = Path(from_dir).resolve(strict=True)

    # If exclude_dirs is a string, convert it to a list
    if isinstance(exclude_dirs, str):
        exclude_dirs = [exclude_dirs]
    elif exclude_dirs is None:
        exclude_dirs = []

    # If stop_when is a string, convert it to a list
    if isinstance(stop_when, str):
        stop_when = [stop_when]
    elif stop_when is None:
        stop_when = []

    # Function to check if a directory is in the exclude list
    def is_excluded(directory):
        return any(exclude in str(directory) for exclude in exclude_dirs)

    # Function to search a directory and its subdirectories for the items
    def search_in_directory(directory):
        if is_excluded(directory):
            return None

        # Traverse the directory and its subdirectories
        for child in directory.rglob('*'):
            if is_excluded(child.parent):
                continue
            # If an item is found, return the parent directory if it's a file, or the item itself if it's a directory
            if child.name in items:
                return child.parent.resolve(strict=True) if child.is_file() else child.resolve(strict=True)
        return None

    # Function to check if the stop_when condition is met in the directory
    def check_stop_condition(directory):
        for stop_item in stop_when:
            if (directory / stop_item).exists():
                return True
        return False

    # Traverse from from_dir and its parent directories
    parents_list = [start_path] + list(start_path.parents)

    # If max_parents is specified, limit the number of parent directories to search
    if max_parents is not None:
        parents_list = parents_list[:max_parents + 1]  # Include the start directory plus max_parents levels

    for directory in parents_list:
        # First, search the current directory and its children
        result = search_in_directory(directory)
        if result:
            return result

        # Check if the stop condition is met
        if check_stop_condition(directory):
            print(f"Stopping traversal: One of the stop_when items found in {directory}")
            break

    return None

BASE_DIR = search_dir(__file__, "manage.py", exclude_dirs=[".venv", "venv"])

env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))
