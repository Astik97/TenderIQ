"""
=========================================================
TenderIQ Weight Service
---------------------------------------------------------
Responsible for

1. Clause Importance
2. Weighted Similarity
3. Weighted Statistics
4. Weight Summary
=========================================================
"""

# =========================================================
# Clause Weights
# =========================================================

CLAUSE_WEIGHTS = {

    "payment": 10,
    "payment terms": 10,
    "emd": 10,
    "earnest money": 10,
    "bid security": 10,
    "eligibility": 10,
    "qualification": 10,

    "technical": 9,
    "technical specification": 9,
    "specification": 9,
    "scope": 9,
    "experience": 9,

    "warranty": 8,
    "guarantee": 8,
    "penalty": 8,
    "liquidated damages": 8,
    "contract": 8,
    "termination": 8,

    "delivery": 7,
    "timeline": 7,
    "completion": 7,

    "invoice": 6,
    "price": 6,
    "gst": 6,
    "tax": 6,

    "address": 2,
    "contact": 2,

    "email": 1,
    "phone": 1,
    "website": 1
}

# =========================================================
# Weight Configuration
# =========================================================

DEFAULT_WEIGHT = 5

CRITICAL_WEIGHT = 10

HIGH_WEIGHT = 8

MEDIUM_WEIGHT = 5

# =========================================================
# Get Clause Weight
# =========================================================

def get_clause_weight(clause):
    """
    Returns the importance weight of a clause.

    Default weight = 5
    """

    if not clause:
        return DEFAULT_WEIGHT

    clause = clause.lower()

    for keyword, weight in CLAUSE_WEIGHTS.items():

        if keyword in clause:

            return weight

    return DEFAULT_WEIGHT

# =========================================================
# Weighted Similarity
# =========================================================

def calculate_weighted_similarity(clause_results):
    """
    Calculate weighted similarity score.

    Formula

    Sum(similarity × weight)
    ------------------------
         Sum(weight)
    """

    if not clause_results:
        return 0

    weighted_sum = 0

    total_weight = 0

    for clause in clause_results:

        weight = get_clause_weight(clause.get("clause", ""))

        similarity = clause.get("similarity", 0)

        weighted_sum += similarity * weight

        total_weight += weight

    if total_weight == 0:
        return 0

    return round(weighted_sum / total_weight, 
                2)

# =========================================================
# Weighted Statistics
# =========================================================

def calculate_weighted_statistics(clause_results):
    """
    Generate weighted statistics.
    """

    if not clause_results:

        return {

            "weighted_similarity": 0,

            "total_weight": 0,

            "average_weight": 0,

            "highest_weight": 0,

            "lowest_weight": 0

        }

    weights = [

    get_clause_weight(clause.get("clause", ""))

    for clause in clause_results

    ]

    weighted_similarity = calculate_weighted_similarity(clause_results)

    difference_percentage = round(
        100 - weighted_similarity,
        2)

    return {

        "weighted_similarity": weighted_similarity,

        "difference_percentage": difference_percentage,

        "total_weight": sum(weights),

        "average_weight": round(
            sum(weights) / len(weights),
            2),

        "highest_weight": max(weights),

        "lowest_weight": min(weights)

    }

# =========================================================
# Weight Summary
# =========================================================

def get_weight_summary(clause_results):
    """
    Returns a complete weight summary.
    """

    if not clause_results:

        return {

            "weighted_similarity": 0,

            "total_weight": 0,

            "average_weight": 0,

            "highest_weight": 0,

            "lowest_weight": 0,

            "critical_clauses": 0,

            "high_priority_clauses": 0,

            "medium_priority_clauses": 0,

            "low_priority_clauses": 0,

            "critical_percentage": 0

        }

    statistics = calculate_weighted_statistics(clause_results)

    critical = 0

    high = 0

    medium = 0

    low = 0

    for clause in clause_results:

        weight = get_clause_weight(clause.get("clause", ""))

        if weight >= 10:
            critical += 1

        elif weight >= 8:
            high += 1

        elif weight >= 5:
            medium += 1

        else:
            low += 1

    total_clauses = len(clause_results)

    critical_percentage = round(
        (critical / total_clauses) * 100,
        2)

    return {

    **statistics,

    "critical_clauses": critical,

    "high_priority_clauses": high,

    "medium_priority_clauses": medium,

    "low_priority_clauses": low,

    "critical_percentage": critical_percentage

} 