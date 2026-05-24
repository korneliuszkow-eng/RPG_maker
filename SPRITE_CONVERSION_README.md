## 🎨 Konwersja Avatarów do Sprite'ów VX Ace

### O czym to?
Script konwertuje avatary postaci (PNG/JPG) na sprite sheets kompatybilne z RPG Maker VX Ace.

### Struktura Sprite Sheet
- **Wymiary**: 384x384 pikseli (4x4 ramki po 96x96 każda)
- **4 stany**: Idle, Attack, Hurt, Dead
- **4 ramki animacji** dla każdego stanu

### Jak używać?

#### 1. Wymagania
```bash
pip install Pillow
```

#### 2. Przygotowanie avatarów
Umieść avatary w folderze `assets/characters/`:
```
assets/characters/
├── gustawisz.jpg
├── pele.jpg
├── marcinek.jpg
└── ...
```

#### 3. Uruchomienie skryptu
```bash
python scripts/convert_avatars_to_sprites.py
```

#### 4. Wynik
Script tworzy:
- `game/Graphics/Characters/{character}_sprite.png` - sprite sheet
- `game/Graphics/Characters/{character}_config.json` - konfiguracja

### Wygenerowane Stany Animacji

| Stan | Opis | Efekt |
|------|------|-------|
| **Idle** | Spoczynkowa | Normalne kolory |
| **Attack** | Atak | +20% jasności |
| **Hurt** | Zraniony | Odcień czerwony |
| **Dead** | Martwy | Czarno-białe |

### Konfiguracja JSON
```json
{
  "character_name": "Gustawiusz",
  "sprite_sheet": "Gustawiusz_sprite.png",
  "sprite_width": 96,
  "sprite_height": 96,
  "frames_per_state": 4,
  "states": ["idle", "attack", "hurt", "dead"],
  "animations": {
    "idle": {"frames": [0, 1, 2, 3], "speed": 8},
    "attack": {"frames": [0, 1, 2, 1], "speed": 6},
    "hurt": {"frames": [0, 1], "speed": 4},
    "dead": {"frames": [0], "speed": 0}
  }
}
```

### Integracja z VX Ace
1. Skopiuj `*_sprite.png` do `game/Graphics/Characters/`
2. Używaj w edytorze VX Ace jako zwykły sprite
3. Konfiguracja JSON zawiera metadane dla custom skryptów

### Rozszerzenie
Aby dodać więcej postaci:
1. Dodaj avatar do `assets/characters/`
2. Dodaj wpis w liście `characters` w `main()`
3. Uruchom script

### TODO
- [ ] Obsługa więcej animacji (walk, magic, defend)
- [ ] Generowanie direction variants (4-kierunkowy sprite)
- [ ] Batch processing dla wielu avatarów
- [ ] GUI do podglądu sprite'ów
