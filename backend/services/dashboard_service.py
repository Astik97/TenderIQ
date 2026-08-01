"""
=========================================================
TenderIQ Dashboard Service
---------------------------------------------------------
Responsible for

1. Dashboard Statistics
2. Tender Statistics
3. Comparison Statistics
4. Similarity Statistics
=========================================================
"""

from scipy import stats
from backend.utils.db import get_connection

# =========================================================
# Total Uploaded Tenders
# =========================================================

def get_total_tenders(user_id):
    """
    Returns the total number of uploaded tenders
    for the current user.

    Parameters
    ----------
    user_id : int

    Returns
    -------
    int
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM tenders
        WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()[0]

        return result if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Total Comparisons
# =========================================================

def get_total_comparisons(user_id):
    """
    Returns the total number of comparisons
    performed by the user.

    Parameters
    ----------
    user_id : int

    Returns
    -------
    int
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM comparison_reports
        WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()[0]

        return result if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Similarity Statistics
# =========================================================

def get_similarity_statistics(user_id):
    """
    Returns detailed similarity statistics.

    Returns
    -------
    dict
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT COUNT(*) AS total_comparisons,

            ROUND(AVG(similarity_score),2)
                AS average_similarity,

            ROUND(MAX(similarity_score),2)
                AS highest_similarity,

            ROUND(MIN(similarity_score),2)
                AS lowest_similarity

        FROM comparison_reports

        WHERE user_id=%s
        """

        cursor.execute(query, (user_id,))

        stats = cursor.fetchone()

        if not stats:

            return {

                "total_comparisons": 0,

                "average_similarity": 0,

                "highest_similarity": 0,

                "lowest_similarity": 0,

                "similarity_range": 0

            }

        stats["average_similarity"] = stats["average_similarity"] or 0

        stats["highest_similarity"] = stats["highest_similarity"] or 0

        stats["lowest_similarity"] = stats["lowest_similarity"] or 0

        stats["similarity_range"] = round(
            stats["highest_similarity"] - 
            stats["lowest_similarity"],
            2)

        return stats

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return {

            "total_comparisons": 0,

            "average_similarity": 0,

            "highest_similarity": 0,

            "lowest_similarity": 0,

            "similarity_range": 0

        }

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Total Excellent Matches
# =========================================================

def get_total_excellent_matches(user_id):
    """
    Returns total Excellent Matches.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM comparison_reports
        WHERE user_id=%s
        AND match_level='Excellent Match'
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Total Good Matches
# =========================================================

def get_total_good_matches(user_id):
    """
    Returns total Good Matches.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM comparison_reports
        WHERE user_id=%s
        AND match_level='Good Match'
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Total Moderate Matches
# =========================================================

def get_total_moderate_matches(user_id):
    """
    Returns total Moderate Matches.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM comparison_reports
        WHERE user_id=%s
        AND match_level='Moderate Match'
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()[0]

        return result if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Total Poor Matches
# =========================================================

def get_total_poor_matches(user_id):
    """
    Returns total Poor Matches.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM comparison_reports
        WHERE user_id=%s
        AND match_level='Poor Match'
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Total High Risk Reports
# =========================================================

def get_total_high_risk_reports(user_id):
    """
    Returns comparisons having
    High Risk similarity (30-49%).
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM comparison_reports
        WHERE user_id=%s
        AND similarity_score >= 30
        AND similarity_score < 50
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Total Critical Risk Reports
# =========================================================

def get_total_critical_risk_reports(user_id):
    """
    Returns comparisons having
    Critical Risk similarity (<30%).
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM comparison_reports
        WHERE user_id=%s
        AND similarity_score < 30
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return 0

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()                      

# =========================================================
# Recent Uploaded Tenders
# =========================================================

def get_recent_tenders(user_id, limit=5):
    """
    Returns recently uploaded tenders.

    Parameters
    ----------
    user_id : int

    limit : int

    Returns
    -------
    list
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id,
        tender_name,
        upload_date
        FROM tenders
        WHERE user_id = %s
        ORDER BY upload_date DESC LIMIT %s
        """

        cursor.execute(query,(user_id,limit))

        tenders = cursor.fetchall()

        return tenders

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Recent Comparisons
# =========================================================

