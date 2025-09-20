from db.db_connection import get_connection

def fetch_recipients():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM recipient")
        results = cursor.fetchall()
        return [row[0] for row in results]
    except Exception as e:
        print(f"[ERROR] Fetching recipients failed: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
