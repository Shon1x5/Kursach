import pygame as pg
import sqlite3
import numpy as np
from pygame import mixer
from piano_keyboard import PianoKeyboard
import random


# Словарь соответствия клавиш клавиатуры нотам пианино
KEY_BINDINGS = {
    # Белые клавиши (основные)
    pg.K_1: 'C2', pg.K_2: 'D2', pg.K_3: 'E2', pg.K_4: 'F2', pg.K_5: 'G2', pg.K_6: 'A2', pg.K_7: 'B2',
    pg.K_q: 'C3', pg.K_w: 'D3', pg.K_e: 'E3', pg.K_r: 'F3', pg.K_t: 'G3', pg.K_y: 'A3', pg.K_u: 'B3',
    pg.K_a: 'C4', pg.K_s: 'D4', pg.K_d: 'E4', pg.K_f: 'F4', pg.K_g: 'G4', pg.K_h: 'A4', pg.K_j: 'B4',
    pg.K_z: 'C5', pg.K_x: 'D5', pg.K_c: 'E5', pg.K_v: 'F5', pg.K_b: 'G5', pg.K_n: 'A5', pg.K_m: 'B5',
    pg.K_9: 'C6', pg.K_0: 'D6', pg.K_i: 'E6', pg.K_o: 'F6', pg.K_p: 'G6', pg.K_k: 'A6', pg.K_l: 'B6',
    
    # Черные клавиши (Shift + основная)
    (pg.K_LSHIFT, pg.K_1): 'C#2', (pg.K_LSHIFT, pg.K_2): 'D#2',
    (pg.K_LSHIFT, pg.K_4): 'F#2', (pg.K_LSHIFT, pg.K_5): 'G#2', (pg.K_LSHIFT, pg.K_6): 'A#2',
    (pg.K_LSHIFT, pg.K_q): 'C#3', (pg.K_LSHIFT, pg.K_w): 'D#3',
    (pg.K_LSHIFT, pg.K_r): 'F#3', (pg.K_LSHIFT, pg.K_t): 'G#3', (pg.K_LSHIFT, pg.K_y): 'A#3',
    (pg.K_LSHIFT, pg.K_a): 'C#4', (pg.K_LSHIFT, pg.K_s): 'D#4',
    (pg.K_LSHIFT, pg.K_f): 'F#4', (pg.K_LSHIFT, pg.K_g): 'G#4', (pg.K_LSHIFT, pg.K_h): 'A#4',
    (pg.K_LSHIFT, pg.K_z): 'C#5', (pg.K_LSHIFT, pg.K_x): 'D#5',
    (pg.K_LSHIFT, pg.K_v): 'F#5', (pg.K_LSHIFT, pg.K_b): 'G#5', (pg.K_LSHIFT, pg.K_n): 'A#5',
    (pg.K_LSHIFT, pg.K_9): 'C#6', (pg.K_LSHIFT, pg.K_0): 'D#6',
    (pg.K_LSHIFT, pg.K_i): 'F#6', (pg.K_LSHIFT, pg.K_o): 'G#6', (pg.K_LSHIFT, pg.K_p): 'A#6'
}


class PianoSound:
    def __init__(self):
        mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self._load_piano_samples()  # Загрузка сэмплов пианино
    
    
    def _generate_piano_wave(self, freq, duration=1.0, sample_rate=44100):
        """Генерация более реалистичного звука пианино"""
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Основной тон
        wave = np.sin(2 * np.pi * freq * t)
        
        # Добавляем обертоны (характерные для пианино)
        for harmonic in [2, 3, 4, 5]:
            wave += 0.3/harmonic * np.sin(2 * np.pi * freq * harmonic * t)
        
        # Эффект затухания
        envelope = np.exp(-t * 2)  # Экспоненциальное затухание
        wave *= envelope
        
        # Добавляем небольшой шум (имитация молоточков)
        noise = 0.01 * np.random.normal(0, 1, len(t))
        wave += noise
        
        return np.int16(wave * 32767 * 0.3)
    
    
    def _load_piano_samples(self):
        """Создаем сэмплы для всех нот пианино"""
        octaves = [2, 3, 4, 5, 6]  # Октавы от большой до третьей
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Частоты для всех нот
        base_freq = 440.0
        for octave in octaves:
            for i, note in enumerate(notes):
                # Рассчитываем частоту по формуле равномерной темперации
                n = (octave - 4) * 12 + i - 9  # Номер полутона относительно A4
                freq = base_freq * (2 ** (n / 12))
                
                # Генерируем уникальный звук для каждой ноты
                note_name = f"{note}{octave}"
                wave = self._generate_piano_wave(freq)
                self.sounds[note_name] = mixer.Sound(buffer=wave)
    
    def play_note(self, note, volume=0.15):
        """Воспроизведение ноты с регулировкой громкости"""
        if note in self.sounds:
            sound = self.sounds[note]
            sound.set_volume(volume)
            sound.play()

