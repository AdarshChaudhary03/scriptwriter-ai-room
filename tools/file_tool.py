def save_script_tool(script_text, filename="final_script.txt"):
    """Save the generated script to a file"""
    os.makedirs("scripts", exist_ok=True)
    filepath = os.path.join("scripts", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(script_text)
    return f"Script saved to {filepath}"