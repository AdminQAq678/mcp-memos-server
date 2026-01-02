import os
import httpx
from fastmcp import FastMCP

# 初始化 MCP 服务
mcp = FastMCP("Memos-Manager")

# 环境变量配置
MEMOS_URL = os.getenv("MEMOS_URL", "").rstrip("/")
MEMOS_TOKEN = os.getenv("MEMOS_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {MEMOS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Memos-MCP-Server/1.0",
}


# --- 新增：定义一个空的 Resource 列表，防止 Claude 探测报错 ---
@mcp.resource("memos://recent")
async def get_memos_resource() -> str:
    """以资源形式返回最近的笔记"""
    return await get_recent_memos(limit=10)


# --- 核心工具 ---
@mcp.tool()
async def create_memo(content: str, visibility: str = "PRIVATE") -> str:
    """
    在 Memos 中创建一条新笔记。
    """
    url = f"{MEMOS_URL}/api/v1/memos"
    payload = {"content": content, "visibility": visibility.upper()}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(url, json=payload, headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                memo_id = data.get("name") or data.get("id")
                return f"✅ 成功存入 Memos！ID: {memo_id}"
            return f"❌ 失败: {response.status_code}"
        except Exception as e:
            return f"⚠️ 错误: {str(e)}"


@mcp.tool()
async def get_recent_memos(limit: int = 5) -> str:
    """获取最近创建的笔记列表。"""
    url = f"{MEMOS_URL}/api/v1/memos"
    params = {"limit": limit}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params, headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                memos = data.get("memos") if isinstance(data, dict) else data
                if not memos:
                    return "没有找到笔记。"

                results = [
                    f"- [{m.get('name') or m.get('id')}]: {m.get('content')[:100]}"
                    for m in memos
                ]
                return "\n".join(results)
            return f"❌ 获取失败"
        except Exception as e:
            return f"⚠️ 错误"


if __name__ == "__main__":
    mcp.run(transport="stdio")
