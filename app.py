from flask import Flask, jsonify, request, send_from_directory
from database import init_db, get_all_memos, get_memo, create_memo, update_memo, delete_memo

app = Flask(__name__)

# アプリ起動時にDBを初期化
init_db()

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/memos", methods=["GET"])
def api_get_memos():
    """全てのメモを取得する（検索・カテゴリ絞り込み・ソート対応）"""
    # 追加：クエリパラメータから検索キーワード・カテゴリ・並び順を取得
    # 例: /api/memos?q=買い物&category=仕事&sort=created_at
    q = request.args.get("q")
    category = request.args.get("category")
    sort = request.args.get("sort", "updated_at")

    memos = get_all_memos(q=q, category=category, sort=sort)
    return jsonify(memos)


@app.route("/api/memos", methods=["POST"])
def api_create_memo():
    """新しいメモを作成する"""
    data = request.get_json(silent=True)  # JSONが空の場合にエラーを出さないようにする

    if not data:
        return jsonify({"error": "リクエストボディが空です"}), 400

    title = data.get("title")
    body = data.get("body")
    category = data.get("category", "")  # 追加：カテゴリは任意項目（未指定なら空文字）

    if not isinstance(title, str) or not isinstance(body, str) or not title.strip() or not body.strip():
        return jsonify({"error": "title と body は必須です"}), 400

    memo_id = create_memo(title, body, category)
    memo = get_memo(memo_id)
    return jsonify(memo), 201


@app.route("/api/memos/<int:id>", methods=["GET"])
def api_get_memo(id):
    """指定されたIDのメモを取得する"""
    memo = get_memo(id)

    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404

    return jsonify(memo)


@app.route("/api/memos/<int:id>", methods=["PUT"])
def api_update_memo(id):
    """指定されたIDのメモを更新する"""
    memo = get_memo(id)
    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404

    data = request.get_json(silent=True)  # JSONが空の場合にエラーを出さないようにする

    if not data:
        return jsonify({"error": "リクエストボディが空です"}), 400

    title = data.get("title")
    body = data.get("body")
    category = data.get("category", "")  # 追加：カテゴリは任意項目（未指定なら空文字）

    if not isinstance(title, str) or not isinstance(body, str) or not title.strip() or not body.strip():
        return jsonify({"error": "title と body は必須です"}), 400

    update_memo(id, title, body, category)
    updated_memo = get_memo(id)
    return jsonify(updated_memo)


@app.route("/api/memos/<int:id>", methods=["DELETE"])
def api_delete_memo(id):
    """指定されたIDのメモを削除する"""
    memo = get_memo(id)
    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404

    delete_memo(id)
    return jsonify({"message": f"メモ (ID:{id}) を削除しました"})


if __name__ == "__main__":
    app.run(debug=True)

#if __name__ == "__main__":
 #   app.run(debug=True, host="0.0.0.0")