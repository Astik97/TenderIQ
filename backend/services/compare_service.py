"""
==========================================
Compare Service
------------------------------------------
Responsible for

1. Calling Similarity Engine
2. Preparing Comparison Result
3. Returning Complete Report
==========================================
"""

from backend.services.similarity_service import (
    calculate_similarity,
    get_similarity_level,
    get_similarity_color
)

def compare_tenders(text1, text2):

    score = calculate_similarity(
        text1,
        text2
    )

    level = get_similarity_level(score)

    color = get_similarity_color(score)

    comparison_result = {

        "similarity": score,

        "level": level,

        "color": color

    }

    return comparison_result