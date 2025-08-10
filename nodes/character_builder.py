from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def character_builder(state):
    model = ModelProvider()
    prompt = f"Based on the following plot: {state['idea']}, create compelling Indian character profiles as per the idea. Each character should reflect authentic Indian cultural, social, or regional backgrounds (e.g., rural or urban India, specific states or languages, caste/class dynamics, generational perspectives). Include their name, age, gender, background, personality traits, and role in the story. Characters should feel multidimensional and emotionally believable, with motivations that align with the plot. Avoid stereotypes, and aim for richness and realism."
    characters_text = model.generate(prompt)
    characters = characters_text.split("\n")
    save_to_db(
        script_id=state["session_id"], 
        genre=state["genre"],
        idea=state.get("idea"),
        characters="\n".join(characters)
    )
    return {**state, "characters": characters}
