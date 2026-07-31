"""
=========================================================
TenderIQ Chart Service
---------------------------------------------------------
Responsible for preparing chart data for Chart.js

1. Similarity Pie Chart
2. Risk Pie Chart
3. Priority Bar Chart
4. Dashboard Summary Chart
=========================================================
"""

# =========================================================
# Similarity Chart
# =========================================================

def generate_similarity_chart(analytics):

    distribution = analytics["similarity_distribution"]

    return {

        "labels": [

            "Excellent",

            "Good",

            "Moderate",

            "Poor"

        ],

        "values": [

            distribution["Excellent"],

            distribution["Good"],

            distribution["Moderate"],

            distribution["Poor"]

        ]

    }

# =========================================================
# Risk Chart
# =========================================================

def generate_risk_chart(analytics):

    distribution = analytics["risk_distribution"]

    return {

        "labels": [

            "Very Low Risk",

            "Low Risk",

            "Medium Risk",

            "High Risk",

            "Critical Risk"

        ],

        "values": [

            distribution["Very Low Risk"],

            distribution["Low Risk"],

            distribution["Medium Risk"],

            distribution["High Risk"],

            distribution["Critical Risk"]

        ]

    }

# =========================================================
# Priority Chart
# =========================================================

def generate_priority_chart(weight_summary):

    return {

        "labels": [

            "Critical",

            "High",

            "Medium",

            "Low"

        ],

        "values": [

            weight_summary["critical_clauses"],

            weight_summary["high_priority_clauses"],

            weight_summary["medium_priority_clauses"],

            weight_summary["low_priority_clauses"]

        ]

    }

# =========================================================
# Dashboard Summary
# =========================================================

def generate_dashboard_chart(result):

    return {

        "labels": [

            "Overall Similarity",

            "Weighted Similarity",

            "Difference"

        ],

        "values": [

            result["similarity"],

            result["weighted_similarity"],

            result["weight_summary"]["difference_percentage"]

        ]

    }

# =========================================================
# Generate All Charts
# =========================================================

def generate_chart_data(result, analytics):

    return {

        "similarity_chart": generate_similarity_chart(analytics),

        "risk_chart": generate_risk_chart(analytics),

        "priority_chart": generate_priority_chart(result["weight_summary"]),

        "dashboard_chart": generate_dashboard_chart(result)

    }