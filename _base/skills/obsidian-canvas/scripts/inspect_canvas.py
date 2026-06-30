#!/usr/bin/env python3
"""Inspect and lightly validate an Obsidian .canvas file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


VALID_SIDES = {"top", "right", "bottom", "left"}


def rect(node: dict) -> tuple[float, float, float, float]:
    x = float(node.get("x", 0))
    y = float(node.get("y", 0))
    w = float(node.get("width", 0))
    h = float(node.get("height", 0))
    return x, y, x + w, y + h


def overlaps(a: dict, b: dict, padding: float = 0) -> bool:
    ax1, ay1, ax2, ay2 = rect(a)
    bx1, by1, bx2, by2 = rect(b)
    return ax1 < bx2 + padding and ax2 + padding > bx1 and ay1 < by2 + padding and ay2 + padding > by1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and summarize an Obsidian .canvas file.")
    parser.add_argument("canvas", type=Path, help="Path to a .canvas file")
    parser.add_argument("--overlap-padding", type=float, default=0, help="Extra padding for overlap warnings")
    args = parser.parse_args()

    issues: list[str] = []
    warnings: list[str] = []

    try:
        data = json.loads(args.canvas.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: cannot parse JSON: {exc}", file=sys.stderr)
        return 2

    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list):
        issues.append("top-level 'nodes' is missing or is not a list")
        nodes = []
    if not isinstance(edges, list):
        issues.append("top-level 'edges' is missing or is not a list")
        edges = []

    node_by_id: dict[str, dict] = {}
    for index, node in enumerate(nodes):
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            issues.append(f"node #{index} has no string id")
            continue
        if node_id in node_by_id:
            issues.append(f"duplicate node id: {node_id}")
        node_by_id[node_id] = node

        for key in ("x", "y", "width", "height"):
            if not isinstance(node.get(key), (int, float)):
                issues.append(f"node {node_id} has invalid {key}")
        if isinstance(node.get("width"), (int, float)) and node["width"] <= 0:
            issues.append(f"node {node_id} width must be positive")
        if isinstance(node.get("height"), (int, float)) and node["height"] <= 0:
            issues.append(f"node {node_id} height must be positive")

    edge_ids: set[str] = set()
    for index, edge in enumerate(edges):
        edge_id = edge.get("id", f"#{index}")
        if isinstance(edge_id, str):
            if edge_id in edge_ids:
                issues.append(f"duplicate edge id: {edge_id}")
            edge_ids.add(edge_id)

        for endpoint in ("fromNode", "toNode"):
            value = edge.get(endpoint)
            if value not in node_by_id:
                issues.append(f"edge {edge_id} references missing {endpoint}: {value}")

        for side_key in ("fromSide", "toSide"):
            side = edge.get(side_key)
            if side is not None and side not in VALID_SIDES:
                issues.append(f"edge {edge_id} has invalid {side_key}: {side}")

    sorted_nodes = sorted(node_by_id.values(), key=lambda n: (n.get("y", 0), n.get("x", 0)))
    for i, first in enumerate(sorted_nodes):
        for second in sorted_nodes[i + 1 :]:
            if overlaps(first, second, args.overlap_padding):
                warnings.append(f"nodes may overlap: {first['id']} and {second['id']}")

    print(f"canvas: {args.canvas}")
    print(f"nodes: {len(nodes)}")
    print(f"edges: {len(edges)}")
    print()
    print("nodes by vertical order:")
    for node in sorted_nodes:
        print(
            f"  {node['id']}: x={node.get('x')} y={node.get('y')} "
            f"w={node.get('width')} h={node.get('height')}"
        )

    if warnings:
        print()
        print("warnings:")
        for warning in warnings:
            print(f"  WARN: {warning}")

    if issues:
        print()
        print("issues:")
        for issue in issues:
            print(f"  ERROR: {issue}")
        return 1

    print()
    print("OK: valid canvas structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
