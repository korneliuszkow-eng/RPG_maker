#!/bin/bash

# 🎨 Skrypt do konwersji avatarów do sprite'ów VX Ace

echo "=========================================="
echo "🎮 KONWERSJA AVATARÓW DO SPRITE'ÓW VX ACE"
echo "=========================================="
echo ""

# Sprawdź czy Python jest zainstalowany
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nie jest zainstalowany!"
    exit 1
fi

# Zainstaluj wymagane pakiety
echo "📦 Instalowanie wymaganych pakietów..."
pip install -r requirements.txt

# Sprawdź czy folder assets/characters istnieje
if [ ! -d "assets/characters" ]; then
    echo "❌ Folder assets/characters nie istnieje!"
    exit 1
fi

# Stwórz folder wyjściowy
mkdir -p game/Graphics/Characters

# Uruchom skrypt konwersji
echo ""
echo "🎨 Rozpoczęcie konwersji..."
python3 scripts/convert_avatars_to_sprites.py

echo ""
echo "=========================================="
echo "✅ Konwersja ukończona!"
echo "=========================================="
echo ""
echo "Sprite sheets znajdują się w: game/Graphics/Characters/"
echo "Konfiguracje JSON znajdują się tam samym folderze"
echo ""
