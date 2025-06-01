#!/bin/bash

# Kiểm tra tham số
if [ -z "$1" ]; then
    echo "❌ Vui lòng cung cấp tên file .mkv"
    echo "📌 Ví dụ: ./extract_en_srt.sh movie.mkv"
    exit 1
fi

INPUT_FILE="$1"

# Kiểm tra file tồn tại
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ File không tồn tại: $INPUT_FILE"
    exit 1
fi

# Lấy thông tin stream và tìm dòng phụ đề tiếng Anh (eng)
ENG_SUB_INDEX=$(ffprobe -v error -select_streams s \
  -show_entries stream=index:stream_tags=language \
  -of csv=p=0 "$INPUT_FILE" | grep ",eng" | head -n 1 | cut -d',' -f1)

# Kiểm tra xem tìm thấy phụ đề tiếng Anh chưa
if [ -z "$ENG_SUB_INDEX" ]; then
    echo "❌ Không tìm thấy phụ đề tiếng Anh trong file."
    exit 1
fi

# Tạo tên file output .srt
BASENAME=$(basename "$INPUT_FILE" .mkv)
OUTPUT_FILE="${BASENAME}.en.srt"

# Thực hiện trích xuất phụ đề
ffmpeg -i "$INPUT_FILE" -map 0:"$ENG_SUB_INDEX" -c:s copy "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    # Xoá toàn bộ ký tự carriage return (^M)
    tr -d '\r' < "$OUTPUT_FILE" > "${OUTPUT_FILE}.clean" && mv "${OUTPUT_FILE}.clean" "$OUTPUT_FILE"
    echo "✅ Đã trích xuất và làm sạch phụ đề tiếng Anh: $OUTPUT_FILE"
else
    echo "❌ Có lỗi khi trích xuất phụ đề."
fi
