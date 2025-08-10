from data.db_utils import init_db
import gradio as gr
from langgraph.graph import StateGraph, START, END
from state.states import ScriptState
from nodes.idea_generator import idea_generator
from nodes.character_builder import character_builder
from nodes.script_outliner import script_outliner
from nodes.screenplay_writer import screenplay_writer
from tools import save_script_tool
from langgraph.checkpoint.memory import MemorySaver


# -----------------
# Stepwise Script Generation Functions
# -----------------
session_id = "session_001"

memory = MemorySaver()

# --- Act-by-Act Screenplay Generation ---
def get_act_from_outline(outline, act_number):
    """Extracts the text for the specified act from the outline string."""
    import re
    pattern = rf"Act {act_number}:.*?(?=\nAct|\nEnding Note:|$)"
    match = re.search(pattern, outline, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return ""

def run_screenplay_writer(genre, idea, characters, outline, act_number):
    act_text = get_act_from_outline(outline, act_number)
    if not act_text:
        return f"Act {act_number} not found in outline."
    state = {
        "genre": genre,
        "idea": idea,
        "characters": characters,
        "outline": outline,
        "act_number": act_number,
        "act_text": act_text,
        "session_id": session_id
    }
    result = screenplay_writer(state)
    screenplay = result.get("screenplay") if isinstance(result, dict) and "screenplay" in result else result
    return screenplay if screenplay else str(result)

def run_idea_generator(genre):
    init_db()
    state = {"genre": genre, "session_id": session_id}
    result = idea_generator(state)
    return result["idea"] if isinstance(result, dict) else result

def run_character_builder(genre, idea):
    state = {"genre": genre, "idea": idea, "session_id": session_id}
    result = character_builder(state)
    chars = result["characters"] if isinstance(result, dict) else result
    if isinstance(chars, list):
        return "\n".join(chars)
    return str(chars)

def run_script_outliner(genre, idea, characters):
    state = {"genre": genre, "idea": idea, "characters": characters, "session_id": session_id}
    result = script_outliner(state)
    outline = result["outline"] if isinstance(result, dict) else result
    if isinstance(outline, list):
        return "\n".join(outline)
    return str(outline)


# --- Act-by-Act Screenplay Generation ---
def get_act_from_outline(outline, act_number):
    """Extracts the text for the specified act from the outline string."""
    import re
    pattern = rf"Act {act_number}:.*?(?=\nAct|\nEnding Note:|$)"
    match = re.search(pattern, outline, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return ""

    act_text = get_act_from_outline(outline, act_number)
    if not act_text:
        return f"Act {act_number} not found in outline."
    state = {
        "genre": genre,
        "idea": idea,
        "characters": characters,
        "outline": outline,
        "act_number": act_number,
        "act_text": act_text,
        "session_id": session_id
    }
    result = screenplay_writer(state)
    screenplay = result.get("screenplay") if isinstance(result, dict) and "screenplay" in result else result
    return screenplay if screenplay else str(result)

def save_all(idea, characters, outline, dialogues):
    save_path1 = save_script_tool(idea, "idea")
    save_path2 = save_script_tool(characters, "characters")
    save_path3 = save_script_tool(outline, "outline")
    save_path4 = save_script_tool(dialogues, "dialogues")
    return f"Idea saved to: {save_path1}\nCharacters saved to: {save_path2}\nOutline saved to: {save_path3}\nDialogues saved to: {save_path4}"


# -----------------
# Gradio Stepwise UI
# -----------------
with gr.Blocks(title="AI Script Generator") as demo:
    gr.Markdown("# 🎬 AI Script Generator")
    gr.Markdown("Step-by-step script creation. Enter a genre, then proceed through each stage.")

    genre_state = gr.State("")
    idea_state = gr.State("")
    characters_state = gr.State("")
    outline_state = gr.State("")
    act1_state = gr.State("")
    act2_state = gr.State("")
    act3_state = gr.State("")

    with gr.Row():
        genre_input = gr.Textbox(label="🎭 Genre", placeholder="e.g. Thriller, Romance, Sci-Fi")
        start_btn = gr.Button("Start Idea Generation", variant="primary")

    with gr.Row():
        idea_output = gr.Textbox(label="💡 Plot Idea", lines=4)
    with gr.Row():
        proceed_char_btn = gr.Button("Proceed to Characters", variant="primary")
        regen_idea_btn = gr.Button("Regenerate Idea", variant="secondary")

    with gr.Row():
        characters_output = gr.Textbox(label="🧑‍🤝‍🧑 Characters", lines=6)
    with gr.Row():
        proceed_outline_btn = gr.Button("Proceed to Outline", variant="primary")
        regen_char_btn = gr.Button("Regenerate Characters", variant="secondary")

    with gr.Row():
        outline_output = gr.Textbox(label="🗂 Outline", lines=8)
    with gr.Row():
        proceed_act1_btn = gr.Button("Generate Act 1 Screenplay", variant="primary")
        regen_outline_btn = gr.Button("Regenerate Outline", variant="secondary")

    with gr.Row():
        act1_output = gr.Textbox(label="🎬 Act 1 Screenplay", lines=12)
    with gr.Row():
        proceed_act2_btn = gr.Button("Proceed to Act 2", variant="primary")
        regen_act1_btn = gr.Button("Regenerate Act 1 Screenplay", variant="secondary")

    with gr.Row():
        act2_output = gr.Textbox(label="� Act 2 Screenplay", lines=12)
    with gr.Row():
        proceed_act3_btn = gr.Button("Proceed to Act 3", variant="primary")
        regen_act2_btn = gr.Button("Regenerate Act 2 Screenplay", variant="secondary")

    with gr.Row():
        act3_output = gr.Textbox(label="🎬 Act 3 Screenplay", lines=12)
    with gr.Row():
        save_btn = gr.Button("Save All", variant="primary")
        regen_act3_btn = gr.Button("Regenerate Act 3 Screenplay", variant="secondary")

    with gr.Row():
        save_info = gr.Textbox(label="📂 Saved File Paths", lines=4)

    # Step 1: Idea Generation
    def idea_step(genre):
        idea = run_idea_generator(genre)
        return idea, genre, "", "", ""
    start_btn.click(
        fn=idea_step,
        inputs=[genre_input],
        outputs=[idea_output, genre_state, idea_state, characters_state, outline_state]
    )
    regen_idea_btn.click(
        fn=idea_step,
        inputs=[genre_input],
        outputs=[idea_output, genre_state, idea_state, characters_state, outline_state]
    )

    # Step 2: Character Builder
    def char_step(genre, idea):
        chars = run_character_builder(genre, idea)
        return chars, chars, ""
    proceed_char_btn.click(
        fn=char_step,
        inputs=[genre_state, idea_output],
        outputs=[characters_output, characters_state, outline_state]
    )
    regen_char_btn.click(
        fn=char_step,
        inputs=[genre_state, idea_output],
        outputs=[characters_output, characters_state, outline_state]
    )

    # Step 3: Script Outliner
    def outline_step(genre, idea, characters):
        outline = run_script_outliner(genre, idea, characters)
        return outline, outline
    proceed_outline_btn.click(
        fn=outline_step,
        inputs=[genre_state, idea_output, characters_output],
        outputs=[outline_output, outline_state]
    )
    regen_outline_btn.click(
        fn=outline_step,
        inputs=[genre_state, idea_output, characters_output],
        outputs=[outline_output, outline_state]
    )


    # Step 4: Act 1 Screenplay
    def act1_step(genre, idea, characters, outline):
        act1 = run_screenplay_writer(genre, idea, characters, outline, 1)
        return act1, act1, "", ""
    proceed_act1_btn.click(
        fn=act1_step,
        inputs=[genre_state, idea_output, characters_output, outline_output],
        outputs=[act1_output, act1_state, act2_state, act3_state]
    )
    regen_act1_btn.click(
        fn=act1_step,
        inputs=[genre_state, idea_output, characters_output, outline_output],
        outputs=[act1_output, act1_state, act2_state, act3_state]
    )

    # Step 5: Act 2 Screenplay
    def act2_step(genre, idea, characters, outline):
        act2 = run_screenplay_writer(genre, idea, characters, outline, 2)
        return act2, act2, ""
    proceed_act2_btn.click(
        fn=act2_step,
        inputs=[genre_state, idea_output, characters_output, outline_output],
        outputs=[act2_output, act2_state, act3_state]
    )
    regen_act2_btn.click(
        fn=act2_step,
        inputs=[genre_state, idea_output, characters_output, outline_output],
        outputs=[act2_output, act2_state, act3_state]
    )

    # Step 6: Act 3 Screenplay
    def act3_step(genre, idea, characters, outline):
        act3 = run_screenplay_writer(genre, idea, characters, outline, 3)
        return act3, act3
    proceed_act3_btn.click(
        fn=act3_step,
        inputs=[genre_state, idea_output, characters_output, outline_output],
        outputs=[act3_output, act3_state]
    )
    regen_act3_btn.click(
        fn=act3_step,
        inputs=[genre_state, idea_output, characters_output, outline_output],
        outputs=[act3_output, act3_state]
    )

    # Save All (now saves all acts)
    def save_all_acts(idea, characters, outline, act1, act2, act3):
        save_path1 = save_script_tool(idea, "idea")
        save_path2 = save_script_tool(characters, "characters")
        save_path3 = save_script_tool(outline, "outline")
        save_path4 = save_script_tool(act1, "act1_screenplay")
        save_path5 = save_script_tool(act2, "act2_screenplay")
        save_path6 = save_script_tool(act3, "act3_screenplay")
        return f"Idea saved to: {save_path1}\nCharacters saved to: {save_path2}\nOutline saved to: {save_path3}\nAct 1 saved to: {save_path4}\nAct 2 saved to: {save_path5}\nAct 3 saved to: {save_path6}"
    save_btn.click(
        fn=save_all_acts,
        inputs=[idea_output, characters_output, outline_output, act1_output, act2_output, act3_output],
        outputs=[save_info]
    )

# Run the app
if __name__ == "__main__":
    demo.launch(share=False)
