"""
=========================================================
TenderIQ History Service
---------------------------------------------------------
Responsible for

1. User Comparison History
2. Individual Report Retrieval
3. History Search
4. Delete History
5. Recent History
6. Dashboard History
7. History Statistics
=========================================================
"""

from backend.utils.db import get_connection

# =========================================================
# Get User History
# =========================================================

def get_user_history(user_id):
    """
    Returns all comparison history of a user.

    Parameters
    ----------
    user_id : int

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
            
            id,

            tender1_id,

            tender2_id,

            similarity_score,

            match_level,

            created_at

        FROM comparison_reports

        WHERE user_id = %s

        ORDER BY created_at DESC
        """

        cursor.execute(query, (user_id,))

        history = cursor.fetchall()

        return history

    except Exception as e:

        print(f"[History Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Get History By ID
# =========================================================

def get_history_by_id(report_id, user_id):
    """
    Returns one comparison report.

    Parameters
    ----------
    report_id : int

    user_id : int

    Returns
    -------
    dict | None
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
        
            id,

            user_id,

            tender1_id,

            tender2_id,

            similarity_score,

            match_level,

            analysis_report,

            created_at

        FROM comparison_reports

        WHERE id = %s

        AND user_id = %s
        """

        cursor.execute(query,(report_id,user_id))
                
        report = cursor.fetchone()

        return report

    except Exception as e:

        print(f"[History Service] {e}")

        return None

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Search History
# =========================================================

def search_history(user_id, keyword):
    """
    Search comparison history by
    tender names or match level.

    Parameters
    ----------
    user_id : int

    keyword : str

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

            cr.id,

            t1.tender_name AS tender1,

            t2.tender_name AS tender2,

            cr.similarity_score,

            cr.match_level,

            cr.created_at

        FROM comparison_reports cr

        INNER JOIN tenders t1
            ON cr.tender1_id = t1.id

        INNER JOIN tenders t2
            ON cr.tender2_id = t2.id

        WHERE

            cr.user_id = %s

        AND

        (

            t1.tender_name LIKE %s

            OR

            t2.tender_name LIKE %s

            OR

            cr.match_level LIKE %s

        )

        ORDER BY cr.created_at DESC
        """

        search = f"%{keyword}%"

        cursor.execute(query,(user_id,search,search,search))

        results = cursor.fetchall()

        return results

    except Exception as e:

        print(f"[History Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Delete History
# =========================================================

def delete_history(report_id, user_id):
    """
    Delete one comparison report.

    Parameters
    ----------
    report_id : int

    user_id : int

    Returns
    -------
    bool
    """

    conn = None

    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        DELETE FROM comparison_reports

        WHERE

            id = %s

        AND

            user_id = %s
        """

        cursor.execute(query,(report_id,user_id))

        conn.commit()

        return cursor.rowcount > 0

    except Exception as e:

        print(f"[History Service] {e}")

        return False

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Get Recent History
# =========================================================

def get_recent_history(user_id, limit=5):
    """
    Returns the most recent comparison reports.

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
        SELECT

            cr.id,

            t1.tender_name AS tender1,

            t2.tender_name AS tender2,

            cr.similarity_score,

            cr.match_level,

            cr.created_at

        FROM comparison_reports cr

        INNER JOIN tenders t1
            ON cr.tender1_id = t1.id

        INNER JOIN tenders t2
            ON cr.tender2_id = t2.id

        WHERE cr.user_id = %s

        ORDER BY cr.created_at DESC

        LIMIT %s
        """

        cursor.execute(query, (user_id, limit))

        history = cursor.fetchall()

        return history

    except Exception as e:

        print(f"[History Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Dashboard History
# =========================================================

def get_dashboard_history(user_id):
    """
    Returns dashboard history statistics.

    Parameters
    ----------
    user_id : int

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
        SELECT

            COUNT(*) AS total_comparisons,

            ROUND(AVG(similarity_score),2)
                AS average_similarity,

            MAX(similarity_score)
                AS highest_similarity,

            MIN(similarity_score)
                AS lowest_similarity

        FROM comparison_reports

        WHERE user_id=%s
        """

        cursor.execute(query, (user_id,))

        dashboard = cursor.fetchone()

        return dashboard

    except Exception as e:

        print(f"[History Service] {e}")

        return {

            "total_comparisons": 0,

            "average_similarity": 0,

            "highest_similarity": 0,

            "lowest_similarity": 0

        }

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# History Statistics
# =========================================================

def history_statistics(user_id):
    """
    Complete history statistics.

    Parameters
    ----------
    user_id : int

    Returns
    -------
    dict
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        # ------------------------------------
        # Match Level Distribution
        # ------------------------------------

        cursor.execute(
            """
            SELECT

                match_level,

                COUNT(*) AS total

            FROM comparison_reports

            WHERE user_id=%s

            GROUP BY match_level
            """,
            (user_id,)
        )

        match_distribution = cursor.fetchall()

        # ------------------------------------
        # Monthly Statistics
        # ------------------------------------

        cursor.execute(
            """
            SELECT

                DATE_FORMAT(created_at,'%Y-%m') AS month,

                COUNT(*) AS comparisons,

                ROUND(AVG(similarity_score),2)
                    AS average_similarity

            FROM comparison_reports

            WHERE user_id=%s

            GROUP BY DATE_FORMAT(created_at,'%Y-%m')

            ORDER BY month DESC
            """,
            (user_id,)
        )

        monthly_statistics = cursor.fetchall()

        # ------------------------------------
        # Dashboard Summary
        # ------------------------------------

        dashboard = get_dashboard_history(user_id)

        return {

            "dashboard": dashboard,

            "match_distribution": match_distribution,

            "monthly_statistics": monthly_statistics

        }

    except Exception as e:

        print(f"[History Service] {e}")

        return {

            "dashboard": {},

            "match_distribution": [],

            "monthly_statistics": []

        }

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()