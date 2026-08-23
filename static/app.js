// --- DOM要素の取得 ---
const memoForm = document.getElementById("memo-form");
const memoTitle = document.getElementById("memo-title");
const memoBody = document.getElementById("memo-body");
const memoCategory = document.getElementById("memo-category"); // 追加
const memoId = document.getElementById("memo-id");
const memoList = document.getElementById("memo-list");
const btnCreate = document.getElementById("btn-create");
const btnUpdate = document.getElementById("btn-update");
const btnDelete = document.getElementById("btn-delete");
const btnCancel = document.getElementById("btn-cancel");
const searchInput = document.getElementById("search-input"); // 追加
const sortSelect = document.getElementById("sort-select");   // 追加


// --- メモ一覧を読み込む ---
async function fetchMemos() {
    // 追加：検索キーワードとソート順をクエリパラメータとして付与
    const params = new URLSearchParams();
    const q = searchInput.value.trim();
    if (q) {
        params.set("q", q);
    }
    params.set("sort", sortSelect.value);

    const response = await fetch("/api/memos?" + params.toString());
    const memos = await response.json();

    // メモ一覧エリアの削除
    memoList.innerHTML = "";

    if (memos.length === 0) {
        memoList.innerHTML = '<p class="empty-message">メモがまだありません。作成しましょう。</p>';
        return;
    }

    // 各メモをカード表示
    memos.forEach(function (memo) {
        const card = document.createElement("div");
        card.className = "memo-card";

        // 修正：innerHTMLでの文字列結合をやめ、要素を組み立てる（XSS対策）
        const titleEl = document.createElement("h3");
        titleEl.textContent = memo.title;

        const bodyEl = document.createElement("p");
        bodyEl.textContent = memo.body;

        const dateEl = document.createElement("span");
        dateEl.className = "memo-date";
        // 追加：カテゴリがあれば日付の前に表示
        const categoryText = memo.category ? "［" + memo.category + "］ " : "";
        dateEl.textContent = categoryText + "更新: " + memo.updated_at;

        card.appendChild(titleEl);
        card.appendChild(bodyEl);
        card.appendChild(dateEl);

        // クリックでメモを選択
        card.addEventListener("click", function () {
            selectMemo(memo);
            // 選択中のカードのスタイルを変更
            document.querySelectorAll(".memo-card").forEach(function (c) {
                c.classList.remove("selected");
            });
            card.classList.add("selected");
        });

        memoList.appendChild(card);
    });
}


// --- メモを作成する ---
async function createMemo() {
    const title = memoTitle.value.trim();
    const body = memoBody.value.trim();
    const category = memoCategory.value.trim(); // 追加

    if (!title || !body) {
        alert("タイトルと本文を入力してください。");
        return;
    }

    await fetch("/api/memos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: title, body: body, category: category }), // 修正：category追加
    });

    resetForm();
    fetchMemos();
}


// --- メモを選択する ---
function selectMemo(memo) {
    memoId.value = memo.id;
    memoTitle.value = memo.title;
    memoBody.value = memo.body;
    memoCategory.value = memo.category || ""; // 追加

    // ボタンの状態を変更
    btnCreate.disabled = true;
    btnUpdate.disabled = false;
    btnDelete.disabled = false;
}


// --- メモを更新する ---
async function updateMemo() {
    const id = memoId.value;
    const title = memoTitle.value.trim();
    const body = memoBody.value.trim();
    const category = memoCategory.value.trim(); // 追加

    if (!title || !body) {
        alert("タイトルと本文を入力してください。");
        return;
    }

    await fetch("/api/memos/" + id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: title, body: body, category: category }), // 修正：category追加
    });

    resetForm();
    fetchMemos();
}


// --- メモを削除する ---
async function deleteMemo() {
    const id = memoId.value;

    if (!confirm("このメモを削除してもよいですか？")) {
        return;
    }

    await fetch("/api/memos/" + id, {
        method: "DELETE",
    });

    resetForm();
    fetchMemos();
}


// --- フォームをリセットする ---
function resetForm() {
    memoId.value = "";
    memoTitle.value = "";
    memoBody.value = "";
    memoCategory.value = ""; // 追加

    // ボタンの状態をリセット
    btnCreate.disabled = false;
    btnUpdate.disabled = true;
    btnDelete.disabled = true;

    // 選択中をリセット
    document.querySelectorAll(".memo-card").forEach(function (c) {
        c.classList.remove("selected");
    });
}


// --- イベントリスナーの登録 ---

// フォームの送信
memoForm.addEventListener("submit", function (e) {
    e.preventDefault();
    createMemo();
});

// 更新
btnUpdate.addEventListener("click", updateMemo);
// 削除
btnDelete.addEventListener("click", deleteMemo);
// キャンセル
btnCancel.addEventListener("click", resetForm);

// 追加：検索入力のたびに一覧を再取得
searchInput.addEventListener("input", fetchMemos);
// 追加：ソート順変更時に一覧を再取得
sortSelect.addEventListener("change", fetchMemos);

// ページ読み込み時にメモ一覧を取得
fetchMemos();