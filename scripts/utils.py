"""
Utility functions for NASA ADS data fetching scripts.
"""
import random
import time
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


def retry_with_backoff(fn, *, attempts=5, base_delay=30, max_delay=900,
                        exceptions=(Exception,), on_retry=None):
    """Call fn(), retrying with exponential backoff and jitter.

    Delays are computed as min(base_delay * 2**n, max_delay) plus a small
    random jitter, rather than read from a fixed list, so raising `attempts`
    is a real knob (no IndexError ceiling).

    Args:
        fn: Zero-argument callable to invoke.
        attempts: Maximum number of calls to fn (>= 1).
        base_delay: Delay in seconds before the first retry.
        max_delay: Upper bound on any single delay.
        exceptions: Exception type(s) that trigger a retry.
        on_retry: Optional callback `on_retry(attempt, exc, delay)`, called
            before each retry sleep (attempt is 0-indexed: the attempt that
            just failed).

    Returns:
        The return value of the first successful call to fn.

    Raises:
        The exception raised by the final attempt, if every attempt fails.
        ValueError: If attempts < 1.
    """
    if attempts < 1:
        raise ValueError(f"attempts must be >= 1, got {attempts}")

    for attempt in range(attempts):
        try:
            return fn()
        except exceptions as e:
            if attempt >= attempts - 1:
                raise
            delay = min(base_delay * 2 ** attempt, max_delay)
            delay += random.uniform(0, delay * 0.1)
            if on_retry is not None:
                on_retry(attempt, e, delay)
            time.sleep(delay)