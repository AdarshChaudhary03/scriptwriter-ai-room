from models.model_provider import ModelProvider

def script_outliner(state):
    model = ModelProvider()
    prompt = f"Create a short film outline based on plot: {state['idea']} and characters: {state['characters']}."
    outline = model.generate(prompt)
    return {**state, "outline": outline}
