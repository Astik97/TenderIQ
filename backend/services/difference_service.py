"""
==========================================
Difference Service
------------------------------------------
Responsible for

1. Compare two clauses
2. Find added words
3. Find removed words
4. Build concise summary

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

STOP_WORDS = {
    "the","a","an","is","are","was","were",
    "should","shall","will","may","can",
    "be","to","of","for","and","or","in",
    "on","within","have","has","had","by",
    "this","that","these","those"
}

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
    
    added = list(matched_words - original_words)

    added = [
        word
        for word in added
        if len(word) > 2
        and word not in STOP_WORDS
    ]

    return sorted(added)

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
    
    removed = list(original_words - matched_words)

    removed = [
        word
        for word in removed
        if len(word) > 2
        and word not in STOP_WORDS
    ]

    return sorted(removed)

def build_summary(added, removed):
    """
    Build a concise summary.
    """

    if not added and not removed:

        return "No significant text difference detected."

    summary = []

    if added:

        preview = ", ".join(added[:3])

        if len(added) > 3:
            preview += "..."

        summary.append(
            f"Added ({len(added)}): {preview}"
        )

    if removed:

        preview = ", ".join(removed[:3])

        if len(removed) > 3:
            preview += "..."

        summary.append(
            f"Removed ({len(removed)}): {preview}"
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
    ),

    "added_count": len(added),

    "removed_count": len(removed),

    "total_changes": len(added) + len(removed)
}