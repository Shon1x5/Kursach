import pygame as pg
import os

class PianoKeyboard:
    def __init__(self, start_octave=2, num_octaves=5, key_width=60, key_height=300):

        self.start_octave = start_octave
        self.num_octaves = num_octaves
        self.key_width = key_width
        self.key_height = key_height
        
 
        self.white_key_img = pg.image.load('wt_klavisha.png')
        self.black_key_img = pg.image.load('bl_klavisha.png')
        

        self.white_key_img = pg.transform.scale(self.white_key_img, (key_width, key_height))
        self.black_key_img = pg.transform.scale(self.black_key_img, (key_width // 2 + 3, key_height // 2 + 35))
        

        self.white_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.black_notes = ['C#', 'D#', 'F#', 'G#', 'A#']
        

        self.black_key_positions = {
            'C#': 0.7,
            'D#': 1.7,
            'F#': 3.7,
            'G#': 4.7,
            'A#': 5.7
        }
        

        self.keys = self._create_keyboard()
    
    def _create_keyboard(self):
        """Создает список всех клавиш на клавиатуре с изображениями"""
        keys = []
        key_id = 0
        
        for octave in range(self.start_octave, self.start_octave + self.num_octaves):
            for i, note in enumerate(self.white_notes):
                x = (octave - self.start_octave) * len(self.white_notes) * self.key_width + i * self.key_width
                keys.append({
                    'id': key_id,
                    'note': f"{note}{octave}",
                    'rect': pg.Rect(x, 0, self.key_width, self.key_height),
                    'image': self.white_key_img,
                    'is_black': False,
                    'is_pressed': False,
                    'pressed_img': self._create_pressed_image(self.white_key_img, (200, 200, 200))
                })
                key_id += 1
            
            for note in self.black_notes:
                if note in self.black_key_positions:
                    pos = self.black_key_positions[note]
                    x = (octave - self.start_octave) * len(self.white_notes) * self.key_width + pos * self.key_width
                    keys.append({
                        'id': key_id,
                        'note': f"{note}{octave}",
                        'rect': pg.Rect(x, 0, self.key_width // 2, self.key_height // 2),
                        'image': self.black_key_img,
                        'is_black': True,
                        'is_pressed': False,
                        'pressed_img': self._create_pressed_image(self.black_key_img, (100, 100, 100))
                    })
                    key_id += 1
        
        return keys
    
    def _create_pressed_image(self, original_img, tint_color):
        """Создает изображение для нажатой клавиши"""
        img = original_img.copy()
        overlay = pg.Surface(img.get_size(), pg.SRCALPHA)
        overlay.fill((*tint_color, 128))  # Полупрозрачный цвет
        img.blit(overlay, (0, 0), special_flags=pg.BLEND_MULT)
        return img
    
    def draw(self, surface):
        """Отрисовка клавиатуры на поверхности"""
        for key in self.keys:
            if not key['is_black']:
                img = key['pressed_img'] if key['is_pressed'] else key['image']
                surface.blit(img, key['rect'])
        

        for key in self.keys:
            if key['is_black']:
                img = key['pressed_img'] if key['is_pressed'] else key['image']
                surface.blit(img, key['rect'])
    
    def get_key_at_pos(self, pos):

        for key in self.keys:
            if key['is_black'] and key['rect'].collidepoint(pos):
                return key
        
        for key in self.keys:
            if not key['is_black'] and key['rect'].collidepoint(pos):
                return key
        
        return None
    
    def press_key(self, key_id):
        """Нажатие клавиши по ID"""
        for key in self.keys:
            if key['id'] == key_id:
                key['is_pressed'] = True
                return key['note']
        return None
    
    def release_key(self, key_id):
        """Отпускание клавиши по ID"""
        for key in self.keys:
            if key['id'] == key_id:
                key['is_pressed'] = False
                return True
        return False


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1000, 400))
    clock = pg.time.Clock()
    

    if not os.path.exists('wt_klavisha.png') or not os.path.exists('bl_klavisha.png'):
        print("Ошибка: Не найдены изображения клавиш wt_klavisha.png и bl_klavisha.png")
    else:
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