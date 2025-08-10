from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def idea_generator(state):
    model = ModelProvider()
    prompt = f"Generate a unique film plot idea in 2-3 sentences. Genre:  {state['genre']}."
    idea = model.generate(prompt)
    save_to_db(script_id=state["session_id"], genre=state["genre"], idea=idea)
    return {**state, "idea": idea}
