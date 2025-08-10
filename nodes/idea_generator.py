from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def idea_generator(state):
    model = ModelProvider()
    prompt = f"Generate a unique and original film plot idea in 2–3 sentences. The story should be set in India and deeply rooted in Indian culture, traditions, and societal dynamics. The characters must be Indian, with distinct regional, linguistic, or cultural backgrounds. The idea should feel fresh, emotionally engaging, and suitable for a wide Indian audience—blending drama, conflict, or fantasy as needed, while remaining grounded in the Indian context. Genre:  {state['genre']}."
    idea = model.generate(prompt)
    save_to_db(script_id=state["session_id"], genre=state["genre"], idea=idea)
    return {**state, "idea": idea}
