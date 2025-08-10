from data.db_utils import save_to_db
from models.model_provider import ModelProvider

def script_outliner(state):
    model = ModelProvider()
    prompt = (
        f"Create a structured short film outline based on the following:\n"
        f"Plot: {state['idea']}\n"
        f"Characters: {state['characters']}\n"
        "\n"
        "Format the outline as follows:\n"
        "Logline: <one-sentence summary>\n"
        "\n"
        "Act 1: (Beginning)\n"
        "- <bullet point for each major event, as many as needed>\n"
        "\n"
        "Act 2: (Middle)\n"
        "- <bullet point for each major event, as many as needed>\n"
        "\n"
        "Act 3: (End)\n"
        "- <bullet point for each major event, as many as needed>\n"
        "\n"
        "Ending Note: <wrap up the story in 1-2 sentences>\n"
    )
    outline = model.generate(prompt)
    save_to_db(
        script_id=state["session_id"],
        genre=state["genre"],
        idea=state.get("idea"),
        characters="\n".join(state.get("characters", [])),
        outline="\n".join(outline)
    )
    return {**state, "outline": outline}
