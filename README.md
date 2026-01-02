{
  "mcpServers": {
    "memos-local": {
      "autoApprove": [
        "create_memo"
      ],
      "disabled": false,
      "timeout": 60,
      "type": "stdio",
      "command": "F:/PROJECTS/.venv/scripts/python",
      "args": [
        "F:/PROJECTS/main.py"
      ],
      "env": {
        "MEMOS_URL": "memos url",
        "MEMOS_TOKEN": "memos token"
      }
    }
  }
}
