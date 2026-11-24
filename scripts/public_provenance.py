"""Shared checks for provenance values that are safe to publish."""
import re

_WINDOWS_PATH = re.compile(r"^[A-Za-z]:")
_ENCODED_SEPARATOR = re.compile(r"%(?:2f|5c)", re.IGNORECASE)
_PRIVATE_ROOT = re.compile(r"(?:^|[^A-Za-z0-9_]|%(?:2f|5c))raw(?:[\\/]|%(?:2f|5c)|$)", re.IGNORECASE)


def exposes_private_path(value):
    """Return whether a public provenance value exposes a private filesystem path."""
    if not isinstance(value, str) or not value.strip():
        return True
    candidate = value.strip()
    return (
        candidate.startswith(("/", "\\"))
        or bool(re.match(r"^%(?:2f|5c)", candidate, re.IGNORECASE))
        or bool(_WINDOWS_PATH.match(candidate))
        or bool(_PRIVATE_ROOT.search(candidate))
    )


def is_public_original_filename(value):
    """Return whether a value is a filename rather than a path or private root."""
    return (
        not exposes_private_path(value)
        and "/" not in value
        and "\\" not in value
        and not _ENCODED_SEPARATOR.search(value)
        and value not in (".", "..")
    )
