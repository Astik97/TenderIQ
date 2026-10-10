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

    "Payment": 10,
    "Payment Terms": 10,
    "EMD": 10,
    "Earnest Money": 10,
    "Bid Security": 10,
    "Eligibility": 10,
    "Qualification": 10,

    "Technical": 9,
    "Technical Specification": 9,
    "Specification": 9,
    "Scope": 9,
    "Experience": 9,

    "Warranty": 8,
    "Guarantee": 8,
    "Penalty": 8,
    "Liquidated Damages": 8,
    "Contract": 8,
    "Termination": 8,

    "Delivery": 7,
    "Timeline": 7,
    "Completion": 7,

    "Invoice": 6,
    "Price": 6,
    "GST": 6,
    "Tax": 6,

    "Address": 2,
    "Contact": 2,

    "Email": 1,
    "Phone": 1,
    "Website": 1
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

    return round(weighted_sum / total_weight, 2)

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
    difference_percentage = round(100 - weighted_similarity,2)

    return {
        "weighted_similarity": weighted_similarity,
        "difference_percentage": difference_percentage,
        "total_weight": sum(weights),
        "average_weight": round(sum(weights) / len(weights),2),
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
    critical_percentage = round((critical / total_clauses) * 100,2)
    
    return {
        **statistics,
        "critical_clauses": critical,
        "high_priority_clauses": high,
        "medium_priority_clauses": medium,
        "low_priority_clauses": low,
        "critical_percentage": critical_percentage
    } 