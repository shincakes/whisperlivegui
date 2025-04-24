import gradio as gr
with gr.Blocks() as demo:
    btn = gr.Button("Test")
print(dir(btn))