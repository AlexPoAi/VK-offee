#!/usr/bin/env python3
"""Транскрибация видео планерок через OpenAI Whisper API"""

import os
import sys
from pathlib import Path
from openai import OpenAI

def transcribe_video(video_path: str, output_path: str):
    """Транскрибирует видео и сохраняет результат в markdown"""

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print(f"Транскрибация: {video_path}")

    with open(video_path, "rb") as video_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=video_file,
            language="ru"
        )

    # Сохранение транскрипции
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Транскрипция планерки\n\n")
        f.write(f"**Источник:** {Path(video_path).name}\n\n")
        f.write(f"---\n\n")
        f.write(transcript.text)

    print(f"✅ Сохранено: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 transcribe.py <video_path> <output_path>")
        sys.exit(1)

    transcribe_video(sys.argv[1], sys.argv[2])
