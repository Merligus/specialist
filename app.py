# app interface related
import gradio as gr
import shutil
import tempfile
from pathlib import Path
import time

# ai related
from Chroma import create_db
from LangChain import query, load_chain


# function to store the state
def load_data(
    chunk_size,
    chunk_overlap,
    uploaded_files,
    existing_data,
    progress=gr.Progress(),
):
    try:
        progress(0, desc="Loading chain...")
        time.sleep(0.5)
        print("Loading chain...")
        # chain load
        chain = load_chain()
        progress(0.3, desc="Chain loaded")
        time.sleep(0.5)
        print("Chain loaded")

        print("Creating db...")
        # clean up previous temporary directory if it exists
        if existing_data and "temp_dir" in existing_data:
            shutil.rmtree(existing_data["temp_dir"])

        # create new consolidated temporary directory
        temp_dir = tempfile.mkdtemp()

        print(f"Copying files to {temp_dir}...")
        # preserve original directory structure
        for i, uploaded_file in enumerate(uploaded_files, 1):
            src_path = Path(uploaded_file.name)
            # move file to consolidated directory
            shutil.move(src_path, temp_dir)
            # update progress bar
            progress(
                0.3 + 0.2 * i / len(uploaded_files), f"Processing {uploaded_file.name.split('/')[-1]}"
            )
            time.sleep(0.1)

        # create db file
        progress(0.5, desc="Creating db...")
        db = create_db(chunk_size, chunk_overlap, INPUT_PATH=temp_dir, CHROMA_PATH=temp_dir)
        progress(1.0, desc="DB created")
        print("DB created")

        return {
            "db": db,
            "chain": chain,
            "temp_dir": temp_dir,
            "loaded": True,
            "file_count": len(uploaded_files),
        }, "✅ Data loaded successfully!"
    except Exception as e:
        return {"loaded": False, "error": str(e)}, f"❌ Error: {str(e)}"


def chat_response(message, chat_history, data):
    if not data or not data.get("loaded"):
        error_msg = data.get("error", "Please load data first!")
        chat_history.append((message, error_msg))
        return chat_history

    # responses based on the input data
    answer, sources = query(message, data["db"], data["chain"])
    sources = "\n".join([s_file.split("/")[-1] for s_file in sources.split("\n")])
    response = f"{answer}\n\nSources:\n{sources}"

    # Append messages as tuples (user, assistant) instead of dictionaries
    chat_history.append((message, response))
    return chat_history


with gr.Blocks(title="Document Analysis Chatbot") as demo:
    # store loaded data
    data_store = gr.State()

    with gr.Row():
        # Left Column - Inputs
        with gr.Column(scale=1):
            gr.Markdown("## Data Upload")
            # create db parameters
            chunk_size = gr.Number(label="Chunk Size", value=1000)
            chunk_overlap = gr.Number(label="Chunk Overlap", value=500)
            # load file
            folder_input = gr.File(file_count="directory", label="Upload Folder")
            # Add status display
            status_text = gr.Textbox(
                label="Status",
                interactive=False,
                show_label=False
            )
            # load button
            load_btn = gr.Button("Load Data", variant="primary")

        # Right Column - Chat
        with gr.Column(scale=3, visible=False) as chat_col:
            gr.Markdown("## Chat Interface")
            chatbot = gr.Chatbot(
                label="Document Analysis Chat",
                type="tuples",
                bubble_full_width=False,  # Prevent stretching of messages
                render_markdown=True,  # Handle markdown formatting properly,
                height=500,
            )
            msg = gr.Textbox(label="Your Question", placeholder="Type your question...")
            clear_btn = gr.Button("Clear Chat", variant="secondary")

    # Loading indicators - update to handle multiple outputs
    load_btn.click(
        fn=load_data,
        inputs=[chunk_size, chunk_overlap, folder_input, data_store],
        outputs=[data_store, status_text],
    ).then(fn=lambda: gr.Column(visible=True), outputs=chat_col)

    # Chat interaction
    msg.submit(
        fn=chat_response,
        inputs=[msg, chatbot, data_store],
        outputs=[chatbot],
    ).then(lambda: "", None, msg)

    # Clear chat
    clear_btn.click(lambda: [], None, chatbot)

if __name__ == "__main__":
    demo.launch()
