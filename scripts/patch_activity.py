"""Measure patch inactivity from submission and discussion timestamps."""
from datetime import UTC, datetime, timedelta
from itertools import chain


def has_recent_activity(patch, comments, now):
    dates = (datetime.fromisoformat(item["date"]) for item in chain([patch], comments))
    latest = max(date.replace(tzinfo=UTC) if date.tzinfo is None else date for date in dates)
    return now - latest < timedelta(days=30)
