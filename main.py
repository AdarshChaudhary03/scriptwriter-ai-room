import gradio as gr
from langgraph.graph import StateGraph, START, END
from state.states import ScriptState
from nodes.idea_generator import idea_generator
from nodes.character_builder import character_builder
from nodes.script_outliner import script_outliner
from nodes.dialogue_writer import dialogue_writer
from tools import save_script_tool
from langgraph.checkpoint.memory import MemorySaver

# -----------------
# Setup LangGraph Workflow
# -----------------
workflow = StateGraph(ScriptState)

workflow.add_node("IdeaGenerator", idea_generator)
workflow.add_node("CharacterBuilder", character_builder)
workflow.add_node("ScriptOutliner", script_outliner)
workflow.add_node("DialogueWriter", dialogue_writer)

workflow.add_edge(START, "IdeaGenerator")
workflow.add_edge("IdeaGenerator", "CharacterBuilder")
workflow.add_edge("CharacterBuilder", "ScriptOutliner")
workflow.add_edge("ScriptOutliner", "DialogueWriter")
workflow.add_edge("DialogueWriter", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


# -----------------
# Script Generation Function
# -----------------
def generate_script(genre):
    """Generate a script flow based on user-selected genre."""
    config = {"configurable": {"thread_id": "user-session"}}
    
    # Pass genre into state so idea_generator can use it
    final_state = app.invoke({"genre": genre}, config=config)

    # Convert list outputs to strings
    characters_str = "\n".join(final_state["characters"]) if isinstance(final_state["characters"], list) else str(final_state["characters"])
    outline_str = "\n".join(final_state["outline"]) if isinstance(final_state["outline"], list) else str(final_state["outline"])
    dialogues_str = "\n".join(final_state["dialogues"]) if isinstance(final_state["dialogues"], list) else str(final_state["dialogues"])

    # Save outputs
    save_path1 = save_script_tool(final_state["idea"], "idea")
    save_path2 = save_script_tool(characters_str, "characters")
    save_path3 = save_script_tool(outline_str, "outline")
    save_path4 = save_script_tool(dialogues_str, "dialogues")

    # Return for UI
    return (
        final_state["idea"],
        characters_str,
        outline_str,
        dialogues_str,
        f"Idea saved to: {save_path1}\nCharacters saved to: {save_path2}\nOutline saved to: {save_path3}\nDialogues saved to: {save_path4}"
    )


# -----------------
# Gradio UI
# -----------------
with gr.Blocks(title="AI Script Generator") as demo:
    gr.Markdown("# 🎬 AI Script Generator")
    gr.Markdown("Enter a genre, and watch the AI create an idea, characters, outline, and dialogues.")

    with gr.Row():
        genre_input = gr.Textbox(label="🎭 Genre", placeholder="e.g. Thriller, Romance, Sci-Fi")

    with gr.Row():
        generate_btn = gr.Button("Generate Script", variant="primary")

    with gr.Row():
        idea_output = gr.Textbox(label="💡 Plot Idea", lines=4)
    with gr.Row():
        characters_output = gr.Textbox(label="🧑‍🤝‍🧑 Characters", lines=6)
    with gr.Row():
        outline_output = gr.Textbox(label="🗂 Outline", lines=8)
    with gr.Row():
        dialogues_output = gr.Textbox(label="🎤 Dialogues", lines=10)
    with gr.Row():
        save_info = gr.Textbox(label="📂 Saved File Paths", lines=4)

    generate_btn.click(
        fn=generate_script,
        inputs=[genre_input],
        outputs=[idea_output, characters_output, outline_output, dialogues_output, save_info]
    )

# Run the app
if __name__ == "__main__":
    demo.launch()
