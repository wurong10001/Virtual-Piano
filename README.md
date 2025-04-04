# Virtual-Piano

# 模拟钢琴程序

这是一个简单的模拟钢琴程序，通过监听电脑键盘的输入来播放对应的钢琴音符。程序使用了 `tkinter` 来创建图形界面，用户可以通过按下键盘上的特定按键来模拟弹奏钢琴。程序支持音频缓存，以减少加载时间，并提供实时显示按键与钢琴键的对应关系。

## 特性

- **键盘输入控制**：通过监听电脑键盘的输入来模拟钢琴演奏。
- **音频缓存**：程序首次运行时会缓存每个音符的音频数据，避免每次播放时重新生成音频，提高效率。
- **界面显示**：实时显示按下的键对应的钢琴音符。
- **音效选择**：可以通过修改 `effect_choice` 变量选择不同的音效，如钢琴音效或风琴音效。
- **多线程支持**：使用多线程来进行音频文件的加载和播放。

## 依赖

- `numpy`
- `simpleaudio`
- `scipy`
- `tkinter`
- `matplotlib`（可选，用于显示音频波形）

你可以使用以下命令安装依赖：

```bash
pip install numpy simpleaudio scipy matplotlib
使用方法
运行程序： 直接运行 main.py 文件，即可启动程序：

bash
复制代码
python main.py
键盘操作：

程序会监听以下电脑键盘上的按键：

a: C4

s: D4

d: E4

f: F4

g: G4

h: A4

j: B4

k: C5

l: D5

z: E5

x: F5

c: G5

v: A5

b: B5

n: C6

每次按下键盘上的这些键，会播放对应的钢琴音符，并且界面会显示出按键和钢琴键的对应关系。

初始化进度条： 程序在第一次运行时，会加载和缓存每个音符的音频数据。你可以看到一个进度条，显示加载的进度。

选择音效： 你可以在代码中修改 effect_choice 变量来切换不同的音效：

'piano'（钢琴音效，默认）

'organ'（风琴音效）

修改后，重新启动程序即可生效。

项目结构
bash
复制代码
piano_simulator/
│
├── main.py              # 程序主文件
├── piano_cache/         # 音频缓存目录
├── README.md            # 项目说明文档
