#!/usr/bin/env python3
"""Транскрибация аудио по частям через OpenAI Whisper API"""

import os
import sys
import glob
from pathlib import Path
from openai import OpenAI

def transcribe_parts(parts_dir: str, output_path: str):
    """Транскрибирует части аудио и объединяет результат"""

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Найти все части
    parts = sorted(glob.glob(f"{parts_dir}/audio_part_*.mp3"))

    if not parts:
        print(f"Части не найдены в {parts_dir}")
        sys.exit(1)

    print(f"Найдено частей: {len(parts)}")

    full_transcript = []

    for i, part_path in enumerate(parts):
        print(f"[{i+1}/{len(parts)}] Транскрибация: {Path(part_path).name}")

        try:
            with open(part_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="ru"
                )

            full_transcript.append(transcript.text)
            print(f"✅ Готово")

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            continue

    # Сохранение
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Транскрипция планерки: Воронка продаж\n\n")
        f.write(f"**Дата:** 2 февраля 2024\n")
        f.write(f"**Длительность:** 1:21:35\n\n")
        f.write(f"---\n\n")
        f.write("\n\n".join(full_transcript))

    print(f"\n✅ Транскрипция сохранена: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 transcribe_parts.py <parts_dir> <output_path>")
        sys.exit(1)

    transcribe_parts(sys.argv[1], sys.argv[2])
