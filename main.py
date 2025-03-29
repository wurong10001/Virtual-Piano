import os
import numpy as np
import simpleaudio as sa
from scipy.io import wavfile
import tkinter as tk
import threading
import time

# 配置参数
CACHE_DIR = 'piano_cache'      # 缓存目录
SAMPLE_RATE = 44100            # 采样率（Hz）
VOLUME = 0.5                   # 音量（0.0到1.0）
DURATION = 0.5                 # 每个音符的持续时间（秒）

# 钢琴键与频率映射
notes = {
    'a': {'note': 'C4', 'frequency': 261.63},
    's': {'note': 'D4', 'frequency': 293.66},
    'd': {'note': 'E4', 'frequency': 329.63},
    'f': {'note': 'F4', 'frequency': 349.23},
    'g': {'note': 'G4', 'frequency': 392.00},
    'h': {'note': 'A4', 'frequency': 440.00},
    'j': {'note': 'B4', 'frequency': 493.88},
    'k': {'note': 'C5', 'frequency': 523.25},
    'l': {'note': 'D5', 'frequency': 587.33},
    'z': {'note': 'E5', 'frequency': 659.25},
    'x': {'note': 'F5', 'frequency': 698.46},
    'c': {'note': 'G5', 'frequency': 783.99},
    'v': {'note': 'A5', 'frequency': 880.00},
    'b': {'note': 'B5', 'frequency': 987.77},
    'n': {'note': 'C6', 'frequency': 1046.50},
}

# 初始化缓存目录
os.makedirs(CACHE_DIR, exist_ok=True)

# 音效类型
effect_choice = 'piano'  # 默认是钢琴

def generate_piano_tone(frequency=440.0, duration=1.0, sample_rate=44100, volume=0.5, effect='piano'):
    """
    生成指定频率和时长的钢琴音色正弦波音频信号。
    :param frequency: 频率（Hz）
    :param duration: 持续时间（秒）
    :param sample_rate: 采样率（Hz）
    :param volume: 音量（0.0到1.0）
    :param effect: 音效类型 ('piano' 或 'organ')
    :return: 音频数据（numpy数组）
    """
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    if effect == 'organ':
        # 风琴的波形（方波）
        audio = volume * np.sign(np.sin(2 * np.pi * frequency * t))
    else:
        # 钢琴的波形（正弦波）
        audio = volume * np.sin(2 * np.pi * frequency * t)
    
    # 添加谐波
    harmonics = [
        (2, 0.5),   # 二次谐波
        (3, 0.3),   # 三次谐波
        (4, 0.2)    # 四次谐波
    ]
    
    for harmonic, coeff in harmonics:
        audio += volume * coeff * np.sin(2 * np.pi * harmonic * frequency * t)
    
    # 归一化
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    return audio

def cache_audio(progress_callback):
    """
    生成所有钢琴音符的音频并缓存到文件中，同时更新进度条。
    """
    print("第一次启动，正在生成并缓存钢琴音频数据...")
    total_notes = len(notes)
    for idx, (key, info) in enumerate(notes.items()):
        freq = info['frequency']
        audio = generate_piano_tone(freq, DURATION, SAMPLE_RATE, VOLUME, effect_choice)
        filename = os.path.join(CACHE_DIR, f"{info['note']}.wav")
        wavfile.write(filename, SAMPLE_RATE, audio)
        
        # 更新进度条
        progress_callback(idx + 1, total_notes)

    print("所有音频数据已缓存。")

def load_audio(note):
    """
    加载缓存的钢琴音频数据。
    :param note: 音符名称（如 'C4'）
    :return: 音频数据（numpy数组）和采样率
    """
    filename = os.path.join(CACHE_DIR, f"{note}.wav")
    sample_rate, audio = wavfile.read(filename)
    return audio, sample_rate

def play_audio(note):
    """
    播放指定的钢琴音频。
    :param note: 音符名称（如 'C4'）
    """
    audio, sample_rate = load_audio(note)
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()

def on_key_press(event, label_display):
    """
    监听键盘输入并播放相应的音符，同时更新显示的键盘和钢琴键关系。
    """
    key = event.char.lower()
    if key in notes:
        info = notes[key]
        note = info['note']
        print(f"播放音符: {note}")
        play_audio(note)

        # 更新显示的键盘和钢琴键对应关系
        label_display.config(text=f"按下的键: {key.upper()} 对应钢琴键: {note}")

    return 'break'  # 阻止系统的默认行为

def start_progress_bar():
    """
    显示一个初始化进度条，加载所有音频数据。
    """
    def progress_callback(current, total):
        progress.set(current / total * 100)  # 更新进度条

    threading.Thread(target=cache_audio, args=(progress_callback,)).start()

def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("键盘弹钢琴")
    root.geometry("800x600")

    # 进度条
    global progress
    progress = tk.DoubleVar()
    progress_bar = tk.Progressbar(root, variable=progress, maximum=100)
    progress_bar.pack(pady=50)

    # 显示按键对应关系的标签
    label_display = tk.Label(root, text="按下键盘上的键来弹奏钢琴！", font=("Arial", 14))
    label_display.pack(pady=20)

    # 开始加载音频文件
    start_progress_bar()

    # 绑定键盘事件到主窗口
    root.bind('<KeyPress>', lambda event: on_key_press(event, label_display))

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()

