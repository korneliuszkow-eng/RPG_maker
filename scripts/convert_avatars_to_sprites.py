#!/usr/bin/env python3
"""
Konwersja avatarów do sprite'ów VX Ace
Tworzy sprite sheets z animacjami dla każdej postaci
"""

import os
from PIL import Image, ImageDraw, ImageFilter
import json

# Konfiguracja VX Ace
VX_ACE_SPRITE_WIDTH = 96
VX_ACE_SPRITE_HEIGHT = 96
FRAMES_PER_STATE = 4  # idle, attack, hurt, dead

# Stany animacji
STATES = ['idle', 'attack', 'hurt', 'dead']

class AvatarToSpriteConverter:
    def __init__(self, input_dir='assets/characters', output_dir='game/Graphics/Characters'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def load_avatar(self, filename):
        """Wczytaj avatar"""
        path = os.path.join(self.input_dir, filename)
        if not os.path.exists(path):
            print(f"❌ Nie znaleziono: {path}")
            return None
        return Image.open(path)
    
    def resize_to_sprite_size(self, img):
        """Przeskaluj do rozmiaru VX Ace sprite'a"""
        img.thumbnail((VX_ACE_SPRITE_WIDTH, VX_ACE_SPRITE_HEIGHT), Image.Resampling.LANCZOS)
        
        # Stwórz nowy obraz z białym tłem
        sprite = Image.new('RGBA', (VX_ACE_SPRITE_WIDTH, VX_ACE_SPRITE_HEIGHT), (255, 255, 255, 0))
        offset = ((VX_ACE_SPRITE_WIDTH - img.width) // 2, 
                  (VX_ACE_SPRITE_HEIGHT - img.height) // 2)
        sprite.paste(img, offset, img if img.mode == 'RGBA' else None)
        return sprite
    
    def create_animation_frame(self, base_sprite, state):
        """Stwórz animacyjną ramkę dla danego stanu"""
        frame = base_sprite.copy()
        
        if state == 'idle':
            # Brak zmian - normalny sprite
            return frame
        elif state == 'attack':
            # Lekko jaśniejszy - atakuje
            return self.brighten_image(frame, 1.2)
        elif state == 'hurt':
            # Odcień czerwony - zraniony
            return self.colorize_image(frame, (255, 0, 0), 0.3)
        elif state == 'dead':
            # Czarno-białe - martwy
            return self.grayscale_image(frame, 0.5)
        
        return frame
    
    def brighten_image(self, img, factor):
        """Rozjaśnij obraz"""
        result = img.copy()
        enhancer = Image.ImageEnhance.Brightness(result)
        return enhancer.enhance(factor)
    
    def colorize_image(self, img, color, alpha):
        """Nałóż kolor na obraz"""
        result = img.copy()
        overlay = Image.new('RGBA', result.size, color + (int(255 * alpha),))
        return Image.alpha_composite(result, overlay)
    
    def grayscale_image(self, img, alpha):
        """Skonwertuj na czarno-białe z przezroczystością"""
        result = img.convert('LA')
        result = result.convert('RGBA')
        return result
    
    def create_sprite_sheet(self, character_name, avatar_img):
        """Stwórz sheet sprite'a (4x4 - 4 stany x 4 ramki animacji)"""
        sheet_width = VX_ACE_SPRITE_WIDTH * 4
        sheet_height = VX_ACE_SPRITE_HEIGHT * 4
        sheet = Image.new('RGBA', (sheet_width, sheet_height), (255, 255, 255, 0))
        
        base_sprite = self.resize_to_sprite_size(avatar_img)
        
        for state_idx, state in enumerate(STATES):
            for frame_idx in range(4):
                # Stwórz ramkę z lekką animacją
                frame = self.create_animation_frame(base_sprite, state)
                
                # Dodaj lekkie skalowanie do animacji
                if frame_idx > 0:
                    scale = 1.0 + (0.02 * (frame_idx - 1))
                    new_size = int(VX_ACE_SPRITE_WIDTH * scale), int(VX_ACE_SPRITE_HEIGHT * scale)
                    frame = frame.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # Centruj
                    temp = Image.new('RGBA', (VX_ACE_SPRITE_WIDTH, VX_ACE_SPRITE_HEIGHT), (255, 255, 255, 0))
                    offset = ((VX_ACE_SPRITE_WIDTH - frame.width) // 2,
                             (VX_ACE_SPRITE_HEIGHT - frame.height) // 2)
                    temp.paste(frame, offset, frame)
                    frame = temp
                
                # Umieść na sheet'cie
                x = frame_idx * VX_ACE_SPRITE_WIDTH
                y = state_idx * VX_ACE_SPRITE_HEIGHT
                sheet.paste(frame, (x, y), frame)
        
        return sheet
    
    def save_sprite_sheet(self, character_name, sheet):
        """Zapisz sprite sheet"""
        output_path = os.path.join(self.output_dir, f"{character_name}_sprite.png")
        sheet.save(output_path, 'PNG')
        print(f"✅ Zapisano: {output_path}")
        return output_path
    
    def create_character_config(self, character_name, original_img_size):
        """Stwórz JSON z konfiguracją postaci"""
        config = {
            "character_name": character_name,
            "sprite_sheet": f"{character_name}_sprite.png",
            "sprite_width": VX_ACE_SPRITE_WIDTH,
            "sprite_height": VX_ACE_SPRITE_HEIGHT,
            "frames_per_state": 4,
            "states": STATES,
            "original_image_size": original_img_size,
            "animations": {
                "idle": {"frames": [0, 1, 2, 3], "speed": 8},
                "attack": {"frames": [0, 1, 2, 1], "speed": 6},
                "hurt": {"frames": [0, 1], "speed": 4},
                "dead": {"frames": [0], "speed": 0}
            }
        }
        return config
    
    def convert(self, character_name, avatar_filename):
        """Główny proces konwersji"""
        print(f"\n🎨 Konwersja: {character_name}...")
        
        # Wczytaj avatar
        avatar = self.load_avatar(avatar_filename)
        if avatar is None:
            return False
        
        # Stwórz sprite sheet
        sprite_sheet = self.create_sprite_sheet(character_name, avatar)
        
        # Zapisz sprite sheet
        self.save_sprite_sheet(character_name, sprite_sheet)
        
        # Stwórz konfigurację
        config = self.create_character_config(character_name, avatar.size)
        config_path = os.path.join(self.output_dir, f"{character_name}_config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Konfiguracja: {config_path}")
        
        return True


def main():
    converter = AvatarToSpriteConverter()
    
    characters = [
        ('Gustawiusz', 'gustawisz.jpg'),
        ('Pele', 'pele.jpg'),
        ('Marcinek34', 'marcinek.jpg'),
    ]
    
    print("=" * 50)
    print("🎮 KONWERSJA AVATARÓW DO SPRITE'ÓW VX ACE")
    print("=" * 50)
    
    success_count = 0
    for char_name, avatar_file in characters:
        if converter.convert(char_name, avatar_file):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Konwersja ukończona: {success_count}/{len(characters)}")
    print("=" * 50)


if __name__ == '__main__':
    main()
