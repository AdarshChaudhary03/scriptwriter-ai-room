from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def dialogue_writer(state):
    model = ModelProvider()
    prompt = f"Write sample dialogues for one important scene from this outline: {state['outline']}."
    dialogues = model.generate(prompt)
    save_to_db(
        script_id=state["session_id"],
        genre=state["genre"],
        idea=state.get("idea"),
        characters="\n".join(state.get("characters", [])),
        outline="\n".join(state.get("outline", [])),
        dialogues="\n".join(dialogues)
    )
    return {**state, "dialogues": dialogues}
