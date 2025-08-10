from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def screenplay_writer(state):
    model = ModelProvider()
    act_number = state.get("act_number", 1)
    act_text = state.get("act_text", "")
    prompt = (
        f"Write a professional screenplay for Act {act_number} of a short film.\n"
        f"Genre: {state.get('genre', '')}\n"
        f"Logline: {state.get('idea', '')}\n"
        f"Characters: {state.get('characters', '')}\n"
        f"Act {act_number} Outline:\n{act_text}\n"
        "\n"
        "Format the screenplay as per industry standards, with multiple scenes, scene headings (INT./EXT., LOCATION - TIME), character names, dialogue, and action lines.\n"
        "Use proper screenplay formatting. Number the scenes.\n"
    )
    screenplay = model.generate(prompt)
    save_to_db(
        script_id=state["session_id"],
        genre=state["genre"],
        idea=state.get("idea"),
        characters="\n".join(state.get("characters", [])) if isinstance(state.get("characters"), list) else state.get("characters", ""),
        outline=state.get("outline", ""),
        screenplay="\n".join(screenplay) if isinstance(screenplay, list) else screenplay
    )
    return {**state, "screenplay": screenplay}
