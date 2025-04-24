import gradio as gr
import os
import socket
import threading
from whisper_live.client import TranscriptionClient

client = None
streaming = False
last_text = ""
transcription_box = []

# Handle real-time transcription updates
def on_transcription(text, is_final):
    global last_text
    combined_text = "\n".join(text).strip()
    if is_final and combined_text != last_text:
        last_text = combined_text
        transcription_box.append(combined_text)
    elif not is_final:
        if transcription_box:
            transcription_box[-1] = combined_text
        else:
            transcription_box.append(combined_text)

# Start audio streaming
def start_stream():
    global client, streaming
    if not streaming:
        streaming = True
        transcription_box.clear()
        client = TranscriptionClient(
            "localhost", 9090,
            lang="en", translate=False,
            model="tiny.en", use_vad=True,
            callback=on_transcription,
        )
        threading.Thread(target=client, daemon=True).start()
        return "🎤 Listening..."
    return "Already streaming..."

# Stop audio streaming
def stop_stream():
    global client, streaming
    if streaming:
        streaming = False
        if client:
            client.close_all_clients()
            client.write_all_clients_srt()
            client = None
        return "🛑 Stopped listening."
    return "Not streaming."

# Display transcription
def get_transcription():
    return "\n".join(transcription_box[-5:])

# Speak out the last transcribed sentence
def speak_transcription():
    if transcription_box:
        text = transcription_box[-1]
        clean_text = text.replace('"', '').replace("'", "")
        os.system(f'espeak "{clean_text}"')
        return f"🗣️ Spoke: {clean_text}"
    return "❗ No transcription yet."


# Custom CSS for button colors and layout
custom_css = """
.start-btn button {
    background-color: #d0f5d0 !important;
    color: #0a3 !important;
}
.stop-btn button {
    background-color: #ffd6d6 !important;
    color: #a00 !important;
}
.speak-btn button {
    background-color: #2a62f3 !important;
    color: white !important;
}
.refresh-btn button {
    background-color: #eee !important;
}
.gr-button {
    font-size: 16px !important;
    font-weight: bold;
    border-radius: 20px !important;
    padding: 8px 20px !important;
    min-height: 40px !important;
    width: 100% !important;
    max-width: none !important;
    box-sizing: border-box;
}
.gr-row {
    gap: 10px !important;
}

html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
}
.gradio-container {
    font-family: "Arial", sans-serif;
    padding: 4px !important;
    padding-top: 20px !important;
}
textarea {
    font-size: 20px !important;
    font-weight: 500 !important;
    line-height: 2em !important;
}
.gr-textbox {
    min-height: 150px !important;
}

#status_box textarea {
    font-size: 18px !important;
    padding: 6px !important;
    text-align: center;
}

#transcript_box {
    min-height: 200px !important;
}

footer{
    display:none !important;
}
"""

# Gradio layout
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown('<h2 style="color:#2563eb; margin-bottom: 4px;">🎙️ SpeakECE</h2>')

    status = gr.Textbox(label="Status", value="Ready", interactive=False, max_lines=1, elem_id="status_box" )

    transcript = gr.Textbox(
        label="Transcription",
        placeholder="Listening output will appear here",
        lines=4,
        max_lines=6,
        elem_id="transcript_box"
    )

    with gr.Row():
        with gr.Column(scale=1):
            start_btn = gr.Button("✅ Start", elem_classes="start-btn")
        with gr.Column(scale=1):
            speak_btn = gr.Button("🎤 Speak", elem_classes="speak-btn")

    with gr.Row():
        with gr.Column(scale=1):
            stop_btn = gr.Button("⛔ Stop", elem_classes="stop-btn")
        with gr.Column(scale=1):
            refresh_btn = gr.Button("🔃 Refresh", elem_classes="refresh-btn")


    # Bind button actions
    start_btn.click(start_stream, outputs=status)
    stop_btn.click(stop_stream, outputs=status)
    speak_btn.click(speak_transcription, outputs=status)
    refresh_btn.click(get_transcription, outputs=transcript)
    demo.load(get_transcription, None, transcript, every=1)

# Auto-find open port (starting at 7860)
def find_open_port(start_port=7860, max_tries=10):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise OSError("No open port found in the given range.")

port = find_open_port()
demo.launch(server_name="0.0.0.0", server_port=port, share=False)
