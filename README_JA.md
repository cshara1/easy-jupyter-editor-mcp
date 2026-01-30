# Easy Jupyter Editor MCP

A lightweight Model Context Protocol (MCP) server designed to allow AI Agents to safely and structurally edit Jupyter Notebook (`.ipynb`) files.

## 開発の経緯 / Background

このMCPサーバーは、AIエージェントが **Jupyter Notebook (.ipynb) を安全に操作するため** に開発されました。

多くのAIエージェント環境（Antigravityなど）では、セキュリティや仕様上の制約により、Notebookファイルを直接実行したり、複雑なJSON構造を持つ `.ipynb` ファイルをテキストとして直接編集することが困難な場合があります（JSON形式を破損させるリスクがあるため）。

このプロジェクトは、**「Notebookの実行権限を回避しつつ、ファイルとしてのNotebookを構造的に正しく編集する」** ことを目的としています。`nbformat` ライブラリを使用することで、JSON構造を壊さずにセルの追加・編集・削除を行うことができます。

## 機能 / Features

以下のツールを提供します：
*   **`read_notebook`**: Notebookのセル一覧（インデックスと内容）を取得します。
*   **`get_cell`**: 指定したインデックスのセルの完全なソースコードを取得します。
*   **`edit_cell`**: 指定したセルの内容を書き換えます。
*   **`add_cell`**: コードまたはMarkdownセルを新規追加します。
*   **`delete_cell`**: 指定したセルを削除します。
*   **`create_notebook`**: 新しい空のNotebookを作成します。

## インストールと使い方 / Installation & Usage

このサーバーは [uv](https://github.com/astral-sh/uv) を使用して実行することを推奨します。

### 1. Claude Desktop / MCP Client 設定

`claude_desktop_config.json` に以下のように設定を追加してください。

#### GitHubから直接実行する場合 (推奨)
```json
{
  "mcpServers": {
    "easy-jupyter-editor": {
      "command": "uv",
      "args": [
        "run",
        "--from",
        "git+https://github.com/YourUsername/easy-jupyter-editor-mcp",
        "easy-jupyter-editor-mcp"
      ]
    }
  }
}
```

#### ローカルで開発・テストする場合
```json
{
  "mcpServers": {
    "easy-jupyter-editor": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "nbformat",
        "python",
        "/absolute/path/to/easy-jupyter-editor-mcp/src/easy_jupyter_editor_mcp/__init__.py"
      ]
    }
  }
}
```

### 2. PyPI (将来的な公開時)

もしPyPIに公開された場合は、以下のように簡潔に記述できます。

```json
{
  "mcpServers": {
    "easy-jupyter-editor": {
      "command": "uvx",
      "args": ["easy-jupyter-editor-mcp"]
    }
  }
}
```

## 開発者向け / Development

```bash
# ビルド
uv build

# PyPIへ公開
uv publish
```