def get_recent_comparisons(user_id, limit=5):
    """
    Returns recent comparison reports.

    Parameters
    ----------
    user_id : int

    limit : int

    Returns
    -------
    list
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT cr.id,
        t1.tender_name AS tender1,
        t2.tender_name AS tender2,
        cr.similarity_score,
        cr.match_level,
        cr.created_at
        FROM comparison_reports cr
        INNER JOIN tenders t1 ON cr.tender1_id = t1.id
        INNER JOIN tenders t2 ON cr.tender2_id = t2.id
        WHERE cr.user_id = %s
        ORDER BY cr.created_at DESC LIMIT %s
        """

        cursor.execute(query,(user_id,limit))

        comparisons = cursor.fetchall()

        return comparisons

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Monthly Statistics
# =========================================================

def get_monthly_statistics(user_id):
    """
    Returns monthly comparison statistics.

    Returns
    -------
    list
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT

            DATE_FORMAT(created_at,'%Y-%m') AS month,

            COUNT(*) AS total_comparisons,

            ROUND(AVG(similarity_score),2)
                AS average_similarity,

            ROUND(MAX(similarity_score),2)
                AS highest_similarity,

            ROUND(MIN(similarity_score),2)
                AS lowest_similarity

        FROM comparison_reports

        WHERE user_id=%s

        GROUP BY DATE_FORMAT(created_at,'%Y-%m')

        ORDER BY month DESC
        """

        cursor.execute(query, (user_id,))

        monthly = cursor.fetchall()

        for row in monthly:

            row["average_similarity"] = row["average_similarity"] or 0

            row["highest_similarity"] = row["highest_similarity"] or 0

            row["lowest_similarity"] = row["lowest_similarity"] or 0

            row["similarity_range"] = round(
                row["highest_similarity"] - 
                row["lowest_similarity"],
                2)

        return monthly

    except Exception as e:

        print(f"[Dashboard Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Dashboard Summary
# =========================================================

def generate_dashboard_summary(user_id):
    """
    Generates the complete dashboard summary.

    Parameters
    ----------
    user_id : int

    Returns
    -------
    dict
    """

    # ----------------------------------
    # Basic Statistics
    # ----------------------------------

    total_tenders = get_total_tenders(user_id)

    total_comparisons = get_total_comparisons(user_id)

    # ----------------------------------
    # Similarity Statistics
    # ----------------------------------

    similarity_statistics = get_similarity_statistics(user_id)

    average = similarity_statistics["average_similarity"]

    # ----------------------------------
    # Match Statistics
    # ----------------------------------

    excellent_matches = get_total_excellent_matches(user_id)

    good_matches = get_total_good_matches(user_id)

    moderate_matches = get_total_moderate_matches(user_id)

    poor_matches = get_total_poor_matches(user_id)

    # ----------------------------------
    # Recent Activity
    # ----------------------------------

    recent_tenders = get_recent_tenders(user_id)

    recent_comparisons = get_recent_comparisons(user_id)

    # ----------------------------------
    # Monthly Statistics
    # ----------------------------------

    monthly_statistics = get_monthly_statistics(user_id)

    # ----------------------------------
    # Risk Statistics
    # ----------------------------------

    high_risk_reports = get_total_high_risk_reports(user_id)

    critical_risk_reports = get_total_critical_risk_reports(user_id)

    # ----------------------------------
    # Dashboard Summary
    # ----------------------------------

    return {

        # Basic Statistics

        "total_tenders": total_tenders,

        "total_comparisons": total_comparisons,

        # Similarity Statistics

        "similarity_statistics": similarity_statistics,

        # Match Statistics

        "excellent_matches": excellent_matches,

        "good_matches": good_matches,

        "moderate_matches": moderate_matches,

        "poor_matches": poor_matches,

        # Recent Activity

        "recent_tenders": recent_tenders,

        "recent_comparisons": recent_comparisons,

        # Monthly Statistics

        "monthly_statistics": monthly_statistics,

        # Risk Statistics

        "high_risk_reports": high_risk_reports,

        "critical_risk_reports": critical_risk_reports

    }