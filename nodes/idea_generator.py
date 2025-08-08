
from models.model_provider import ModelProvider

def idea_generator(state):
    model = ModelProvider()
    prompt = f"Generate a unique film plot idea in 2-3 sentences. Genre:  {state['genre']}."
    idea = model.generate(prompt)
    return {**state, "idea": idea}
