#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
import config
from translate import translate_subtitle  # Import your function


def load_custom_prompt(prompt_file: str) -> str:
    """Load custom prompt from JSON file."""
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Expect JSON structure like: {"prompt": "Your custom prompt here"}
            return data.get("prompt", "")
    except FileNotFoundError:
        print(f"Error: Prompt file '{prompt_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in prompt file '{prompt_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading prompt file '{prompt_file}': {e}")
        sys.exit(1)


def validate_file(file_path: str) -> str:
    """Validate if file exists and is readable."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    if not os.access(file_path, os.R_OK):
        print(f"Error: Cannot read file '{file_path}'.")
        sys.exit(1)

    return file_path


def main():
    parser = argparse.ArgumentParser(
        description="Translate subtitle files using OpenAI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python translate.py -f eng.srt
  python translate.py -f eng.srt -custom_prompt prompt.json
  python translate.py -f eng.srt -model gpt-4 -temp 0.3
  python translate.py -f eng.srt -custom_prompt prompt.json -max_tokens 2000
        """,
    )

    # Required arguments
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the subtitle file (.srt) to translate",
    )

    # Optional arguments
    parser.add_argument(
        "-custom_prompt",
        "--custom-prompt",
        help="Path to JSON file containing custom prompt",
    )

    parser.add_argument(
        "-model",
        "--model",
        default=config.MODEL,
        help=f"OpenAI model to use (default: {config.MODEL})",
    )

    parser.add_argument(
        "-temp",
        "--temperature",
        type=float,
        default=config.TEMPERATURE,
        help=f"Temperature for the model (default: {config.TEMPERATURE})",
    )

    parser.add_argument(
        "-max_tokens",
        "--max-tokens",
        type=int,
        default=config.MAX_TOKENS,
        help=f"Maximum tokens per request (default: {config.MAX_TOKENS})",
    )

    parser.add_argument(
        "-block_size",
        "--block-size",
        type=int,
        default=config.BLOCK_SIZE,
        help=f"Number of subtitles to process in each block (default: {config.BLOCK_SIZE})",
    )

    parser.add_argument(
        "-block_overlap",
        "--block-overlap",
        type=int,
        default=config.CHUNK_OVERLAP,
        help=f"Number of overlapping subtitles between blocks (default: {config.CHUNK_OVERLAP})",
    )

    parser.add_argument(
        "-api_key",
        "--api-key",
        help="OpenAI API key (if not set, will try to get from environment variable OPENAI_API_KEY)",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (if not specified, will use default naming)",
    )

    args = parser.parse_args()

    # Validate input file
    input_file = validate_file(args.file)

    # Check if it's a .srt file
    if not input_file.lower().endswith(".srt"):
        print("Warning: Input file doesn't have .srt extension. Proceeding anyway...")

    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: OpenAI API key not provided. Use -api_key argument or set OPENAI_API_KEY environment variable."
        )
        sys.exit(1)

    # Load custom prompt if provided
    custom_prompt = None
    if args.custom_prompt:
        custom_prompt = load_custom_prompt(args.custom_prompt)
        print(f"Using custom prompt from: {args.custom_prompt}")

    # Read subtitle file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            subtitle_content = f.read()
    except Exception as e:
        print(f"Error reading subtitle file: {e}")
        sys.exit(1)

    # Translate subtitle
    print(f"Starting translation of: {input_file}")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"Block size: {args.block_size}")
    print(f"Block overlap: {args.block_overlap}")
    print("-" * 50)

    try:
        output_file = translate_subtitle(
            subtitle=subtitle_content,
            api_key=api_key,
            original_filename=input_file,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            block_size=args.block_size,
            block_overlap=args.block_overlap,
            custom_prompt=custom_prompt,
        )

        print(f"\nTranslation completed successfully!")
        print(f"Output saved to: {output_file}")

        # If user specified custom output path, move the file
        if args.output:
            import shutil

            shutil.move(output_file, args.output)
            print(f"File moved to: {args.output}")

    except Exception as e:
        print(f"Error during translation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
