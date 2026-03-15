#!/usr/bin/env python3
"""Локальная транскрибация через Whisper"""

import sys
import whisper

def transcribe_local(audio_path: str, output_path: str):
    print(f"Загрузка модели Whisper...")
    model = whisper.load_model("base")

    print(f"Транскрибация: {audio_path}")
    result = model.transcribe(audio_path, language="ru")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Транскрипция планерки: Воронка продаж\n\n")
        f.write(f"**Дата:** 2 февраля 2024\n\n---\n\n")
        f.write(result["text"])

    print(f"✅ Сохранено: {output_path}")

if __name__ == "__main__":
    transcribe_local(sys.argv[1], sys.argv[2])
