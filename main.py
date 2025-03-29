import os
import numpy as np
import simpleaudio as sa
from scipy.io import wavfile
import tkinter as tk
from tkinter import ttk
import threading

# 配置
CACHE_DIR = 'piano_cache'
SAMPLE_RATE, VOLUME, DURATION = 44100, 0.5, 0.5
NOTES = {
    'a': ('C4', 261.63), 's': ('D4', 293.66), 'd': ('E4', 329.63),
    'f': ('F4', 349.23), 'g': ('G4', 392.00), 'h': ('A4', 440.00),
    'j': ('B4', 493.88), 'k': ('C5', 523.25), 'l': ('D5', 587.33),
    'z': ('E5', 659.25), 'x': ('F5', 698.46), 'c': ('G5', 783.99),
    'v': ('A5', 880.00), 'b': ('B5', 987.77), 'n': ('C6', 1046.50)
}

class PianoApp:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.setup_ui()
        
    def generate_tone(self, freq, effect='piano'):
        t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)
        audio = VOLUME * (np.sign if effect == 'organ' else np.sin)(2 * np.pi * freq * t)
        for h, coeff in [(2,0.5), (3,0.3), (4,0.2)]:
            audio += VOLUME * coeff * np.sin(2 * np.pi * h * freq * t)
        return (audio * 32767 / np.max(np.abs(audio))).astype(np.int16)
    
    def cache_audio(self):
        for key, (note, freq) in NOTES.items():
            wavfile.write(f"{CACHE_DIR}/{note}.wav", SAMPLE_RATE, self.generate_tone(freq))
            self.progress.set((list(NOTES).index(key)+1) / len(NOTES) * 100)
    
    def play_note(self, note):
        sa.play_buffer(*wavfile.read(f"{CACHE_DIR}/{note}.wav")).wait_done()
    
    def on_key_press(self, event):
        if (key := event.keysym.lower()) in NOTES:
            note, _ = NOTES[key]
            self.label.config(text=f"按键: {key.upper()} → 音符: {note}")
            self.buttons[key].config(bg='yellow')
            threading.Thread(target=self.play_note, args=(note,)).start()
        for btn in self.buttons.values():
            btn.config(bg='gray' if btn['bg'] != 'yellow' else 'yellow')
    
    def setup_ui(self):
        # 进度窗口
        self.progress_window = tk.Tk()
        self.progress_window.title("初始化中...")
        self.progress = tk.DoubleVar()
        ttk.Progressbar(self.progress_window, variable=self.progress, maximum=100).pack(pady=20)
        threading.Thread(target=self.cache_audio).start()
        self.progress_window.after(100, self.check_progress)
        
    def check_progress(self):
        if self.progress.get() >= 100:
            self.progress_window.destroy()
            self.create_main_window()
        else:
            self.progress_window.after(100, self.check_progress)
    
    def create_main_window(self):
        # 主窗口
        root = tk.Tk()
        root.title("键盘钢琴")
        self.label = tk.Label(root, text="按下键盘按键演奏!", font=("Arial", 14))
        self.label.pack(pady=20)
        
        frame = tk.Frame(root)
        frame.pack(pady=10)
        self.buttons = {
            key: tk.Button(frame, text=key.upper(), width=4, height=2, bg='gray',
                          command=lambda n=note: self.play_note(n))
            for key, (note, _) in NOTES.items()
        }
        for btn in self.buttons.values():
            btn.pack(side=tk.LEFT, padx=2)
        
        root.bind('<KeyPress>', self.on_key_press)
        root.mainloop()

if __name__ == "__main__":
    PianoApp()
