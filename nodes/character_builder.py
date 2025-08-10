from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def character_builder(state):
    model = ModelProvider()
    prompt = f"Based on this plot: {state['idea']}, create 3-4 interesting character descriptions."
    characters_text = model.generate(prompt)
    characters = characters_text.split("\n")
    save_to_db(
        script_id=state["session_id"], 
        genre=state["genre"],
        idea=state.get("idea"),
        characters="\n".join(characters)
    )
    return {**state, "characters": characters}
