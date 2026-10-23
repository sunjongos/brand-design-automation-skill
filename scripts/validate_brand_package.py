#!/usr/bin/env python3
"""Validate a brand-package JSON without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def _luminance(hex_color: str) -> float:
    channels = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(a: str, b: str) -> float:
    light, dark = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    def need(path: str, value, kind=None):
        if value is None or value == "" or value == []:
            errors.append(f"{path}: required")
        elif kind and not isinstance(value, kind):
            errors.append(f"{path}: expected {kind.__name__}")

    for key in ("brand", "audience", "strategy", "voice", "visual", "governance"):
        need(key, data.get(key), dict)
    need("channels", data.get("channels"), list)
    if errors:
        return errors

    need("brand.name", data["brand"].get("name"), str)
    need("audience.primary", data["audience"].get("primary"), str)
    need("audience.problem", data["audience"].get("problem"), str)
    need("strategy.promise", data["strategy"].get("promise"), str)
    need("strategy.proof", data["strategy"].get("proof"), list)
    need("strategy.primary_cta", data["strategy"].get("primary_cta"), str)

    traits = data["voice"].get("traits", [])
    if not 3 <= len(traits) <= 5:
        errors.append("voice.traits: use 3 to 5 traits")
    for key in ("do", "dont"):
        if len(data["voice"].get(key, [])) < 2:
            errors.append(f"voice.{key}: provide at least 2 rules")

    visual = data["visual"]
    colors = visual.get("colors", {})
    if not isinstance(colors, dict):
        return errors + ["visual.colors: expected dict"]
    for key in ("primary", "background", "text", "accent"):
        value = colors.get(key)
        if not isinstance(value, str) or not HEX.fullmatch(value):
            errors.append(f"visual.colors.{key}: expected #RRGGBB")
    if all(isinstance(colors.get(key), str) and HEX.fullmatch(colors[key]) for key in ("text", "background")):
        ratio = _contrast(colors["text"], colors["background"])
        if ratio < 4.5:
            errors.append(f"visual.colors: text/background contrast {ratio:.2f}:1 is below 4.5:1")
    size = visual.get("typography", {}).get("minimum_body_px", 0)
    if not isinstance(size, (int, float)) or size < 12:
        errors.append("visual.typography.minimum_body_px: must be >= 12")
    if len(visual.get("spacing", [])) < 4:
        errors.append("visual.spacing: provide at least 4 tokens")

    channels = data["channels"]
    if channels:
        names = []
        for i, channel in enumerate(channels):
            if not isinstance(channel, dict):
                errors.append(f"channels[{i}]: expected dict")
                continue
            name = channel.get("name")
            need(f"channels[{i}].name", name, str)
            need(f"channels[{i}].deliverables", channel.get("deliverables"), list)
            names.append(name)
        if len(names) != len(set(names)):
            errors.append("channels: duplicate channel names")

    governance = data["governance"]
    need("governance.approver", governance.get("approver"), str)
    for key in ("rights_checked", "privacy_checked", "claims_checked"):
        if governance.get(key) is not True:
            errors.append(f"governance.{key}: must be true before release")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.package.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}")
        return 2
    errors = validate(data)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: brand package passes release prerequisites")
    return 0


if __name__ == "__main__":
    sys.exit(main())
