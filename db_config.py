import os
import sqlite3
import pandas as pd
from datetime import date, datetime

def init_db():
    db_file = "tips.db"
    first_run = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file, check_same_thread=False)

    if first_run:
        with conn:
            conn.execute("""
                CREATE TABLE staffs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
            """)
            conn.execute("""
                CREATE TABLE tips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    staff_id INTEGER NOT NULL,
                    tip_amount REAL NOT NULL,
                    tip_date DATE NOT NULL,
                    FOREIGN KEY (staff_id) REFERENCES staffs(id)
                );
            """)
            # Seed some staff
            conn.executemany("INSERT INTO staffs (name) VALUES (?)", [
                ("Chi Hai",), ("Hana",), ("Pi",), ("Wendy",), ("Vee",), ("Tina",), ("Hai",)
            ])
    return conn

def get_staff_list(conn):
    df = pd.read_sql("SELECT name FROM staffs ORDER BY name", conn)
    return df['name'].tolist()

def get_staff_id(conn, name):
    cur = conn.execute("SELECT id FROM staffs WHERE name = ?", (name,))
    row = cur.fetchone()
    return row[0] if row else None

def add_tip(conn, staff_name, tip_amount, tip_date):
    staff_id = get_staff_id(conn, staff_name)
    if staff_id:
        with conn:
            conn.execute("INSERT INTO tips (staff_id, tip_amount, tip_date) VALUES (?, ?, ?)",
                         (staff_id, tip_amount, tip_date))

def get_statistics_by_range(conn, start_date, end_date):
    query = """
        SELECT s.name AS 'Tên Nhân Viên', SUM(t.tip_amount) AS 'Tổng Tiền Tip'
        FROM tips t
        JOIN staffs s ON t.staff_id = s.id
        WHERE tip_date BETWEEN ? AND ?
        GROUP BY s.name
        ORDER BY s.name
    """
    return pd.read_sql_query(query, conn, params=(start_date, end_date))

def get_statistics_by_period(conn, period):
    if period == "ngày":
        group_expr = "strftime('%Y-%m-%d', tip_date)"
    elif period == "tuần":
        group_expr = "strftime('%Y-W%W', tip_date)"
    elif period == "tháng":
        group_expr = "strftime('%Y-%m', tip_date)"
    else:
        return pd.DataFrame()

    query = f"""
        SELECT s.name AS staff_name, {group_expr} AS time, SUM(t.tip_amount) AS total
        FROM tips t
        JOIN staffs s ON t.staff_id = s.id
        GROUP BY s.name, time
        ORDER BY time
    """
    return pd.read_sql_query(query, conn)
