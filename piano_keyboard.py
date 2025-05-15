import pygame as pg
import os

class PianoKeyboard:
    def __init__(self, start_octave=2, num_octaves=5, key_width=60, key_height=300):
        self.start_octave = start_octave
        self.num_octaves = num_octaves
        self.key_width = key_width
        self.key_height = key_height
        
        # Получаем путь к директории с текущим скриптом
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Загрузка изображений клавиш с относительными путями
        white_key_path = os.path.join(base_dir, 'wt_klavisha.png')
        black_key_path = os.path.join(base_dir, 'bl_klavisha.png')
        
        try:
            self.white_key_img = pg.image.load(white_key_path)
            self.black_key_img = pg.image.load(black_key_path)
        except pg.error as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки если изображения не загрузились
            self.white_key_img = pg.Surface((key_width, key_height))
            self.white_key_img.fill((255, 255, 255))
            self.black_key_img = pg.Surface((key_width // 2 + 3, key_height // 2 + 35))
            self.black_key_img.fill((0, 0, 0))
        
        # Масштабирование изображений
        self.white_key_img = pg.transform.scale(self.white_key_img, (key_width, key_height))
        self.black_key_img = pg.transform.scale(self.black_key_img, (key_width // 2 + 3, key_height // 2 + 35))
        
        # Остальной код без изменений
        self.white_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.black_notes = ['C#', 'D#', 'F#', 'G#', 'A#']
        
        self.black_key_positions = {
            'C#': 0.7,
            'D#': 1.7,
            'F#': 3.7,
            'G#': 4.7,
            'A#': 5.7
        }
        
        self.key_labels = {
            'C2': '1', 'D2': '2', 'E2': '3', 'F2': '4', 'G2': '5', 'A2': '6', 'B2': '7',
            'C#2': 'Shift+1', 'D#2': 'Shift+2', 'F#2': 'Shift+4', 'G#2': 'Shift+5', 'A#2': 'Shift+6',
            'C3': 'Q', 'D3': 'W', 'E3': 'E', 'F3': 'R', 'G3': 'T', 'A3': 'Y', 'B3': 'U',
            'C#3': 'Shift+Q', 'D#3': 'Shift+W', 'F#3': 'Shift+R', 'G#3': 'Shift+T', 'A#3': 'Shift+Y',
            'C4': 'A', 'D4': 'S', 'E4': 'D', 'F4': 'F', 'G4': 'G', 'A4': 'H', 'B4': 'J',
            'C#4': 'Shift+A', 'D#4': 'Shift+S', 'F#4': 'Shift+F', 'G#4': 'Shift+G', 'A#4': 'Shift+H',
            'C5': 'Z', 'D5': 'X', 'E5': 'C', 'F5': 'V', 'G5': 'B', 'A5': 'N', 'B5': 'M',
            'C#5': 'Shift+Z', 'D#5': 'Shift+X', 'F#5': 'Shift+V', 'G#5': 'Shift+B', 'A#5': 'Shift+N',
            'C6': '9', 'D6': '0', 'E6': 'i', 'F6': 'o', 'G6': 'p', 'A6': 'k', 'B6': 'l',
            'C#6': 'Shift+9', 'D#6': 'Shift+0', 'F#6': 'Shift+i', 'G#6': 'Shift+o', 'A#6': 'Shift+p,'
        }
        
        self.font = pg.font.Font(None, 20)
        self.black_font = pg.font.Font(None, 16)
        self.keys = self._create_keyboard()
    
    # Остальные методы класса остаются без изменений
    def _create_keyboard(self):
        keys = []
        key_id = 0
        
        for octave in range(self.start_octave, self.start_octave + self.num_octaves):
            for i, note in enumerate(self.white_notes):
                x = (octave - self.start_octave) * len(self.white_notes) * self.key_width + i * self.key_width
                note_name = f"{note}{octave}"
                keys.append({
                    'id': key_id,
                    'note': note_name,
                    'rect': pg.Rect(x, 0, self.key_width, self.key_height),
                    'image': self.white_key_img,
                    'is_black': False,
                    'is_pressed': False,
                    'key_label': self.key_labels.get(note_name, ''),
                    'pressed_img': self._create_pressed_image(self.white_key_img, (200, 200, 200))
                })
                key_id += 1
            
            for note in self.black_notes:
                if note in self.black_key_positions:
                    pos = self.black_key_positions[note]
                    x = (octave - self.start_octave) * len(self.white_notes) * self.key_width + pos * self.key_width
                    note_name = f"{note}{octave}"
                    keys.append({
                        'id': key_id,
                        'note': note_name,
                        'rect': pg.Rect(x, 0, self.key_width // 2, self.key_height // 2),
                        'image': self.black_key_img,
                        'is_black': True,
                        'is_pressed': False,
                        'key_label': self.key_labels.get(note_name, ''),
                        'pressed_img': self._create_pressed_image(self.black_key_img, (100, 100, 100))
                    })
                    key_id += 1
        
        return keys
    
    def _create_pressed_image(self, original_img, tint_color):
        img = original_img.copy()
        overlay = pg.Surface(img.get_size(), pg.SRCALPHA)
        overlay.fill((*tint_color, 128))
        img.blit(overlay, (0, 0), special_flags=pg.BLEND_MULT)
        return img
    
    def press_key_by_note(self, note):
        for key in self.keys:
            if key['note'] == note:
                self.press_key(key['id'])
                return True
        return False

    def draw(self, surface):
        for key in self.keys:
            if not key['is_black']:
                img = key['pressed_img'] if key['is_pressed'] else key['image']
                surface.blit(img, key['rect'])
                
                if key['key_label']:
                    label = self.font.render(key['key_label'], True, (50, 50, 50))
                    label_pos = (key['rect'].x + key['rect'].width // 2 - label.get_width() // 2,
                                key['rect'].y + key['rect'].height - 30)
                    surface.blit(label, label_pos)
        
        for key in self.keys:
            if key['is_black']:
                img = key['pressed_img'] if key['is_pressed'] else key['image']
                surface.blit(img, key['rect'])
                
                if key['key_label']:
                    label = self.black_font.render(key['key_label'], True, (255, 255, 255))
                    label_pos = (key['rect'].x + key['rect'].width // 2 - label.get_width() // 2,
                                key['rect'].y + key['rect'].height - 20)
                    surface.blit(label, label_pos)
    
    def get_key_at_pos(self, pos):
        for key in self.keys:
            if key['is_black'] and key['rect'].collidepoint(pos):
                return key
        
        for key in self.keys:
            if not key['is_black'] and key['rect'].collidepoint(pos):
                return key
        
        return None
    
    def press_key(self, key_id):
        for key in self.keys:
            if key['id'] == key_id:
                key['is_pressed'] = True
                return key['note']
        return None
    
    def release_key(self, key_id):
        for key in self.keys:
            if key['id'] == key_id:
                key['is_pressed'] = False
                return True
        return False


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1000, 400))
    clock = pg.time.Clock()
    
    keyboard = PianoKeyboard(key_width=60)
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                key = keyboard.get_key_at_pos(event.pos)
                if key:
                    print(f"Pressed: {key['note']}")
                    keyboard.press_key(key['id'])
            elif event.type == pg.MOUSEBUTTONUP:
                for key in keyboard.keys:
                    if key['is_pressed']:
                        keyboard.release_key(key['id'])
        
        screen.fill((100, 100, 100))
        keyboard.draw(screen)
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()