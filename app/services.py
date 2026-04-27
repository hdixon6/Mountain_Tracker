from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pycountry


API_URL = "https://api.api-ninjas.com/v1/mountains"


@dataclass
class MountainDTO:
    external_id: str | None
    name: str
    country: str
    elevation_m: int | None


class ExternalApiError(RuntimeError):
    pass


def country_choices() -> list[str]:
    names = sorted({country.name for country in pycountry.countries})
    return names


def validate_review(rating: str, review_text: str) -> list[str]:
    errors: list[str] = []

    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 5:
            errors.append("Rating must be between 1 and 5.")
    except (TypeError, ValueError):
        errors.append("Rating must be a number between 1 and 5.")

    if not review_text or not review_text.strip():
        errors.append("Review text is required.")

    return errors


def transform_mountain_payload(payload: list[dict[str, Any]], selected_country: str) -> list[MountainDTO]:
    mountains: list[MountainDTO] = []

    for row in payload:
        name = row.get("name")
        if not name:
            continue

        elevation = row.get("elevation")
        elevation_int = int(elevation) if isinstance(elevation, (int, float)) else None

        mountains.append(
            MountainDTO(
                external_id=str(row.get("id")) if row.get("id") is not None else None,
                name=name.strip(),
                country=selected_country,
                elevation_m=elevation_int,
            )
        )

    return sorted(mountains, key=lambda item: item.name.lower())


def fetch_mountains_by_country(country: str, api_key: str | None = None) -> list[MountainDTO]:
    import json
    from pathlib import Path

    data_path = Path(__file__).resolve().parent.parent / "data" / "mountains.json"

    try:
        with open(data_path, "r", encoding="utf-8") as file:
            payload = json.load(file)
    except OSError as exc:
        raise ExternalApiError("Unable to load mountain data right now.") from exc

    if not isinstance(payload, list):
        raise ExternalApiError("Unexpected mountain data format.")

    filtered = [row for row in payload if row.get("country") == country]

    return transform_mountain_payload(filtered, country)
