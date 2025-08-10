from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def screenplay_writer(state):
    model = ModelProvider()
    act_number = state.get("act_number", 1)
    act_text = state.get("act_text", "")
    prompt = (
        f"Write a professionally formatted screenplay for **Act {act_number}** of a short Indian film.\n\n"
        f"**Genre:** {state.get('genre', '')}\n"
        f"**Logline:** {state.get('idea', '')}\n"
        f"**Characters:** {state.get('characters', '')}\n\n"
        f"**Act {act_number} Outline:**\n{act_text}\n\n"
        "Follow the standard screenplay structure used in the Indian film industry (inspired by international formats like Final Draft or Celtx):\n"
        "- Number each scene.\n"
        "- Use scene headings (e.g., INT./EXT. – LOCATION – TIME).\n"
        "- Include character names in uppercase above dialogues.\n"
        "- Write dialogue in natural, culturally appropriate Indian tone (can include code-switching or regional influences).\n"
        "- Add action lines and transitions where needed.\n"
        "- Avoid over-description; focus on what can be shown on screen.\n\n"
        "Write in English. Maintain cinematic flow, emotional beats, and strong pacing throughout the act."
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
