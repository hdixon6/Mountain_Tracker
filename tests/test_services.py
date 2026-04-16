from app.services import transform_mountain_payload, validate_review


def test_transform_mountain_payload_sorts_and_excludes_missing_names():
    payload = [
        {"id": 2, "name": "Snowdon", "elevation": 1085},
        {"id": 1, "name": "Ben Nevis", "elevation": 1345},
        {"id": 3, "name": None, "elevation": 999},
        {"id": 4, "name": "Helvellyn"},
    ]

    result = transform_mountain_payload(payload, "United Kingdom")

    assert [item.name for item in result] == ["Ben Nevis", "Helvellyn", "Snowdon"]
    assert result[1].elevation_m is None


def test_validate_review_rejects_bad_input():
    errors = validate_review("9", "   ")
    assert "Rating must be between 1 and 5." in errors
    assert "Review text is required." in errors
