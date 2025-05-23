import gradio as gr
from translate import translate_subtitle
import config


def gradio_translate(api_key, srt_file):
    """
    Translate SRT file using OpenAI API.
    """
    try:
        # Check API key
        final_api_key = config.OPENAI_API_KEY or api_key
        if not final_api_key:
            return "Error: API key is required.", None
        # Check if file is provided
        if not srt_file:
            return "Error: No file provided.", None
        with open(srt_file, "r", encoding="utf-8") as file:
            subtitle = file.read()
        return "Success! Download your translated file below.", translate_subtitle(
            subtitle=subtitle, api_key=api_key, original_filename=srt_file.name
        )
    except Exception as e:
        return f"Error: {e}"


gr.Interface(
    fn=gradio_translate,
    inputs=[
        gr.Textbox(label="OpenAI API Key", type="password"),
        gr.File(label="Upload SRT File"),
    ],
    outputs=[gr.Textbox(label="Status"), gr.File(label="Download Translated SRT File")],
    title="Subtitle Translator",
    description="Translate subtitles using OpenAI API.",
).launch()
