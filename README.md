<div align="center">

# 🔊 ClipboardSpeak

### Transforme qualquer texto copiado em áudio instantaneamente

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-blue?style=for-the-badge)]()
[![Edge TTS](https://img.shields.io/badge/Powered%20by-Edge%20TTS-0078D4?style=for-the-badge&logo=microsoft-edge&logoColor=white)]()

<br>

<img src="https://raw.githubusercontent.com/rubiali/ClipboardSpeak/main/assets/demo.gif" alt="ClipboardSpeak Demo" width="600">

<br>

**Copie qualquer texto em inglês e ouça instantaneamente com vozes neurais de alta qualidade.**

[📥 Download](#-instalação) •
[✨ Features](#-features) •
[🚀 Como Usar](#-como-usar) •
[🤝 Contribuir](#-contribuindo)

</div>

---

## 📋 Sobre

**ClipboardSpeak** é uma aplicação moderna de Text-to-Speech que monitora automaticamente sua área de transferência e reproduz qualquer texto em inglês copiado usando as vozes neurais do Microsoft Edge TTS — as mesmas vozes naturais usadas pelo Microsoft Edge.

Perfeito para:
- 📚 **Estudantes de inglês** que querem melhorar a pronúncia
- 👨‍💻 **Desenvolvedores** que leem documentação em inglês
- 📖 **Leitores** que preferem ouvir artigos e textos
- ♿ **Acessibilidade** para usuários com dificuldades visuais

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎤 18 Vozes Neurais
Vozes naturais de 6 países diferentes:
- 🇺🇸 Estados Unidos (6 vozes)
- 🇬🇧 Reino Unido (4 vozes)
- 🇦🇺 Austrália (2 vozes)
- 🇨🇦 Canadá (2 vozes)
- 🇮🇳 Índia (2 vozes)
- 🇮🇪 Irlanda (2 vozes)

</td>
<td width="50%">

### ⚡ Funcionalidades
- 🔄 Monitoramento automático do clipboard
- 🎲 Modo de voz aleatória
- 🔊 Controle de volume em tempo real
- ⚡ Ajuste de velocidade (-50% a +50%)
- 📜 Histórico de leituras
- 📥 Minimiza para System Tray

</td>
</tr>
</table>

### 🎨 Interface Moderna

| Dark Mode | System Tray |
|:---------:|:-----------:|
| Interface elegante com CustomTkinter | Continue ouvindo em segundo plano |
| Abas organizadas e intuitivas | Controle rápido pelo ícone |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/rubiali/ClipboardSpeak.git

# Entre no diretório
cd ClipboardSpeak

# Instale as dependências
pip install -r requirements.txt

# Execute
python main.py
```

### 📦 Dependências

```txt
customtkinter>=5.0.0
edge-tts>=6.1.0
pygame>=2.5.0
pyperclip>=1.8.0
pystray>=0.19.0
Pillow>=10.0.0
```

<details>
<summary><b>📥 Instalação manual das dependências</b></summary>

```bash
pip install customtkinter edge-tts pygame pyperclip pystray Pillow
```

</details>

---

## 🎮 Como Usar

### Uso Básico

1. **Execute** o ClipboardSpeak
2. **Copie** qualquer texto em inglês (Ctrl+C)
3. **Ouça** automaticamente! 🔊

### Controles

| Ação | Descrição |
|------|-----------|
| `📡 Monitoring` | Liga/desliga monitoramento automático |
| `⏹️ Stop` | Para a reprodução atual |
| `▶️ Test Voice` | Testa a voz selecionada |
| `📋 Read Clipboard` | Lê manualmente o clipboard atual |

### ⌨️ Atalhos

- **Ctrl+C** → Copie texto para ouvir automaticamente
- **System Tray** → Clique duplo para restaurar janela

---

## 🏗️ Arquitetura

```
ClipboardSpeak/
├── 📄 main.py    # Aplicação principal
├── 📄 requirements.txt     # Dependências
├── 📄 README.md           # Documentação
├── 📄 LICENSE             # Licença MIT
└── 📁 assets/             # Recursos (ícones, imagens)
```

### 🔧 Tecnologias Utilizadas

<div align="center">

| Tecnologia | Uso |
|:----------:|:---:|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Linguagem principal |
| ![CustomTkinter](https://img.shields.io/badge/CustomTkinter-2B2B2B?style=flat-square&logo=python&logoColor=white) | Interface gráfica moderna |
| ![Edge TTS](https://img.shields.io/badge/Edge_TTS-0078D4?style=flat-square&logo=microsoft-edge&logoColor=white) | Síntese de voz neural |
| ![Pygame](https://img.shields.io/badge/Pygame-3DDC84?style=flat-square&logo=python&logoColor=white) | Reprodução de áudio |

</div>

---

## 🗣️ Vozes Disponíveis

<details>
<summary><b>🇺🇸 Estados Unidos</b></summary>

| Voz | Gênero | ID |
|-----|--------|-----|
| Aria | Feminino | `en-US-AriaNeural` |
| Jenny | Feminino | `en-US-JennyNeural` |
| Michelle | Feminino | `en-US-MichelleNeural` |
| Guy | Masculino | `en-US-GuyNeural` |
| Christopher | Masculino | `en-US-ChristopherNeural` |
| Eric | Masculino | `en-US-EricNeural` |

</details>

<details>
<summary><b>🇬🇧 Reino Unido</b></summary>

| Voz | Gênero | ID |
|-----|--------|-----|
| Sonia | Feminino | `en-GB-SoniaNeural` |
| Libby | Feminino | `en-GB-LibbyNeural` |
| Ryan | Masculino | `en-GB-RyanNeural` |
| Thomas | Masculino | `en-GB-ThomasNeural` |

</details>

<details>
<summary><b>🌏 Outras Regiões</b></summary>

| País | Vozes |
|------|-------|
| 🇦🇺 Austrália | Natasha, William |
| 🇨🇦 Canadá | Clara, Liam |
| 🇮🇳 Índia | Neerja, Prabhat |
| 🇮🇪 Irlanda | Emily, Connor |

</details>

---

## 🛠️ Desenvolvimento

### Executar em modo de desenvolvimento

```bash
# Clone com SSH
git clone git@github.com:rubiali/ClipboardSpeak.git

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Execute
python main.py
```

### 📦 Build Executável (Windows)

```bash
pip install pyinstaller

pyinstaller --onefile --windowed --icon=assets/icon.ico --name=ClipboardSpeak main.py
```

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! 

1. **Fork** o projeto
2. Crie sua **Feature Branch** (`git checkout -b feature/NovaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add: nova feature'`)
4. **Push** para a Branch (`git push origin feature/NovaFeature`)
5. Abra um **Pull Request**

### 💡 Ideias para Contribuir

- [ ] Suporte a mais idiomas
- [ ] Atalhos de teclado globais
- [ ] Configurações persistentes
- [ ] Tradução da interface
- [ ] Tema claro

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👤 Autor

<div align="center">

**Criado com ❤️ por [@rubiali](https://github.com/rubiali)**

[![GitHub](https://img.shields.io/badge/GitHub-rubiali-181717?style=for-the-badge&logo=github)](https://github.com/rubiali)

</div>
```

---

## 📁 Arquivo `requirements.txt`

Crie também este arquivo na raiz do projeto:

```txt
customtkinter>=5.0.0
edge-tts
pygame>=2.5.0
pyperclip>=1.8.0
pystray>=0.19.0
Pillow>=10.0.0
keyboard
```

---