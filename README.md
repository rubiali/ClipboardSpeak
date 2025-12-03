```markdown
<div align="center">

# 🔊 Clipboard English Reader

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern_UI-1F6AA5?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Edge TTS](https://img.shields.io/badge/Edge_TTS-Neural_Voices-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://github.com/rany2/edge-tts)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A modern Text-to-Speech application that automatically reads English text from your clipboard using Microsoft's neural voices.**

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Voices](#-available-voices) •
[Contributing](#-contributing)

---

<img src="https://raw.githubusercontent.com/yourusername/clipboard-english-reader/main/assets/demo.gif" alt="Demo" width="600">

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- **Automatic Detection** — Instantly reads any text copied to clipboard
- **18 Neural Voices** — Natural-sounding voices from 6 English-speaking regions
- **System Tray** — Runs silently in background
- **Reading History** — Track your last 50 readings

</td>
<td width="50%">

### 🎨 User Experience
- **Modern Dark UI** — Beautiful CustomTkinter interface
- **Volume & Speed Control** — Adjust playback to your preference
- **Random Voice Mode** — Variety with each reading
- **One-Click Preview** — Test any voice instantly

</td>
</tr>
</table>

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10/11 (recommended) or Linux/macOS

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/clipboard-english-reader.git
cd clipboard-english-reader

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

Create a `requirements.txt` file:

```txt
customtkinter>=5.2.0
edge-tts>=6.1.0
pygame>=2.5.0
pyperclip>=1.8.0
pystray>=0.19.0
Pillow>=10.0.0
```

Or install manually:

```bash
pip install customtkinter edge-tts pygame pyperclip pystray Pillow
```

## 📖 Usage

### Starting the Application

```bash
python clipboard_reader.py
```

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. 📋 Copy any English text (Ctrl+C / Cmd+C)               │
│  2. 🔊 Audio plays automatically                            │
│  3. ⏹️  Use Stop button to interrupt if needed              │
│  4. 📥 Minimize to tray to keep running in background       │
└─────────────────────────────────────────────────────────────┘
```

### Interface Overview

| Tab | Description |
|-----|-------------|
| 🏠 **Main** | Control panel with volume, speed, and quick actions |
| 🎤 **Voices** | Browse and select from 18 available voices |
| 📜 **History** | View your reading history with timestamps |
| ⚙️ **Settings** | Configure behavior and preferences |

## 🎤 Available Voices

<details>
<summary><b>🇺🇸 United States (6 voices)</b></summary>

| Voice | Gender | ID |
|-------|--------|-----|
| Aria | Female | `en-US-AriaNeural` |
| Jenny | Female | `en-US-JennyNeural` |
| Michelle | Female | `en-US-MichelleNeural` |
| Guy | Male | `en-US-GuyNeural` |
| Christopher | Male | `en-US-ChristopherNeural` |
| Eric | Male | `en-US-EricNeural` |

</details>

<details>
<summary><b>🇬🇧 United Kingdom (4 voices)</b></summary>

| Voice | Gender | ID |
|-------|--------|-----|
| Sonia | Female | `en-GB-SoniaNeural` |
| Libby | Female | `en-GB-LibbyNeural` |
| Ryan | Male | `en-GB-RyanNeural` |
| Thomas | Male | `en-GB-ThomasNeural` |

</details>

<details>
<summary><b>🇦🇺 Australia (2 voices)</b></summary>

| Voice | Gender | ID |
|-------|--------|-----|
| Natasha | Female | `en-AU-NatashaNeural` |
| William | Male | `en-AU-WilliamNeural` |

</details>

<details>
<summary><b>🇨🇦 Canada (2 voices)</b></summary>

| Voice | Gender | ID |
|-------|--------|-----|
| Clara | Female | `en-CA-ClaraNeural` |
| Liam | Male | `en-CA-LiamNeural` |

</details>

<details>
<summary><b>🇮🇳 India (2 voices)</b></summary>

| Voice | Gender | ID |
|-------|--------|-----|
| Neerja | Female | `en-IN-NeerjaNeural` |
| Prabhat | Male | `en-IN-PrabhatNeural` |

</details>

<details>
<summary><b>🇮🇪 Ireland (2 voices)</b></summary>

| Voice | Gender | ID |
|-------|--------|-----|
| Emily | Female | `en-IE-EmilyNeural` |
| Connor | Male | `en-IE-ConnorNeural` |

</details>

## 🏗️ Project Structure

```
clipboard-english-reader/
├── 📄 clipboard_reader.py    # Main application
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md             # Documentation
├── 📄 LICENSE               # MIT License
└── 📁 assets/               # Images and resources
    └── 📄 demo.gif          # Demo animation
```

## ⚙️ Configuration

### Speed Control

| Value | Description |
|-------|-------------|
| `-50%` | Half speed (slow reading) |
| `0%` | Normal speed |
| `+50%` | 1.5x speed (fast reading) |

### System Tray Options

| Action | Description |
|--------|-------------|
| **Show Window** | Restore the main window |
| **Pause/Resume** | Toggle clipboard monitoring |
| **Stop Audio** | Stop current playback |
| **Exit** | Close the application completely |

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|:----------:|:-------:|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core Language |
| ![CustomTkinter](https://img.shields.io/badge/CustomTkinter-1F6AA5?style=flat-square) | Modern UI Framework |
| ![Edge TTS](https://img.shields.io/badge/Edge_TTS-0078D4?style=flat-square&logo=microsoft&logoColor=white) | Neural Text-to-Speech |
| ![Pygame](https://img.shields.io/badge/Pygame-3DDC84?style=flat-square) | Audio Playback |
| ![Pystray](https://img.shields.io/badge/Pystray-FFA500?style=flat-square) | System Tray Integration |

</div>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Ideas for Contribution

- [ ] Add support for more languages
- [ ] Implement keyboard shortcuts
- [ ] Add text filtering options
- [ ] Create installer/executable
- [ ] Add pronunciation dictionary

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Microsoft Edge TTS](https://github.com/rany2/edge-tts) for the amazing neural voices
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components
- [Pygame](https://www.pygame.org/) for reliable audio playback

---

<div align="center">

**Made with ❤️ for English learners everywhere**

⭐ Star this repo if you find it useful!

</div>
```

---

## 📌 Observações

1. **Substitua** `yourusername` pelo seu usuário do GitHub
2. **Adicione** uma pasta `assets/` com um GIF de demonstração do app
3. **Crie** o arquivo `LICENSE` com a licença MIT se desejar
4. **Ajuste** os badges conforme necessário

### Arquivo LICENSE (MIT) opcional:

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```