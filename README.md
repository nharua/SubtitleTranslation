# Subtitle Translator: English ➜ Vietnamese

This project provides a simple and user-friendly web interface for translating `.srt` subtitle files from **English to Vietnamese**, powered by **OpenAI's GPT models**. It is built using **Gradio** and supports file uploads, API key management, and downloadable translated results.

---

## Project Goals

- Translate English `.srt` subtitles into natural-sounding Vietnamese.
- Preserve subtitle formatting, line numbers, and timestamps.
- Correctly interpret pronouns and conversational context (e.g., "you" → "anh", "em", "con", etc.).
- Provide an accessible and intuitive interface via Gradio.
- Handle large subtitle files efficiently by chunking.

---

## Project Structure

```ruby
subtitle-translator/
├── app.py              # Gradio interface
├── config.py           # Configuration (model, token limits, block sizes)
├── translate.py        # Translation logic and file handling
├── .env                # (Optional) Environment file to store API key
├── requirements.txt    # Required dependencies
└── README.md           # Project documentation
```
---

## Requirements
- Python 3.8+
- Gradio
- OpenAI API Key
- dotenv (optional, for environment variables)

---

## License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this software with attribution.






