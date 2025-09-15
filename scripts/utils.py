"""
Utility functions for NASA ADS data fetching scripts.
"""
from pathlib import Path


def get_repo_root() -> Path:
    """
    Get the repository root directory.

    Returns the absolute path to the repository root, which is assumed
    to be one level up from the scripts directory.

    Returns:
        Path: Absolute path to the repository root directory.

    Raises:
        RuntimeError: If the expected directory structure is not found.
    """
    # Get the directory containing this utils.py file (scripts/)
    scripts_dir = Path(__file__).parent

    # Repository root is parent of scripts directory
    repo_root = scripts_dir.parent

    # Validate that we're in the expected structure
    expected_markers = [
        repo_root / "public",
        repo_root / "package.json",
        repo_root / "scripts"
    ]

    if not all(marker.exists() for marker in expected_markers):
        raise RuntimeError(
            f"Repository structure validation failed. "
            f"Expected to find 'public/', 'package.json', and 'scripts/' in {repo_root}"
        )

    return repo_root.resolve()  # Return absolute path


def get_public_data_dir() -> Path:
    """
    Get the public/data directory path.

    Note: This returns the path only. Call path.mkdir(parents=True, exist_ok=True)
    if you need to ensure the directory exists.

    Returns:
        Path: Absolute path to public/data directory.
    """
    return get_repo_root() / "public" / "data"


def get_public_plots_dir() -> Path:
    """
    Get the public/plots directory path.

    Note: This returns the path only. Call path.mkdir(parents=True, exist_ok=True)
    if you need to ensure the directory exists.

    Returns:
        Path: Absolute path to public/plots directory.
    """
    return get_repo_root() / "public" / "plots"


def get_relative_path(path: Path) -> Path:
    """
    Convert an absolute path to a path relative to the repository root.

    If the path is not within the repository, returns the original path.

    Args:
        path: Path to convert (can be absolute or relative)

    Returns:
        Path: Relative path from repo root, or original path if not in repo
    """
    try:
        # Ensure we have absolute paths for comparison
        abs_path = path.resolve()
        repo_root = get_repo_root()
        return abs_path.relative_to(repo_root)
    except ValueError:
        # Path is not within the repository
        return path