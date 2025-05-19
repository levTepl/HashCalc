#!/usr/bin/env python3
import os
import hashlib
import argparse

def directory_hash(dir_path, include_empty_dirs=False, followlinks=False):
    h = hashlib.sha256()
    for root, dirs, files in os.walk(dir_path, topdown=True, followlinks=followlinks):
        dirs.sort(key=str.casefold)
        files.sort(key=str.casefold)

        if include_empty_dirs and not files and not dirs:
            rel_dir = os.path.relpath(root, dir_path).replace(os.sep, '/')
            h.update(rel_dir.encode('utf-8') + b'\0')

        for fname in files:
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, dir_path).replace(os.sep, '/')
            h.update(rel.encode('utf-8') + b'\0')
            with open(fpath, 'rb') as fh:
                for chunk in iter(lambda: fh.read(8192), b''):
                    h.update(chunk)

    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(
        description="Compute a deterministic SHA-256 over a directory tree."
    )
    p.add_argument("directory",
                   help="Path to the directory you want to hash")
    p.add_argument("--include-empty-dirs", action="store_true",
                   help="Also incorporate empty subdirectories into the hash")
    p.add_argument("--follow-links", action="store_true",
                   help="Follow symbolic links when walking")
    args = p.parse_args()

    digest = directory_hash(
        args.directory,
        include_empty_dirs=args.include_empty_dirs,
        followlinks=args.follow_links
    )
    print(digest)

if __name__ == "__main__":
    main()

