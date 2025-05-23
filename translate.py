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
) -> str:
    """
    Translate a subtitle using OpenAI API.
    """
    # Set OpenAI API key
    client = OpenAI(api_key=api_key)
    logger.info(f"Starting translation of file: {original_filename}")

    # Parse .srt content to list of Subtitle objects
    subs: List[Subtitle] = list(parse_srt(subtitle))
    translated_subs: List[Subtitle] = []

    for start in range(0, len(subs), block_size - block_overlap):
        end = min(start + block_size, len(subs))
        block = subs[start:end]
        # Format input text with index to help map translations back

        formatted_input = ""
        for sub in block:
            # Lấy index của phần tử hiện tại
            index_str = f"[{sub.index}]"

            # Lấy nội dung và thay thế tất cả ký tự xuống dòng bằng dấu cách
            content_replaced = sub.content.replace("\n", " ")

            # Tạo một dòng mới có định dạng "[index] nội dung đã xử lý"
            line = f"{index_str} {content_replaced}"

            # Thêm dòng này vào chuỗi kết quả, kèm theo ký tự xuống dòng nếu không phải là dòng đầu tiên
            if formatted_input:
                formatted_input += "\n"
            formatted_input += line

        # Call OpenAI API to translate the block
        prompt = (
            "Bạn là một chuyên gia dịch phụ đề phim.\n"
            "Dịch đoạn hội thoại sau sang tiếng Việt, giữ đúng văn phong và ngữ cảnh đối thoại.\n"
            "Nếu xuất hiện 'you', hãy đoán đúng vai trò trong hội thoại (ví dụ: anh, em, con, mẹ...).\n"
            "Giữ nguyên định dạng số dòng như đầu vào (ví dụ: [5] Câu thoại).\n\n"
            f"{formatted_input}"
        )

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
        # Parse translated result
        translated_lines = translated_text.split("\n")
        block_copy = (
            block.copy()
        )  # Create a copy of the block to avoid modifying the original
        for i, line in enumerate(translated_lines):
            if i >= len(block_copy):
                break
            text_only = line.partition("]")[2].strip() if "]" in line else line
            block_copy[i].content = text_only
        # Keep text that not overlap if not first block
        if start == 0:
            translated_subs.extend(block_copy)
        else:
            non_overlap_start = block_overlap
            translated_subs.extend(block_copy[non_overlap_start:])

    # Convert translated subtitles back to SRT formatted_input
    output_srt = "\n".join(sub.to_srt() for sub in translated_subs)

    # Add the original filename to the output srt
    basename = os.path.splitext(os.path.basename(original_filename))[0]
    output_name = f"{basename}.vi"
    # Write the translated subtitles to a temporary file
    with tempfile.NamedTemporaryFile(
        delete=False, prefix=output_name, suffix=".srt", mode="w", encoding="utf-8"
    ) as temp_file:
        temp_file.write(output_srt)
        logger.info(f"Translated subtitles saved to {temp_file.name}")
        return temp_file.name