def run_game(login):
    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((1920, 1080))
    bg = pg.image.load("1.png")
    
    # Настройка шрифтов
    font = pg.font.Font('Comic Sans MS.ttf', 40)
    font_small = pg.font.Font('Comic Sans MS.ttf', 25)
    
    # Инициализация клавиатуры
    keyboard = PianoKeyboard(
        start_octave=2,
        num_octaves=5,
        key_width=55,
        key_height=350
    )
    
    # Позиционирование клавиатуры
    keyboard_y = 1080 - keyboard.key_height  # Отступ от нижнего края
    for key in keyboard.keys:
        key['rect'].y = keyboard_y
    
    # Инициализация звуковой системы
    piano_sound = PianoSound()
    
    # Эффекты для нажатых клавиш
    key_effects = {}
    
    # Загрузка данных игрока
    connection = sqlite3.connect('kirieshki.db')
    cursor = connection.cursor()
    cursor.execute('SELECT in_game_time, Click_score FROM users WHERE login = ?', (login,))
    time1, key_presses = cursor.fetchone()
    connection.close()

    # Разбивка времени
    seconds = time1 % 60
    minutes = time1 % 3600 // 60
    hours = time1 // 3600

    clock = pg.time.Clock()
    timer_event = pg.USEREVENT + 1
    pg.time.set_timer(timer_event, 1000)
    
    run = True
    while run:
        screen.blit(bg, (0, 0))
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
            elif e.type == timer_event:
                seconds += 1
                if seconds == 60:
                    seconds = 0
                    minutes += 1
                    if minutes == 60:
                        minutes = 0
                        hours += 1
            elif e.type == pg.MOUSEBUTTONDOWN:
                key = keyboard.get_key_at_pos(e.pos)
                if key:
                    keyboard.press_key(key['id'])
                    # Воспроизводим звук с небольшим случайным variation
                    octave = key['note'][-1]  # Получаем последний символ (номер октавы)
                    
                    if octave == '2':
                        piano_sound.play_note(key['note'], volume=0.7 + random.uniform(0, 0.2))
                    elif octave == '3':
                        piano_sound.play_note(key['note'], volume=0.555 + random.uniform(0, 0.2))
                    elif octave == '4':
                        piano_sound.play_note(key['note'], volume=0.445 + random.uniform(0, 0.2))
                    elif octave == '5':
                        piano_sound.play_note(key['note'], volume=0.3345 + random.uniform(0, 0.2))
                    elif octave == '6':
                        piano_sound.play_note(key['note'], volume=0.22345 + random.uniform(0, 0.2))
                    
                    key_presses += 1
                    
                    # Создаем эффект нажатия
                    key_effects[key['id']] = {
                        'pos': (key['rect'].x + key['rect'].w//2, key['rect'].y + key['rect'].h // 2),
                        'timer': 30,
                        'alpha': 255
                    }
            elif e.type == pg.MOUSEBUTTONUP:
                for key in keyboard.keys:
                    if key['is_pressed']:
                        keyboard.release_key(key['id'])
            elif e.type == pg.KEYDOWN:
                key_presses += 1
                if e.key == pg.K_ESCAPE:
                    run = False
                
                # Получаем текущее состояние модификаторов
                modifiers = pg.key.get_mods()
                shift_pressed = modifiers & pg.KMOD_LSHIFT or modifiers & pg.KMOD_RSHIFT
                
                # Проверяем комбинации с Shift в первую очередь
                if shift_pressed:
                    for (shift_key, key_code), note in [(k, v) for k, v in KEY_BINDINGS.items() if isinstance(k, tuple)]:
                        if e.key == key_code:
                            keyboard.press_key_by_note(note)
                            piano_sound.play_note(note)
                            break
                    else:  # Если не нашли комбинацию с Shift, проверяем обычные клавиши
                        if e.key in KEY_BINDINGS:
                            note = KEY_BINDINGS[e.key]
                            keyboard.press_key_by_note(note)
                            piano_sound.play_note(note)
                else:
                    # Проверяем обычные клавиши
                    if e.key in KEY_BINDINGS:
                        note = KEY_BINDINGS[e.key]
                        keyboard.press_key_by_note(note)
                        piano_sound.play_note(note)

            elif e.type == pg.KEYUP:
                # Отпускаем все клавиши при отпускании любой клавиши
                for key in keyboard.keys:
                    if key['is_pressed']:
                        keyboard.release_key(key['id'])

        # Отрисовка интерфейса
        time_str = "Время: {:02}:{:02}:{:02}".format(hours, minutes, seconds)
        text = font.render(time_str, True, (189, 169, 218))
        pg.draw.rect(screen, (100, 78, 132), (5, 5, text.get_width() + 20, 50), border_radius=10)
        screen.blit(text, (15, -2))

        # Красивое отображение логина
        text3 = font.render(login, True, (200, 230, 255))
        pg.draw.rect(screen, (50, 50, 80), (960 - text3.get_width() // 2 - 10, 5, text3.get_width() + 20, 50), border_radius=10)
        screen.blit(text3, (960 - text3.get_width()//2, 0))
        
        # Счетчик нажатий с иконкой
        score_text = f"Нажатий: {key_presses}"
        score = font.render(score_text, True, (240, 240, 150))
        pg.draw.rect(screen, (80, 80, 50), (1915 - score.get_width() - 30, 5, score.get_width() + 20, 50), border_radius=15)
        screen.blit(score, (1915 - score.get_width() - 20, 0))

        # Отрисовка клавиатуры
        keyboard.draw(screen)
        
        # Отрисовка эффектов нажатия
        for key_id, effect in list(key_effects.items()):
            effect['timer'] -= 1
            effect['alpha'] -= 8
            
            if effect['timer'] <= 0:
                key_effects.pop(key_id)
            else:
                # Рисуем круги расходящиеся от нажатой клавиши
                radius = 50 - effect['timer']
                s = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
                pg.draw.circle(s, (255, 255, 255, effect['alpha']), (radius, radius), radius, 2)
                screen.blit(s, (effect['pos'][0] - radius, effect['pos'][1] - radius))

        pg.display.flip()
        clock.tick(60)

    # Сохранение результатов
    all_time_in_sec = seconds + minutes * 60 + hours * 60 * 60

    connection = sqlite3.connect('kirieshki.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET in_game_time=?, Click_score=? WHERE login=?', 
                  (all_time_in_sec, key_presses, login))
    connection.commit()
    connection.close()

    pg.quit()
