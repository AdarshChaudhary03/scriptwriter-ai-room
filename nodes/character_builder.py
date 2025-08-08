from models.model_provider import ModelProvider

def character_builder(state):
    model = ModelProvider()
    prompt = f"Based on this plot: {state['idea']}, create 3-4 interesting character descriptions."
    characters_text = model.generate(prompt)
    characters = characters_text.split("\n")
    return {**state, "characters": characters}
