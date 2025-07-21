# Subtitle Translator: English ➜ Vietnamese

This project provides both a **web interface** and **command-line interface (CLI)** for translating `.srt` subtitle files from **English to Vietnamese**, powered by **OpenAI's GPT models**. The web interface is built using **Gradio** for easy accessibility, while the CLI offers advanced automation and scripting capabilities.

---

## Project Goals

- Translate English `.srt` subtitles into natural-sounding Vietnamese.
- Preserve subtitle formatting, line numbers, and timestamps.
- Correctly interpret pronouns and conversational context (e.g., "you" → "anh", "em", "con", etc.).
- Provide both accessible web interface and powerful CLI for different use cases.
- Handle large subtitle files efficiently by chunking.
- Support custom prompts for specialized translation contexts (e.g., crime dramas, technical content).

---

## Project Structure

```ruby
subtitle-translator/
├── app.py              # Gradio web interface
├── config.py           # Configuration (model, token limits, block sizes)
├── translate.py        # CLI interface for subtitle translation
├── subtitle_translator.py  # Core translation logic and file handling
├── prompt.json         # Custom prompt configuration (example)
├── .env                # (Optional) Environment file to store API key
├── requirements.txt    # Required dependencies
└── README.md           # Project documentation
```

---

## Requirements

- Python 3.8+
- OpenAI API Key
- Required packages (install via `pip install -r requirements.txt`):
  - `gradio` (for web interface)
  - `openai` (for API access)
  - `srt` (for subtitle parsing)
  - `python-dotenv` (optional, for environment variables)

---

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd subtitle-translator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# Option 1: Environment variable
export OPENAI_API_KEY="your_api_key_here"

# Option 2: Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

---

## Usage

### Web Interface (Gradio)

Launch the web interface for easy drag-and-drop translation:

```bash
python app.py
```

Then open your browser to the displayed URL (usually `http://localhost:7860`).

### Command Line Interface (CLI)

The CLI provides more control and automation capabilities:

#### Basic Usage

```bash
# Translate with default settings
python translate.py -f english_subtitles.srt

# Translate with custom prompt
python translate.py -f english_subtitles.srt -custom_prompt prompt.json

# Specify API key directly
python translate.py -f english_subtitles.srt -api_key your_api_key_here
```

#### Advanced Options

```bash
# Full customization
python translate.py -f movie.srt \
  -custom_prompt prompt.json \
  -model gpt-4 \
  -temp 0.2 \
  -max_tokens 2000 \
  -block_size 8 \
  -block_overlap 1 \
  -o vietnamese_movie.srt
```

#### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-f, --file` | Input .srt file path | Required |
| `-custom_prompt, --custom-prompt` | JSON file with custom prompt | None |
| `-model, --model` | OpenAI model to use | From config.py |
| `-temp, --temperature` | Model temperature (0.0-1.0) | From config.py |
| `-max_tokens, --max-tokens` | Maximum tokens per request | From config.py |
| `-block_size, --block-size` | Subtitles per processing block | From config.py |
| `-block_overlap, --block-overlap` | Overlap between blocks | From config.py |
| `-api_key, --api-key` | OpenAI API key | From environment |
| `-o, --output` | Output file path | Auto-generated |
| `-h, --help` | Show help message | - |

---

## Custom Prompts

Create specialized prompts for different content types by using a JSON configuration file:

### Example: Crime Drama Prompt (`prompt.json`)

```json
{
  "prompt": "Bạn là một chuyên gia dịch phụ đề phim.\nPhim này tên là \"Ballard (2025)\", thể loại **hình sự, điều tra phá án**, lấy bối cảnh ở Los Angeles, với nhân vật chính là Thanh tra LAPD Renee Ballard phụ trách đơn vị án lạnh.\nHãy dịch đoạn hội thoại sau sang **tiếng Việt**, giữ đúng ngữ cảnh, sắc thái, và không khí hình sự căng thẳng, thực tế.\n- Giữ văn phong **ngắn gọn, tự nhiên, hơi lạnh lùng, đời thường** như trong phim điều tra.\n- Nếu xuất hiện 'you', hãy đoán đúng vai trò xưng hô trong hội thoại (ví dụ: cô, anh, em, chị, sếp...) dựa vào bối cảnh câu nói.\n- Giữ nguyên định dạng số dòng như đầu vào (ví dụ: [5] Câu thoại).\n- Giữ nguyên tên nhân vật, thuật ngữ chuyên ngành hoặc tên riêng (LAPD, cold case, Ballard…).\n- Tránh dịch quá văn hoa, hãy dịch giống phụ đề phim truyền hình hình sự Mỹ.\nVí dụ:\n[1] Ballard, you got a minute?\n[2] Sure. What's up?\n(Kết quả mong muốn:[1] Ballard, cô rảnh một phút không?[2] Ừ. Có chuyện gì?)"
}
```

### Using Custom Prompts

```bash
# For crime dramas
python translate.py -f crime_show.srt -custom_prompt crime_prompt.json

# For medical dramas
python translate.py -f medical_show.srt -custom_prompt medical_prompt.json

# For comedy shows
python translate.py -f comedy_show.srt -custom_prompt comedy_prompt.json
```

---

## Examples

### Web Interface Example

1. Launch: `python app.py`
2. Upload your `.srt` file
3. Enter your OpenAI API key
4. Optionally customize the prompt
5. Click "Translate"
6. Download the translated file

### CLI Example

```bash
# Translate a TV show episode
python translate.py -f "Breaking.Bad.S01E01.srt" \
  -custom_prompt tv_drama_prompt.json \
  -model gpt-4 \
  -temp 0.1 \
  -o "Breaking.Bad.S01E01.vi.srt"
```

---

## Features

### Web Interface
- ✅ Drag-and-drop file upload
- ✅ Real-time translation progress
- ✅ Downloadable results
- ✅ Custom prompt input
- ✅ API key management

### CLI Interface
- ✅ Batch processing automation
- ✅ Custom prompt files
- ✅ Advanced parameter control
- ✅ Environment variable support
- ✅ Error handling and validation
- ✅ Progress logging
- ✅ Flexible output naming

### Translation Quality
- ✅ Context-aware pronoun translation
- ✅ Preserves formatting and timestamps
- ✅ Handles overlapping dialogue
- ✅ Maintains subtitle numbering
- ✅ Genre-specific language adaptation

---

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenAI API key is valid and has sufficient credits
2. **File Not Found**: Check file paths and permissions
3. **JSON Error**: Validate your custom prompt JSON syntax
4. **Model Not Available**: Verify the model name is correct and accessible with your API key

### Getting Help

```bash
# View all CLI options
python translate.py --help

# Check configuration
python -c "import config; print(config.MODEL, config.TEMPERATURE)"
```

---

## License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this software with attribution.