import tempfile
from srt import parse as parse_srt, Subtitle
from openai import OpenAI
from typing import List
import config
import os
import logging

# Enable logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def translate_subtitle(
    subtitle: str,
    api_key,
    original_filename: str,
    model: str = config.MODEL,
    temperature: float = config.TEMPERATURE,
    max_tokens: int = config.MAX_TOKENS,
    block_size: int = config.BLOCK_SIZE,
    block_overlap: int = config.CHUNK_OVERLAP,
    custom_prompt: str | None = None,
) -> str:
    """
    Translate a subtitle using OpenAI API.
    """
    client = OpenAI(api_key=api_key)
    logger.info(f"Starting translation of file: {original_filename}")

    subs: List[Subtitle] = list(parse_srt(subtitle))
    translated_subs: List[Subtitle] = []

    for start in range(0, len(subs), block_size - block_overlap):
        end = min(start + block_size, len(subs))
        block = subs[start:end]

        formatted_input = ""
        for sub in block:
            index_str = f"[{sub.index}]"
            content_replaced = sub.content.replace("\n", " ")
            line = f"{index_str} {content_replaced}"
            if formatted_input:
                formatted_input += "\n"
            formatted_input += line

        # Use custom prompt if provided, otherwise use default prompt
        default_prompt = (
            "Bạn là một chuyên gia dịch phụ đề phim.\n"
            "Dịch đoạn hội thoại sau sang tiếng Việt, giữ đúng văn phong và ngữ cảnh đối thoại.\n"
            "Nếu xuất hiện 'you', hãy đoán đúng vai trò trong hội thoại (ví dụ: anh, em, con, mẹ...).\n"
            "Giữ nguyên định dạng số dòng như đầu vào (ví dụ: [5] Câu thoại).\n\n"
        )
        prompt = (
            custom_prompt.strip() + "\n\n" if custom_prompt else default_prompt
        ) + formatted_input

        translated_text = ""
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            translated_text = (
                response.choices[0].message.content.strip()
                if response.choices[0].message.content
                else ""
            )
            logger.info(f"Translated block {start}-{end}: {translated_text}")

        except Exception as e:
            print(f"Error translating block {start}-{end}: {e}")

        translated_lines = translated_text.split("\n")
        block_copy = block.copy()
        for i, line in enumerate(translated_lines):
            if i >= len(block_copy):
                break
            text_only = line.partition("]")[2].strip() if "]" in line else line
            block_copy[i].content = text_only
        if start == 0:
            translated_subs.extend(block_copy)
        else:
            non_overlap_start = block_overlap
            translated_subs.extend(block_copy[non_overlap_start:])

    output_srt = "\n".join(sub.to_srt() for sub in translated_subs)

    basename = os.path.splitext(os.path.basename(original_filename))[0]
    output_name = f"{basename}.vi"
    with tempfile.NamedTemporaryFile(
        delete=False, prefix=output_name, suffix=".srt", mode="w", encoding="utf-8"
    ) as temp_file:
        temp_file.write(output_srt)
        logger.info(f"Translated subtitles saved to {temp_file.name}")
        return temp_file.name
