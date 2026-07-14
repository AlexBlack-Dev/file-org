from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from .categories import CATEGORIES, UNCATEGORISED

CATEGORY_NAMES = set(CATEGORIES) | {UNCATEGORISED}


def classify(ext: str) -> str:
    for cat, exts in CATEGORIES.items():
        if ext.lower() in exts:
            return cat
    return UNCATEGORISED


@dataclass
class OrganiseResult:
    moved: list[tuple[Path, Path]] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    errors: list[tuple[Path, str]] = field(default_factory=list)


def organise(
    directory: Path,
    dry_run: bool = False,
    undo: bool = False,
    snapshot: Path | None = None,
) -> OrganiseResult:
    result = OrganiseResult()
    snapshot_path = snapshot or directory / ".file-org-snapshot.json"

    if undo:
        return _undo(snapshot_path, dry_run)

    items = [p for p in directory.iterdir() if p.is_file()]
    moves: list[tuple[Path, Path]] = []

    for item in items:
        ext = item.suffix
        cat = classify(ext)
        target_dir = directory / cat
        target = target_dir / item.name

        if target.exists():
            result.skipped.append(item)
            continue

        try:
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(target))
            moves.append((item, target))
            result.moved.append((item, target))
        except OSError as e:
            result.errors.append((item, str(e)))

    if not dry_run and moves:
        snapshot_data = [
            {"from": str(src), "to": str(dst)}
            for src, dst in moves
        ]
        if snapshot_path.exists():
            existing = json.loads(snapshot_path.read_text())
            snapshot_data = existing + snapshot_data
        snapshot_path.write_text(json.dumps(snapshot_data, indent=2))

    return result


def _undo(snapshot_path: Path, dry_run: bool) -> OrganiseResult:
    result = OrganiseResult()

    if not snapshot_path.exists():
        result.errors.append((snapshot_path, "No snapshot found to undo"))
        return result

    snapshot = json.loads(snapshot_path.read_text())

    for entry in reversed(snapshot):
        src = Path(entry["from"])
        dst = Path(entry["to"])

        if not dst.exists():
            result.skipped.append(dst)
            continue

        try:
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dst), str(src))
            result.moved.append((dst, src))
        except OSError as e:
            result.errors.append((dst, str(e)))

    if not dry_run:
        snapshot_path.unlink(missing_ok=True)

    return result
