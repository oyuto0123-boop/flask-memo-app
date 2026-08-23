import sqlite3

DATABASE = "memo.db"


def get_connection():
    """データベースへの接続を取得する"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """データベースを初期化する（テーブルを作成する）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 追加：既存DBにcategory列がなければ追加する（マイグレーション）
    # 既にcategory列がある場合はエラーになるのでtry/exceptで無視する
    try:
        cursor.execute("ALTER TABLE memos ADD COLUMN category TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass  # 既に列が存在する場合はスキップ

    conn.commit()
    conn.close()


def get_all_memos(q=None, category=None, sort="updated_at"):
    """
    全てのメモを取得する
    q: タイトルまたは本文の検索キーワード（省略可）
    category: カテゴリで絞り込み（省略可）
    sort: 並び順 "created_at" / "updated_at" / "category"（省略時はupdated_at）
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 許可された列名のみソートに使う（SQLインジェクション対策）
    allowed_sort = {
        "created_at": "created_at DESC",
        "updated_at": "updated_at DESC",
        "category": "category ASC, updated_at DESC",
    }
    order_clause = allowed_sort.get(sort, "updated_at DESC")

    query = "SELECT * FROM memos WHERE 1=1"
    params = []

    if q:
        query += " AND (title LIKE ? OR body LIKE ?)"
        keyword = f"%{q}%"
        params.extend([keyword, keyword])

    if category:
        query += " AND category = ?"
        params.append(category)

    query += f" ORDER BY {order_clause}"

    cursor.execute(query, params)
    memos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return memos


def get_memo(memo_id):
    """指定されたIDのメモを取得する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memos WHERE id = ?", (memo_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def create_memo(title, body, category=""):
    """新しいメモを作成する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO memos (title, body, category) VALUES (?, ?, ?)",
        (title, body, category)
    )
    conn.commit()
    memo_id = cursor.lastrowid
    conn.close()
    return memo_id


def update_memo(memo_id, title, body, category=""):
    """指定されたIDのメモを更新する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE memos SET title = ?, body = ?, category = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (title, body, category, memo_id)
    )
    conn.commit()
    changes = cursor.rowcount  
    conn.close()
    return changes > 0


def delete_memo(memo_id):
    """指定されたIDのメモを削除する"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memos WHERE id = ?", (memo_id,))
    conn.commit()
    changes = cursor.rowcount
    conn.close()
    return changes > 0