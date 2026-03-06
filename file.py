#!/usr/bin/env python3
"""Generate random test files quickly using a shared random blob + small worker threads."""

from __future__ import annotations

import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

NUM_DIRS = int(os.getenv("NUM_DIRS", "100"))
FILES_PER_DIR = int(os.getenv("FILES_PER_DIR", "1000"))
MIN_FILE_SIZE = int(os.getenv("MIN_FILE_SIZE", str(1024)))
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(5 * 1024)))
BLOB_SIZE = int(os.getenv("BLOB_SIZE", str(8 * 1024 * 1024)))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", str(min(8, max(2, os.cpu_count() or 2)))))


def write_directory(directory_id: int, blob: bytes, seed: int) -> None:
    rng = random.Random(seed)
    directory = Path(str(directory_id))
    directory.mkdir(parents=True, exist_ok=True)

    upper_bound = len(blob)
    for file_id in range(1, FILES_PER_DIR + 1):
        size = rng.randint(MIN_FILE_SIZE, MAX_FILE_SIZE)
        start = rng.randint(0, upper_bound - size)
        (directory / f"{file_id}.rnd").write_bytes(blob[start : start + size])


def main() -> None:
    if MIN_FILE_SIZE <= 0 or MAX_FILE_SIZE < MIN_FILE_SIZE:
        raise ValueError("Invalid file size bounds.")
    if BLOB_SIZE < MAX_FILE_SIZE:
        raise ValueError("BLOB_SIZE must be >= MAX_FILE_SIZE.")
    if NUM_DIRS <= 0 or FILES_PER_DIR <= 0 or MAX_WORKERS <= 0:
        raise ValueError("NUM_DIRS, FILES_PER_DIR, and MAX_WORKERS must be > 0.")

    blob = os.urandom(BLOB_SIZE)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [
            pool.submit(write_directory, directory_id, blob, random.randrange(2**63))
            for directory_id in range(1, NUM_DIRS + 1)
        ]
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    main()
