from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def script_outliner(state):
    model = ModelProvider()
    prompt = f"Create a short film outline based on plot: {state['idea']} and characters: {state['characters']}."
    outline = model.generate(prompt)
    save_to_db(
        script_id=state["session_id"], 
        genre=state["genre"],
        idea=state.get("idea"),
        characters="\n".join(state.get("characters", [])),
        outline="\n".join(outline)
    )
    return {**state, "outline": outline}
