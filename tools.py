# tools.py
from duckduckgo_search import DDGS
import os

def web_search_tool(query, max_results=3):
    """Simple DuckDuckGo search tool"""
    with DDGS() as ddgs:
        results = [r["body"] for r in ddgs.text(query, max_results=max_results)]
    return "\n".join(results)

def save_script_tool(script_text, filename):
    """Save the generated script to a file"""
    os.makedirs("scripts", exist_ok=True)
    filepath = os.path.join("scripts", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(script_text)
    return f"Script saved to {filepath}"
