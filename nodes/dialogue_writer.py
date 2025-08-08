from models.model_provider import ModelProvider

def dialogue_writer(state):
    model = ModelProvider()
    prompt = f"Write sample dialogues for one important scene from this outline: {state['outline']}."
    dialogues = model.generate(prompt)
    return {**state, "dialogues": dialogues}
