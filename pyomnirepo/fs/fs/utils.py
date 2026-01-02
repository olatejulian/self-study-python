from pathlib import Path


def is_binary_file(path: Path, chunk_size: int = 1024) -> bool:
    """Check if a file is binary by reading a chunk of its content."""
    with path.open("rb") as f:
        chunk = f.read(chunk_size)
        if b"\0" in chunk:
            return True
    return False
