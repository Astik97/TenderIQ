"""
==========================================
Difference Service
------------------------------------------
Responsible for

1. Compare two clauses
2. Find added words
3. Find removed words
4. Build concise summary

No database operations.
No similarity calculation.
==========================================
"""

import re

def tokenize(text):
    """
    Convert clause into lowercase tokens.
    """

    if not text:
        return []

    return re.findall(
        r"\b\w+\b",
        text.lower()
    )

def get_added_words(original, matched):
    """
    Words present only in matched clause.
    """

    original_words = set(
        tokenize(original)
    )

    matched_words = set(
        tokenize(matched)
    )

    return sorted(
        list(
            matched_words - original_words
        )
    )

def get_removed_words(original, matched):
    """
    Words removed from original clause.
    """

    original_words = set(
        tokenize(original)
    )

    matched_words = set(
        tokenize(matched)
    )

    return sorted(
        list(
            original_words - matched_words
        )
    )

def build_summary(added, removed):
    """
    Build a concise summary.
    """

    if not added and not removed:

        return "No significant textual difference detected."

    summary = []

    if added:

        summary.append(
            "Added: " + ", ".join(added)
        )

    if removed:

        summary.append(
            "Removed: " + ", ".join(removed)
        )

    return " | ".join(summary)

def compare_clauses(original, matched):
    """
    Compare two clauses.
    """

    added = get_added_words(
        original,
        matched
    )

    removed = get_removed_words(
        original,
        matched
    )

    return {

        "changed": bool(
            added or removed
        ),

        "added": added,

        "removed": removed,

        "summary": build_summary(
            added,
            removed
        )

    }