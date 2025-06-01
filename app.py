import gradio as gr
from translate import translate_subtitle
import config

# Default prompt để hiển thị như hướng dẫn
DEFAULT_PROMPT = """\
Bạn là một chuyên gia dịch phụ đề phim.
Dịch đoạn hội thoại sau sang tiếng Việt, giữ đúng văn phong và ngữ cảnh đối thoại.
Nếu xuất hiện 'you', hãy đoán đúng vai trò trong hội thoại (ví dụ: anh, em, con, mẹ...).
Giữ nguyên định dạng số dòng như đầu vào (ví dụ: [5] Câu thoại)."""

def gradio_translate(api_key, srt_file, custom_prompt=None):
    try:
        final_api_key = config.OPENAI_API_KEY or api_key
        if not final_api_key:
            return "Error: API key is required.", None
        if not srt_file:
            return "Error: No file provided.", None
        with open(srt_file, "r", encoding="utf-8") as file:
            subtitle = file.read()
        return "Success! Download your translated file below.", translate_subtitle(
            subtitle=subtitle,
            api_key=final_api_key,
            original_filename=srt_file.name,
            custom_prompt=custom_prompt
        )
    except Exception as e:
        return f"Error: {e}", None

with gr.Blocks() as demo:
    gr.Markdown("## 🎬 Subtitle Translator")
    gr.Markdown("Translate subtitles using OpenAI API. Optionally customize the translation style with your own prompt.")
    
    with gr.Row():
        api_key = gr.Textbox(label="🔑 OpenAI API Key", type="password")
    
    with gr.Row():
        srt_file = gr.File(label="📂 Upload .SRT File")
    
    custom_prompt = gr.Textbox(
        label="✍️ Custom Prompt (Optional)",
        placeholder="Leave blank to use default prompt.",
        lines=6
    )

    gr.Markdown("💡 **Default Prompt Example (used if Custom Prompt is blank):**")
    gr.Code(DEFAULT_PROMPT, language="markdown")

    status, output_file = gradio_translate(api_key, srt_file, custom_prompt)
    translate_button = gr.Button("🚀 Translate")

    result_status = gr.Textbox(label="Status")
    result_file = gr.File(label="Download Translated SRT File")

    def on_translate(api_key, srt_file, custom_prompt):
        return gradio_translate(api_key, srt_file, custom_prompt)

    translate_button.click(
        fn=on_translate,
        inputs=[api_key, srt_file, custom_prompt],
        outputs=[result_status, result_file]
    )

demo.launch()
