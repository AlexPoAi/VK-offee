#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления кодировки в knowledge-base/
Конвертирует все .md и .txt файлы в UTF-8
"""

import os
from pathlib import Path
import chardet
import shutil
from datetime import datetime

# Пути
REPO_PATH = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = REPO_PATH / "knowledge-base"
BACKUP_PATH = REPO_PATH / f"knowledge-base-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

# Статистика
stats = {
    'total': 0,
    'fixed': 0,
    'already_utf8': 0,
    'errors': 0,
    'error_files': []
}

def detect_encoding(file_path):
    """Определение кодировки файла"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding'], result['confidence']
    except Exception as e:
        return None, 0

def fix_file_encoding(file_path):
    """Исправление кодировки файла"""
    try:
        # Определяем текущую кодировку
        encoding, confidence = detect_encoding(file_path)

        if not encoding:
            print(f"  ⚠️  Не удалось определить кодировку")
            stats['errors'] += 1
            stats['error_files'].append(str(file_path.relative_to(REPO_PATH)))
            return False

        # Если уже UTF-8, пропускаем
        if encoding.lower() in ['utf-8', 'ascii']:
            stats['already_utf8'] += 1
            return True

        print(f"  🔄 Конвертация: {encoding} → UTF-8 (уверенность: {confidence:.0%})")

        # Читаем с определённой кодировкой
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()

        # Записываем в UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        stats['fixed'] += 1
        return True

    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        stats['errors'] += 1
        stats['error_files'].append(str(file_path.relative_to(REPO_PATH)))
        return False

def main():
    print("="*60)
    print("🔧 ИСПРАВЛЕНИЕ КОДИРОВКИ В KNOWLEDGE-BASE")
    print("="*60)
    print()

    # Проверка существования папки
    if not KNOWLEDGE_BASE_PATH.exists():
        print(f"❌ Папка не найдена: {KNOWLEDGE_BASE_PATH}")
        return

    print(f"📁 Папка: {KNOWLEDGE_BASE_PATH}")
    print()

    # Создание резервной копии
    print("💾 Создание резервной копии...")
    try:
        shutil.copytree(KNOWLEDGE_BASE_PATH, BACKUP_PATH)
        print(f"✅ Резервная копия создана: {BACKUP_PATH}")
    except Exception as e:
        print(f"⚠️  Не удалось создать резервную копию: {e}")
        response = input("Продолжить без резервной копии? (y/n): ")
        if response.lower() != 'y':
            print("Отмене��о")
            return

    print()
    print("🔍 Поиск файл��в для обработки...")
    print()

    # Находим все текстовые файлы
    text_files = []
    for ext in ['.md', '.txt']:
        text_files.extend(KNOWLEDGE_BASE_PATH.rglob(f"*{ext}"))

    # Исключаем отчёты синхронизации
    text_files = [f for f in text_files if 'sync-report' not in str(f).lower()]

    print(f"Найдено файлов: {len(text_files)}")
    print()

    # Обработка файлов
    print("⚙️  Обработка файлов...")
    print()

    for i, file_path in enumerate(text_files, 1):
        stats['total'] += 1
        rel_path = file_path.relative_to(KNOWLEDGE_BASE_PATH)
        print(f"[{i}/{len(text_files)}] {rel_path}")

        fix_file_encoding(file_path)

    # Итоговая статистика
    print()
    print("="*60)
    print("✅ ОБ��АБОТКА ЗАВЕРШЕНА")
    print("="*60)
    print()
    print(f"📊 Статистика:")
    print(f"  Всего файлов: {stats['total']}")
    print(f"  Исправлено: {stats['fixed']}")
    print(f"  Уже UTF-8: {stats['already_utf8']}")
    print(f"  Ошибок: {stats['errors']}")
    print()

    if stats['error_files']:
        print("❌ Файлы с ошибками:")
        for file in stats['error_files']:
            print(f"  - {file}")
        print()

    print(f"💾 Ре��ервная копия: {BACKUP_PATH}")
    print()
    print("✅ Готово! Теперь можно запустить Telegram-бота.")

if __name__ == '__main__':
    main()
