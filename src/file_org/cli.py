from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .organiser import organise, CATEGORY_NAMES


def _join(items: list[tuple[Path, Path]]) -> str:
    lines = [f"  {a.name}  ->  {b.parent.name}/{b.name}" for a, b in items]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="file-org",
        description="Organise files in a directory by category",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        type=Path,
        help="Directory to organise (default: current)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview changes without moving files",
    )
    parser.add_argument(
        "--undo", "-u",
        action="store_true",
        help="Revert the last organise",
    )
    args = parser.parse_args(argv)

    target = args.directory.resolve()

    if not target.is_dir():
        print(f"error: {target} is not a directory", file=sys.stderr)
        return 1

    verb = "Undo" if args.undo else ("Would organise" if args.dry_run else "Organise")
    print(f"{verb} {target}")

    result = organise(
        directory=target,
        dry_run=args.dry_run,
        undo=args.undo,
    )

    if result.moved:
        tag = "Would move" if args.dry_run else ("Reverted" if args.undo else "Moved")
        print(f"\n{tag} {len(result.moved)} file(s):")
        print(_join(result.moved))

    if result.skipped:
        print(f"\nSkipped {len(result.skipped)} file(s) (already exist at target)")

    if result.errors:
        print(f"\n{len(result.errors)} error(s):", file=sys.stderr)
        for src, msg in result.errors:
            print(f"  {src}: {msg}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
