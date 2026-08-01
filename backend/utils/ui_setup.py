"""
=========================================
TenderIQ UI Setup
-----------------------------------------
Contains helper functions for UI display.

Used by:
- compare_routes.py
- dashboard_routes.py
- history_routes.py
=========================================
"""

# =========================================
# Risk Badge
# =========================================

def get_risk_badge(level):
    """
    Returns Bootstrap badge color according to risk level.
    """

    colors = {

        "Critical": "danger",

        "High": "warning",

        "Medium": "info",

        "Low": "success"

    }

    return colors.get(level, "secondary")

# =========================================
# Risk Icon
# =========================================

def get_risk_icon(level):
    """
    Returns emoji for risk level.
    """

    icons = {

        "Critical": "🔴",

        "High": "🟠",

        "Medium": "🟡",

        "Low": "🟢"

    }

    return icons.get(level, "⚪")