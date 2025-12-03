"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      CLIPBOARD ENGLISH READER                                 ║
║                   Modern TTS App with System Tray                            ║
║                         v1.1 - Enhanced Edition                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
from PIL import Image, ImageDraw
import threading
import asyncio
import tempfile
import random
import time
import os
import sys
import re
from datetime import datetime
from pathlib import Path

import pyperclip
import pygame
import edge_tts
import pystray
import keyboard  # pip install keyboard

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DO TEMA
# ══════════════════════════════════════════════════════════════════════════════

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ══════════════════════════════════════════════════════════════════════════════
# VOZES DISPONÍVEIS (Edge TTS)
# ══════════════════════════════════════════════════════════════════════════════

VOICES = {
    # US Voices
    "🇺🇸 Aria (US Female)": "en-US-AriaNeural",
    "🇺🇸 Jenny (US Female)": "en-US-JennyNeural",
    "🇺🇸 Michelle (US Female)": "en-US-MichelleNeural",
    "🇺🇸 Guy (US Male)": "en-US-GuyNeural",
    "🇺🇸 Christopher (US Male)": "en-US-ChristopherNeural",
    "🇺🇸 Eric (US Male)": "en-US-EricNeural",
    # UK Voices
    "🇬🇧 Sonia (UK Female)": "en-GB-SoniaNeural",
    "🇬🇧 Libby (UK Female)": "en-GB-LibbyNeural",
    "🇬🇧 Ryan (UK Male)": "en-GB-RyanNeural",
    "🇬🇧 Thomas (UK Male)": "en-GB-ThomasNeural",
    # Australian Voices
    "🇦🇺 Natasha (AU Female)": "en-AU-NatashaNeural",
    "🇦🇺 William (AU Male)": "en-AU-WilliamNeural",
    # Canadian Voices
    "🇨🇦 Clara (CA Female)": "en-CA-ClaraNeural",
    "🇨🇦 Liam (CA Male)": "en-CA-LiamNeural",
    # Indian Voices
    "🇮🇳 Neerja (IN Female)": "en-IN-NeerjaNeural",
    "🇮🇳 Prabhat (IN Male)": "en-IN-PrabhatNeural",
    # Irish Voices
    "🇮🇪 Emily (IE Female)": "en-IE-EmilyNeural",
    "🇮🇪 Connor (IE Male)": "en-IE-ConnorNeural",
}

VOICE_CATEGORIES = {
    "🇺🇸 United States": [
        "🇺🇸 Aria (US Female)",
        "🇺🇸 Jenny (US Female)",
        "🇺🇸 Michelle (US Female)",
        "🇺🇸 Guy (US Male)",
        "🇺🇸 Christopher (US Male)",
        "🇺🇸 Eric (US Male)",
    ],
    "🇬🇧 United Kingdom": [
        "🇬🇧 Sonia (UK Female)",
        "🇬🇧 Libby (UK Female)",
        "🇬🇧 Ryan (UK Male)",
        "🇬🇧 Thomas (UK Male)",
    ],
    "🇦🇺 Australia": [
        "🇦🇺 Natasha (AU Female)",
        "🇦🇺 William (AU Male)",
    ],
    "🇨🇦 Canada": [
        "🇨🇦 Clara (CA Female)",
        "🇨🇦 Liam (CA Male)",
    ],
    "🇮🇳 India": [
        "🇮🇳 Neerja (IN Female)",
        "🇮🇳 Prabhat (IN Male)",
    ],
    "🇮🇪 Ireland": [
        "🇮🇪 Emily (IE Female)",
        "🇮🇪 Connor (IE Male)",
    ],
}

# Mapeamento de regiões para filtro de voz aleatória
RANDOM_VOICE_FILTERS = {
    "🌍 All Voices": None,  # None = todas as vozes
    "🇺🇸 US Only": "🇺🇸 United States",
    "🇬🇧 UK Only": "🇬🇧 United Kingdom",
    "🇦🇺 Australia Only": "🇦🇺 Australia",
    "🇨🇦 Canada Only": "🇨🇦 Canada",
    "🇮🇳 India Only": "🇮🇳 India",
    "🇮🇪 Ireland Only": "🇮🇪 Ireland",
    "🇺🇸🇬🇧 US + UK": ["🇺🇸 United States", "🇬🇧 United Kingdom"],
    "🌎 Americas (US + CA)": ["🇺🇸 United States", "🇨🇦 Canada"],
}

# ══════════════════════════════════════════════════════════════════════════════
# ESTADO GLOBAL
# ══════════════════════════════════════════════════════════════════════════════

class AppState:
    last_clipboard = ""
    last_spoken_text = ""  # Último texto falado (para CTRL+R)
    stop_flag = False
    is_monitoring = True
    current_audio_file = None
    volume = 1.0
    rate = "+0%"
    use_random_voice = False
    random_voice_filter = "🌍 All Voices"  # Filtro de região para voz aleatória
    text_history = []
    is_speaking = False
    is_minimized = False
    pending_text = None
    # Configurações de salvamento MP3
    save_mp3_enabled = False
    mp3_save_path = str(Path.home() / "Documents" / "ClipboardReader_Audio")

state = AppState()

# ══════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO PYGAME
# ══════════════════════════════════════════════════════════════════════════════

pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=512)

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE ÁUDIO
# ══════════════════════════════════════════════════════════════════════════════

def cleanup_audio():
    """Limpa arquivo de áudio anterior."""
    if state.current_audio_file and os.path.exists(state.current_audio_file):
        try:
            pygame.mixer.music.unload()
            # Só deleta se não for arquivo salvo pelo usuário
            if tempfile.gettempdir() in state.current_audio_file:
                os.unlink(state.current_audio_file)
        except Exception:
            pass

def play_audio(path):
    """Reproduz arquivo de áudio."""
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        cleanup_audio()
        
        if not os.path.exists(path) or os.path.getsize(path) < 100:
            return False
        
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(state.volume)
        pygame.mixer.music.play()
        state.current_audio_file = path
        state.is_speaking = True
        return True
    except Exception as e:
        print(f"[ERRO] Play: {e}")
        return False

def stop_audio():
    """Para reprodução atual."""
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        state.is_speaking = False
    except Exception:
        pass

def is_audio_playing():
    """Verifica se está reproduzindo."""
    try:
        return pygame.mixer.music.get_busy()
    except Exception:
        return False

# ══════════════════════════════════════════════════════════════════════════════
# ENGINE EDGE-TTS
# ══════════════════════════════════════════════════════════════════════════════

async def generate_tts_async(text, out_path, voice, rate):
    """Gera áudio com edge-tts."""
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(out_path)

def generate_tts(text, out_path, voice, rate="+0%"):
    """Wrapper síncrono para edge-tts."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(generate_tts_async(text, out_path, voice, rate))
        return os.path.exists(out_path) and os.path.getsize(out_path) > 100
    except Exception as e:
        print(f"[ERRO] TTS: {e}")
        return False
    finally:
        loop.close()

def get_random_voice():
    """Retorna uma voz aleatória baseada no filtro selecionado."""
    filter_key = state.random_voice_filter
    filter_value = RANDOM_VOICE_FILTERS.get(filter_key)
    
    if filter_value is None:
        # Todas as vozes
        return random.choice(list(VOICES.values()))
    
    # Coleta vozes das categorias filtradas
    available_voices = []
    
    if isinstance(filter_value, list):
        # Múltiplas categorias
        for category in filter_value:
            if category in VOICE_CATEGORIES:
                for voice_name in VOICE_CATEGORIES[category]:
                    if voice_name in VOICES:
                        available_voices.append(VOICES[voice_name])
    else:
        # Uma única categoria
        if filter_value in VOICE_CATEGORIES:
            for voice_name in VOICE_CATEGORIES[filter_value]:
                if voice_name in VOICES:
                    available_voices.append(VOICES[voice_name])
    
    if available_voices:
        return random.choice(available_voices)
    
    # Fallback para qualquer voz se não encontrar
    return random.choice(list(VOICES.values()))

def sanitize_filename(text, max_length=50):
    """Sanitiza texto para uso como nome de arquivo."""
    # Remove caracteres inválidos
    sanitized = re.sub(r'[<>:"/\\|?*\n\r\t]', '', text)
    # Substitui espaços múltiplos por um único
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    # Limita o tamanho
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rsplit(' ', 1)[0]
    return sanitized or "audio"

def save_mp3_copy(source_path, text):
    """Salva uma cópia do MP3 na pasta configurada."""
    if not state.save_mp3_enabled:
        return None
    
    try:
        # Cria pasta se não existir
        save_dir = Path(state.mp3_save_path)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Gera nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_preview = sanitize_filename(text, 40)
        filename = f"{timestamp}_{text_preview}.mp3"
        
        dest_path = save_dir / filename
        
        # Copia o arquivo
        import shutil
        shutil.copy2(source_path, dest_path)
        
        print(f"[INFO] MP3 salvo: {dest_path}")
        return str(dest_path)
    except Exception as e:
        print(f"[ERRO] Salvar MP3: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# MONITOR DE CLIPBOARD
# ══════════════════════════════════════════════════════════════════════════════

def monitor_clipboard(get_voice, get_rate, on_text_detected=None):
    """Thread que monitora clipboard."""
    while not state.stop_flag:
        try:
            if not state.is_monitoring:
                time.sleep(0.3)
                continue
            
            txt = pyperclip.paste()
            if txt is None:
                txt = ""
            txt = txt.strip()
            
            if not txt or txt == state.last_clipboard:
                time.sleep(0.3)
                continue
            
            state.last_clipboard = txt
            state.last_spoken_text = txt  # Salva para CTRL+R
            
            # Adiciona ao histórico
            timestamp = time.strftime("%H:%M:%S")
            state.text_history.insert(0, {"time": timestamp, "text": txt[:200]})
            if len(state.text_history) > 50:
                state.text_history.pop()
            
            # Guarda texto para callback
            state.pending_text = txt
            
            # Callback para UI
            if on_text_detected and not state.is_minimized:
                on_text_detected(txt)
            
            # Gera áudio
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp.close()
            
            voice = get_voice()
            rate = get_rate()
            
            if generate_tts(txt, tmp.name, voice, rate):
                # Salva cópia se habilitado
                save_mp3_copy(tmp.name, txt)
                play_audio(tmp.name)
            else:
                try:
                    os.unlink(tmp.name)
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"[ERRO] Monitor: {e}")
        
        time.sleep(0.3)

# ══════════════════════════════════════════════════════════════════════════════
# ÍCONE DO SYSTEM TRAY
# ══════════════════════════════════════════════════════════════════════════════

def create_tray_image():
    """Cria imagem para o ícone do tray."""
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Círculo de fundo
    draw.ellipse([(2, 2), (62, 62)], fill=(30, 144, 255, 255))
    
    # Alto-falante
    draw.polygon([(18, 24), (26, 24), (34, 16), (34, 48), (26, 40), (18, 40)], fill='white')
    
    # Ondas de som
    draw.arc([(36, 20), (48, 44)], -60, 60, fill='white', width=3)
    draw.arc([(42, 24), (54, 40)], -50, 50, fill='white', width=3)
    
    return img

def create_tray_icon(app_ref):
    """Cria ícone na bandeja do sistema."""
    
    def on_show(icon, item):
        app_ref.after(0, app_ref._show_from_tray)
    
    def on_pause(icon, item):
        state.is_monitoring = not state.is_monitoring
        app_ref.after(0, app_ref._sync_monitoring_state)
    
    def on_stop(icon, item):
        stop_audio()
    
    def on_reread(icon, item):
        app_ref.after(0, app_ref._reread_last_text)
    
    def on_quit(icon, item):
        app_ref.after(0, app_ref._quit_app)
    
    def get_pause_text(item):
        return "▶️ Resume" if not state.is_monitoring else "⏸️ Pause"
    
    menu = pystray.Menu(
        pystray.MenuItem("📖 Show Window", on_show, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(get_pause_text, on_pause),
        pystray.MenuItem("🔄 Re-read (Ctrl+R)", on_reread),
        pystray.MenuItem("⏹️ Stop Audio", on_stop),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("❌ Exit", on_quit)
    )
    
    icon = pystray.Icon(
        "ClipboardReader",
        create_tray_image(),
        "Clipboard English Reader",
        menu
    )
    
    return icon

# ══════════════════════════════════════════════════════════════════════════════
# INTERFACE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ══════════════════════════════════════════════════════════════════
        # CONFIGURAÇÃO DA JANELA
        # ══════════════════════════════════════════════════════════════════
        
        self.title("Clipboard English Reader")
        self.geometry("600x750")
        self.minsize(550, 700)
        
        # Centraliza na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 750) // 2
        self.geometry(f"+{x}+{y}")
        
        # Variáveis
        self.voice_var = ctk.StringVar(value="🇺🇸 Aria (US Female)")
        self.volume_var = ctk.DoubleVar(value=100)
        self.rate_var = ctk.IntVar(value=0)
        self.monitoring_var = ctk.BooleanVar(value=True)
        self.minimize_to_tray_var = ctk.BooleanVar(value=True)
        self.random_voice_var = ctk.BooleanVar(value=False)
        self.random_filter_var = ctk.StringVar(value="🌍 All Voices")
        self.save_mp3_var = ctk.BooleanVar(value=False)
        self.mp3_path_var = ctk.StringVar(value=state.mp3_save_path)
        
        # Tray icon
        self.tray_icon = None
        self.tray_thread = None
        
        # Flag de UI ativa
        self._ui_update_job = None
        
        # ══════════════════════════════════════════════════════════════════
        # INICIALIZA CLIPBOARD STATE
        # ══════════════════════════════════════════════════════════════════
        
        try:
            initial_clipboard = pyperclip.paste()
            if initial_clipboard:
                state.last_clipboard = initial_clipboard.strip()
        except Exception:
            pass
        
        # ══════════════════════════════════════════════════════════════════
        # CONSTRUÇÃO DA UI
        # ══════════════════════════════════════════════════════════════════
        
        self._create_ui()
        
        # ══════════════════════════════════════════════════════════════════
        # REGISTRA HOTKEY GLOBAL
        # ══════════════════════════════════════════════════════════════════
        
        self._register_global_hotkey()
        
        # ══════════════════════════════════════════════════════════════════
        # INICIA MONITOR
        # ══════════════════════════════════════════════════════════════════
        
        self.monitor_thread = threading.Thread(
            target=monitor_clipboard,
            args=(
                self._get_voice, 
                self._get_rate, 
                self._on_text_detected,
            ),
            daemon=True
        )
        self.monitor_thread.start()
        
        # Handler de fechamento
        self.protocol("WM_DELETE_WINDOW", self._on_close_request)
        
        # Update loop para UI
        self._start_ui_loop()
    
    def _register_global_hotkey(self):
        """Registra hotkey global CTRL+R."""
        try:
            keyboard.add_hotkey('ctrl+r', self._on_global_reread, suppress=False)
            print("[INFO] Hotkey CTRL+R registrada com sucesso")
        except Exception as e:
            print(f"[AVISO] Não foi possível registrar hotkey global: {e}")
    
    def _unregister_global_hotkey(self):
        """Remove hotkey global."""
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
    
    def _on_global_reread(self):
        """Callback para hotkey CTRL+R."""
        # Executa na thread principal
        self.after(0, self._reread_last_text)
    
    def _reread_last_text(self):
        """Relê o último texto falado."""
        if not state.last_spoken_text:
            print("[INFO] Nenhum texto para reler")
            return
        
        def reread_thread():
            try:
                txt = state.last_spoken_text
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tmp.close()
                
                if generate_tts(txt, tmp.name, self._get_voice(), self._get_rate()):
                    # Salva cópia se habilitado
                    save_mp3_copy(tmp.name, txt)
                    play_audio(tmp.name)
            except Exception as e:
                print(f"[ERRO] Re-read: {e}")
        
        threading.Thread(target=reread_thread, daemon=True).start()
    
    def _create_ui(self):
        """Constrói interface."""
        
        # ══════════════════════════════════════════════════════════════════
        # HEADER
        # ══════════════════════════════════════════════════════════════════
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        # Título com ícone
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🔊 Clipboard English Reader",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Copy any English text to hear it spoken • Ctrl+R to repeat",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.pack(anchor="w")
        
        # Status area
        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        self.status_badge = ctk.CTkLabel(
            status_frame,
            text="● READY",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00D26A"
        )
        self.status_badge.pack()
        
        self.speaking_indicator = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#3B8ED0"
        )
        self.speaking_indicator.pack()
        
        # ══════════════════════════════════════════════════════════════════
        # TABVIEW
        # ══════════════════════════════════════════════════════════════════
        
        self.tabview = ctk.CTkTabview(self, corner_radius=15)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Criar abas
        self.tab_main = self.tabview.add("🏠 Main")
        self.tab_voices = self.tabview.add("🎤 Voices")
        self.tab_history = self.tabview.add("📜 History")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        
        # Construir cada aba
        self._build_main_tab()
        self._build_voices_tab()
        self._build_history_tab()
        self._build_settings_tab()
    
    def _build_main_tab(self):
        """Aba principal."""
        
        # Status Card
        status_card = ctk.CTkFrame(self.tab_main, corner_radius=12)
        status_card.pack(fill="x", padx=10, pady=(10, 5))
        
        status_inner = ctk.CTkFrame(status_card, fg_color="transparent")
        status_inner.pack(fill="x", padx=15, pady=12)
        
        # Monitoring toggle grande
        monitor_label = ctk.CTkLabel(
            status_inner,
            text="📡 Clipboard Monitoring",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        monitor_label.pack(side="left")
        
        self.monitor_switch = ctk.CTkSwitch(
            status_inner,
            text="",
            variable=self.monitoring_var,
            command=self._toggle_monitoring,
            onvalue=True,
            offvalue=False,
            width=50
        )
        self.monitor_switch.pack(side="right")
        
        # Current Voice Display
        voice_card = ctk.CTkFrame(self.tab_main, corner_radius=12)
        voice_card.pack(fill="x", padx=10, pady=5)
        
        voice_inner = ctk.CTkFrame(voice_card, fg_color="transparent")
        voice_inner.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            voice_inner,
            text="🎤 Current Voice:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")
        
        self.current_voice_label = ctk.CTkLabel(
            voice_inner,
            text=self.voice_var.get(),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3B8ED0"
        )
        self.current_voice_label.pack(side="right")
        
        # Quick Controls
        controls_card = ctk.CTkFrame(self.tab_main, corner_radius=12)
        controls_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            controls_card,
            text="🎮 Quick Controls",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 8))
        
        btn_frame = ctk.CTkFrame(controls_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏹️ Stop",
            width=80,
            height=40,
            corner_radius=10,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=stop_audio
        )
        self.stop_btn.pack(side="left", padx=(0, 6))
        
        self.reread_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Re-read",
            width=95,
            height=40,
            corner_radius=10,
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            command=self._reread_last_text
        )
        self.reread_btn.pack(side="left", padx=(0, 6))
        
        self.preview_btn = ctk.CTkButton(
            btn_frame,
            text="▶️ Test",
            width=80,
            height=40,
            corner_radius=10,
            command=self._preview_voice
        )
        self.preview_btn.pack(side="left", padx=(0, 6))
        
        self.read_btn = ctk.CTkButton(
            btn_frame,
            text="📋 Read Clipboard",
            width=130,
            height=40,
            corner_radius=10,
            fg_color="#27AE60",
            hover_color="#1E8449",
            command=self._read_current_clipboard
        )
        self.read_btn.pack(side="left")
        
        # Hotkey hint
        hotkey_hint = ctk.CTkLabel(
            controls_card,
            text="💡 Press Ctrl+R anywhere to re-read last text",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        hotkey_hint.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Volume Control
        vol_card = ctk.CTkFrame(self.tab_main, corner_radius=12)
        vol_card.pack(fill="x", padx=10, pady=5)
        
        vol_header = ctk.CTkFrame(vol_card, fg_color="transparent")
        vol_header.pack(fill="x", padx=15, pady=(12, 5))
        
        ctk.CTkLabel(
            vol_header,
            text="🔊 Volume",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        self.vol_label = ctk.CTkLabel(
            vol_header,
            text="100%",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B8ED0"
        )
        self.vol_label.pack(side="right")
        
        self.vol_slider = ctk.CTkSlider(
            vol_card,
            from_=0,
            to=100,
            variable=self.volume_var,
            command=self._on_volume_change
        )
        self.vol_slider.pack(fill="x", padx=15, pady=(0, 12))
        
        # Speed Control
        speed_card = ctk.CTkFrame(self.tab_main, corner_radius=12)
        speed_card.pack(fill="x", padx=10, pady=5)
        
        speed_header = ctk.CTkFrame(speed_card, fg_color="transparent")
        speed_header.pack(fill="x", padx=15, pady=(12, 5))
        
        ctk.CTkLabel(
            speed_header,
            text="⚡ Speed",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        self.rate_label = ctk.CTkLabel(
            speed_header,
            text="Normal",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B8ED0"
        )
        self.rate_label.pack(side="right")
        
        self.rate_slider = ctk.CTkSlider(
            speed_card,
            from_=-50,
            to=50,
            variable=self.rate_var,
            command=self._on_rate_change
        )
        self.rate_slider.pack(fill="x", padx=15, pady=(0, 12))
        
        # Last Text Preview
        text_card = ctk.CTkFrame(self.tab_main, corner_radius=12)
        text_card.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        text_header = ctk.CTkFrame(text_card, fg_color="transparent")
        text_header.pack(fill="x", padx=15, pady=(12, 5))
        
        ctk.CTkLabel(
            text_header,
            text="📝 Last Detected Text",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        self.char_count_label = ctk.CTkLabel(
            text_header,
            text="0 chars",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.char_count_label.pack(side="right")
        
        self.text_display = ctk.CTkTextbox(
            text_card,
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            state="disabled",
            wrap="word"
        )
        self.text_display.pack(fill="both", expand=True, padx=15, pady=(0, 12))
    
    def _build_voices_tab(self):
        """Aba de vozes."""
        
        # Random Voice Option
        random_card = ctk.CTkFrame(self.tab_voices, corner_radius=12)
        random_card.pack(fill="x", padx=10, pady=(10, 5))
        
        random_inner = ctk.CTkFrame(random_card, fg_color="transparent")
        random_inner.pack(fill="x", padx=15, pady=12)
        
        random_left = ctk.CTkFrame(random_inner, fg_color="transparent")
        random_left.pack(side="left")
        
        ctk.CTkLabel(
            random_left,
            text="🎲 Random Voice",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            random_left,
            text="Use a different voice each time",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w")
        
        self.random_switch = ctk.CTkSwitch(
            random_inner,
            text="",
            variable=self.random_voice_var,
            command=self._toggle_random_voice,
            onvalue=True,
            offvalue=False
        )
        self.random_switch.pack(side="right")
        
        # Random Voice Filter (Região)
        filter_card = ctk.CTkFrame(self.tab_voices, corner_radius=12)
        filter_card.pack(fill="x", padx=10, pady=5)
        
        filter_inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        filter_inner.pack(fill="x", padx=15, pady=12)
        
        filter_left = ctk.CTkFrame(filter_inner, fg_color="transparent")
        filter_left.pack(side="left")
        
        ctk.CTkLabel(
            filter_left,
            text="🌍 Random Voice Region",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            filter_left,
            text="Filter which accents to use in random mode",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w")
        
        self.random_filter_combo = ctk.CTkComboBox(
            filter_inner,
            variable=self.random_filter_var,
            values=list(RANDOM_VOICE_FILTERS.keys()),
            width=180,
            command=self._on_random_filter_change,
            state="readonly"
        )
        self.random_filter_combo.pack(side="right")
        
        # Voice Selection
        select_card = ctk.CTkFrame(self.tab_voices, corner_radius=12)
        select_card.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            select_card,
            text="🎤 Select Voice",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 8))
        
        # Scrollable frame para vozes
        voice_scroll = ctk.CTkScrollableFrame(
            select_card,
            corner_radius=8
        )
        voice_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        
        # Criar radio buttons por categoria
        self.voice_radios = []
        for category, voices in VOICE_CATEGORIES.items():
            # Header da categoria
            cat_label = ctk.CTkLabel(
                voice_scroll,
                text=category,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#3B8ED0"
            )
            cat_label.pack(anchor="w", pady=(10, 5))
            
            for voice_name in voices:
                radio_frame = ctk.CTkFrame(voice_scroll, fg_color="transparent")
                radio_frame.pack(fill="x", pady=2)
                
                radio = ctk.CTkRadioButton(
                    radio_frame,
                    text=voice_name,
                    variable=self.voice_var,
                    value=voice_name,
                    command=self._on_voice_change,
                    font=ctk.CTkFont(size=13)
                )
                radio.pack(side="left")
                
                # Botão de preview individual
                preview_btn = ctk.CTkButton(
                    radio_frame,
                    text="▶️",
                    width=30,
                    height=25,
                    corner_radius=5,
                    command=lambda v=voice_name: self._preview_specific_voice(v)
                )
                preview_btn.pack(side="right", padx=5)
                
                self.voice_radios.append(radio)
    
    def _build_history_tab(self):
        """Aba de histórico."""
        
        # Header
        header_frame = ctk.CTkFrame(self.tab_history, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="📜 Reading History",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="left")
        
        clear_btn = ctk.CTkButton(
            header_frame,
            text="🗑️ Clear All",
            width=100,
            height=30,
            corner_radius=8,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self._clear_history
        )
        clear_btn.pack(side="right")
        
        # History List
        self.history_frame = ctk.CTkScrollableFrame(
            self.tab_history,
            corner_radius=12
        )
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Placeholder
        self.history_placeholder = ctk.CTkLabel(
            self.history_frame,
            text="No history yet.\nCopy some text to get started!",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.history_placeholder.pack(pady=50)
    
    def _build_settings_tab(self):
        """Aba de configurações."""
        
        # ══════════════════════════════════════════════════════════════════
        # SAVE MP3 SETTINGS
        # ══════════════════════════════════════════════════════════════════
        
        mp3_card = ctk.CTkFrame(self.tab_settings, corner_radius=12)
        mp3_card.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            mp3_card,
            text="💾 Save MP3 for Offline Study",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 8))
        
        # Toggle para salvar MP3
        mp3_toggle_frame = ctk.CTkFrame(mp3_card, fg_color="transparent")
        mp3_toggle_frame.pack(fill="x", padx=15, pady=5)
        
        mp3_left = ctk.CTkFrame(mp3_toggle_frame, fg_color="transparent")
        mp3_left.pack(side="left")
        
        ctk.CTkLabel(
            mp3_left,
            text="Auto-save audio files",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            mp3_left,
            text="Save a copy of each audio for later playback",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w")
        
        self.save_mp3_switch = ctk.CTkSwitch(
            mp3_toggle_frame,
            text="",
            variable=self.save_mp3_var,
            command=self._toggle_save_mp3,
            onvalue=True,
            offvalue=False
        )
        self.save_mp3_switch.pack(side="right")
        
        # Pasta de destino
        path_frame = ctk.CTkFrame(mp3_card, fg_color="transparent")
        path_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            path_frame,
            text="📁 Save Location:",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w")
        
        path_input_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_input_frame.pack(fill="x", pady=5)
        
        self.mp3_path_entry = ctk.CTkEntry(
            path_input_frame,
            textvariable=self.mp3_path_var,
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.mp3_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        browse_btn = ctk.CTkButton(
            path_input_frame,
            text="📂 Browse",
            width=90,
            height=35,
            corner_radius=8,
            command=self._browse_mp3_folder
        )
        browse_btn.pack(side="right")
        
        open_folder_btn = ctk.CTkButton(
            mp3_card,
            text="📂 Open Saved Files Folder",
            width=200,
            height=32,
            corner_radius=8,
            fg_color="#27AE60",
            hover_color="#1E8449",
            command=self._open_mp3_folder
        )
        open_folder_btn.pack(anchor="w", padx=15, pady=(5, 12))
        
        # ══════════════════════════════════════════════════════════════════
        # BEHAVIOR SETTINGS
        # ══════════════════════════════════════════════════════════════════
        
        behavior_card = ctk.CTkFrame(self.tab_settings, corner_radius=12)
        behavior_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            behavior_card,
            text="🔧 Behavior",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 8))
        
        # Minimize to tray
        tray_frame = ctk.CTkFrame(behavior_card, fg_color="transparent")
        tray_frame.pack(fill="x", padx=15, pady=5)
        
        tray_left = ctk.CTkFrame(tray_frame, fg_color="transparent")
        tray_left.pack(side="left")
        
        ctk.CTkLabel(
            tray_left,
            text="📥 Minimize to System Tray",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            tray_left,
            text="Keep running in background when closed",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w")
        
        self.tray_switch = ctk.CTkSwitch(
            tray_frame,
            text="",
            variable=self.minimize_to_tray_var,
            onvalue=True,
            offvalue=False
        )
        self.tray_switch.pack(side="right")
        
        # Separator
        ctk.CTkFrame(behavior_card, height=1, fg_color="gray").pack(fill="x", padx=15, pady=10)
        
        # Auto-start info
        auto_frame = ctk.CTkFrame(behavior_card, fg_color="transparent")
        auto_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        ctk.CTkLabel(
            auto_frame,
            text="ℹ️ Tip: Add to startup for automatic launch",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w")
        
        # ══════════════════════════════════════════════════════════════════
        # KEYBOARD SHORTCUTS
        # ══════════════════════════════════════════════════════════════════
        
        shortcuts_card = ctk.CTkFrame(self.tab_settings, corner_radius=12)
        shortcuts_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            shortcuts_card,
            text="⌨️ Keyboard Shortcuts",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 8))
        
        shortcuts = [
            ("Ctrl+C", "Copy text → Auto-read"),
            ("Ctrl+R", "Re-read last text (global hotkey)"),
        ]
        
        for key, desc in shortcuts:
            shortcut_frame = ctk.CTkFrame(shortcuts_card, fg_color="transparent")
            shortcut_frame.pack(fill="x", padx=15, pady=3)
            
            key_label = ctk.CTkLabel(
                shortcut_frame,
                text=key,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#3B8ED0",
                width=80
            )
            key_label.pack(side="left")
            
            ctk.CTkLabel(
                shortcut_frame,
                text=desc,
                font=ctk.CTkFont(size=12)
            ).pack(side="left")
        
        ctk.CTkFrame(shortcuts_card, height=10, fg_color="transparent").pack()
        
        # ══════════════════════════════════════════════════════════════════
        # ABOUT
        # ══════════════════════════════════════════════════════════════════
        
        about_card = ctk.CTkFrame(self.tab_settings, corner_radius=12)
        about_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            about_card,
            text="ℹ️ About",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 8))
        
        about_text = """Clipboard English Reader v1.1

Features:
• 18 natural-sounding voices from 6 regions
• Global Ctrl+R hotkey to re-read
• Save MP3 for offline study
• Random voice with region filter
• Adjustable volume and speed"""
        
        ctk.CTkLabel(
            about_card,
            text=about_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(0, 12))
    
    # ══════════════════════════════════════════════════════════════════════
    # CALLBACKS
    # ══════════════════════════════════════════════════════════════════════
    
    def _get_voice(self):
        """Retorna código da voz selecionada."""
        if self.random_voice_var.get():
            return get_random_voice()
        return VOICES.get(self.voice_var.get(), "en-US-AriaNeural")
    
    def _get_rate(self):
        """Retorna rate formatado."""
        rate = self.rate_var.get()
        if rate >= 0:
            return f"+{rate}%"
        return f"{rate}%"
    
    def _on_volume_change(self, value):
        """Atualiza volume."""
        vol = int(value)
        self.vol_label.configure(text=f"{vol}%")
        state.volume = vol / 100
        try:
            pygame.mixer.music.set_volume(state.volume)
        except Exception:
            pass
    
    def _on_rate_change(self, value):
        """Atualiza velocidade."""
        rate = int(value)
        if rate == 0:
            text = "Normal"
        elif rate > 0:
            text = f"+{rate}%"
        else:
            text = f"{rate}%"
        self.rate_label.configure(text=text)
        state.rate = self._get_rate()
    
    def _on_voice_change(self):
        """Callback quando voz muda."""
        voice = self.voice_var.get()
        self.current_voice_label.configure(text=voice)
        # Desativa random se selecionar voz específica
        if self.random_voice_var.get():
            self.random_voice_var.set(False)
            state.use_random_voice = False
    
    def _on_random_filter_change(self, value):
        """Callback quando filtro de voz aleatória muda."""
        state.random_voice_filter = value
    
    def _toggle_monitoring(self):
        """Alterna monitoramento."""
        state.is_monitoring = self.monitoring_var.get()
        self._update_status_badge()
    
    def _toggle_random_voice(self):
        """Alterna modo de voz aleatória."""
        state.use_random_voice = self.random_voice_var.get()
        if state.use_random_voice:
            filter_text = self.random_filter_var.get()
            self.current_voice_label.configure(text=f"🎲 Random ({filter_text})")
        else:
            self.current_voice_label.configure(text=self.voice_var.get())
    
    def _toggle_save_mp3(self):
        """Alterna salvamento de MP3."""
        state.save_mp3_enabled = self.save_mp3_var.get()
        state.mp3_save_path = self.mp3_path_var.get()
        
        if state.save_mp3_enabled:
            # Cria pasta se não existir
            try:
                Path(state.mp3_save_path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"[ERRO] Criar pasta MP3: {e}")
    
    def _browse_mp3_folder(self):
        """Abre diálogo para escolher pasta."""
        from tkinter import filedialog
        
        folder = filedialog.askdirectory(
            initialdir=self.mp3_path_var.get(),
            title="Select folder to save MP3 files"
        )
        
        if folder:
            self.mp3_path_var.set(folder)
            state.mp3_save_path = folder
    
    def _open_mp3_folder(self):
        """Abre pasta de MP3 no explorador."""
        folder = self.mp3_path_var.get()
        
        # Cria pasta se não existir
        try:
            Path(folder).mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        
        # Abre no explorador de arquivos
        if sys.platform == 'win32':
            os.startfile(folder)
        elif sys.platform == 'darwin':
            os.system(f'open "{folder}"')
        else:
            os.system(f'xdg-open "{folder}"')
    
    def _sync_monitoring_state(self):
        """Sincroniza estado de monitoramento com UI."""
        if state.is_minimized:
            return
        self.monitoring_var.set(state.is_monitoring)
        self._update_status_badge()
    
    def _update_status_badge(self):
        """Atualiza badge de status."""
        if state.is_minimized:
            return
        if state.is_monitoring:
            self.status_badge.configure(text="● READY", text_color="#00D26A")
        else:
            self.status_badge.configure(text="● PAUSED", text_color="#F39C12")
    
    def _preview_voice(self):
        """Reproduz preview da voz selecionada."""
        def preview_thread():
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp.close()
            
            text = "Hello! This is a preview of the selected voice."
            voice = self._get_voice()
            if generate_tts(text, tmp.name, voice, self._get_rate()):
                play_audio(tmp.name)
        
        threading.Thread(target=preview_thread, daemon=True).start()
    
    def _preview_specific_voice(self, voice_name):
        """Preview de uma voz específica."""
        def preview_thread():
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp.close()
            
            text = "Hello! This is how I sound."
            voice = VOICES.get(voice_name, "en-US-AriaNeural")
            if generate_tts(text, tmp.name, voice, self._get_rate()):
                play_audio(tmp.name)
        
        threading.Thread(target=preview_thread, daemon=True).start()
    
    def _read_current_clipboard(self):
        """Lê o conteúdo atual do clipboard manualmente."""
        def read_thread():
            try:
                txt = pyperclip.paste()
                if txt and txt.strip():
                    txt = txt.strip()
                    state.last_spoken_text = txt  # Salva para CTRL+R
                    
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tmp.close()
                    
                    if generate_tts(txt, tmp.name, self._get_voice(), self._get_rate()):
                        # Salva cópia se habilitado
                        save_mp3_copy(tmp.name, txt)
                        play_audio(tmp.name)
                        state.pending_text = txt
            except Exception as e:
                print(f"[ERRO] Read clipboard: {e}")
        
        threading.Thread(target=read_thread, daemon=True).start()
    
    def _clear_history(self):
        """Limpa histórico."""
        state.last_clipboard = ""
        state.last_spoken_text = ""
        state.text_history.clear()
        state.pending_text = None
        
        # Limpa display principal
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")
        self.text_display.configure(state="disabled")
        self.char_count_label.configure(text="0 chars")
        
        # Limpa histórico visual
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        self.history_placeholder = ctk.CTkLabel(
            self.history_frame,
            text="No history yet.\nCopy some text to get started!",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.history_placeholder.pack(pady=50)
    
    def _on_text_detected(self, text):
        """Callback quando texto é detectado (chamado da thread)."""
        if state.is_minimized:
            return
        
        try:
            self.after(0, lambda: self._update_text_display(text))
        except Exception:
            pass
    
    def _update_text_display(self, text):
        """Atualiza display de texto (executado na thread principal)."""
        if state.is_minimized:
            return
            
        try:
            self.text_display.configure(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("1.0", text)
            self.text_display.configure(state="disabled")
            self.char_count_label.configure(text=f"{len(text)} chars")
            
            self._update_history_display()
        except Exception as e:
            print(f"[ERRO] Update display: {e}")
    
    def _update_history_display(self):
        """Atualiza display do histórico."""
        if state.is_minimized:
            return
            
        try:
            if hasattr(self, 'history_placeholder'):
                try:
                    if self.history_placeholder.winfo_exists():
                        self.history_placeholder.destroy()
                except Exception:
                    pass
            
            for widget in self.history_frame.winfo_children():
                try:
                    widget.destroy()
                except Exception:
                    pass
            
            for item in state.text_history[:20]:
                item_frame = ctk.CTkFrame(self.history_frame, corner_radius=8)
                item_frame.pack(fill="x", pady=3)
                
                # Header com timestamp e botão de replay
                header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(8, 2))
                
                ctk.CTkLabel(
                    header_frame,
                    text=item["time"],
                    font=ctk.CTkFont(size=11),
                    text_color="#3B8ED0"
                ).pack(side="left")
                
                # Botão para reler este item
                replay_btn = ctk.CTkButton(
                    header_frame,
                    text="🔄",
                    width=28,
                    height=22,
                    corner_radius=5,
                    font=ctk.CTkFont(size=11),
                    command=lambda t=item["text"]: self._replay_history_item(t)
                )
                replay_btn.pack(side="right")
                
                preview = item["text"][:100] + ("..." if len(item["text"]) > 100 else "")
                ctk.CTkLabel(
                    item_frame,
                    text=preview,
                    font=ctk.CTkFont(size=12),
                    wraplength=400,
                    justify="left"
                ).pack(anchor="w", padx=10, pady=(0, 8))
                
        except Exception as e:
            print(f"[ERRO] Update history: {e}")
    
    def _replay_history_item(self, text):
        """Reproduz um item do histórico."""
        def replay_thread():
            try:
                state.last_spoken_text = text
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tmp.close()
                
                if generate_tts(text, tmp.name, self._get_voice(), self._get_rate()):
                    save_mp3_copy(tmp.name, text)
                    play_audio(tmp.name)
            except Exception as e:
                print(f"[ERRO] Replay: {e}")
        
        threading.Thread(target=replay_thread, daemon=True).start()
    
    def _start_ui_loop(self):
        """Inicia loop de atualização da UI."""
        self._update_ui_loop()
    
    def _stop_ui_loop(self):
        """Para loop de atualização da UI."""
        if self._ui_update_job:
            try:
                self.after_cancel(self._ui_update_job)
            except Exception:
                pass
            self._ui_update_job = None
    
    def _update_ui_loop(self):
        """Loop de atualização da UI."""
        if state.is_minimized or state.stop_flag:
            return
        
        try:
            is_playing = is_audio_playing()
            if is_playing:
                self.speaking_indicator.configure(text="🔊 Speaking...")
            else:
                self.speaking_indicator.configure(text="")
            
            if state.pending_text and not state.is_minimized:
                self._update_text_display(state.pending_text)
                state.pending_text = None
                
        except Exception as e:
            print(f"[ERRO] UI Loop: {e}")
        
        if not state.stop_flag and not state.is_minimized:
            self._ui_update_job = self.after(200, self._update_ui_loop)
    
    # ══════════════════════════════════════════════════════════════════════
    # SYSTEM TRAY
    # ══════════════════════════════════════════════════════════════════════
    
    def _minimize_to_tray(self):
        """Minimiza para bandeja do sistema."""
        state.is_minimized = True
        self._stop_ui_loop()
        self.withdraw()
        
        if self.tray_icon is None:
            self.tray_icon = create_tray_icon(self)
            self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            self.tray_thread.start()
    
    def _show_from_tray(self):
        """Mostra janela a partir do tray."""
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
            self.tray_icon = None
        
        state.is_minimized = False
        
        self.deiconify()
        self.lift()
        self.focus_force()
        
        self._start_ui_loop()
        self._sync_monitoring_state()
        
        if state.pending_text:
            self.after(100, lambda: self._update_text_display(state.pending_text))
            state.pending_text = None
        
        self.after(200, self._update_history_display)
    
    def _quit_app(self):
        """Encerra aplicação."""
        state.stop_flag = True
        state.is_minimized = True
        
        self._stop_ui_loop()
        self._unregister_global_hotkey()
        
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
            self.tray_icon = None
        
        try:
            stop_audio()
            pygame.mixer.quit()
        except Exception:
            pass
        
        cleanup_audio()
        
        try:
            self.destroy()
        except Exception:
            pass
    
    def _on_close_request(self):
        """Handler do botão X."""
        if self.minimize_to_tray_var.get():
            dialog = CloseDialog(self)
            self.wait_window(dialog)
            
            if dialog.result == "minimize":
                self._minimize_to_tray()
            elif dialog.result == "exit":
                self._quit_app()
        else:
            self._quit_app()

# ══════════════════════════════════════════════════════════════════════════════
# DIÁLOGO DE FECHAMENTO
# ══════════════════════════════════════════════════════════════════════════════

class CloseDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.result = None
        
        self.title("Close Application")
        self.geometry("400x180")
        self.resizable(False, False)
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 180) // 2
        self.geometry(f"+{x}+{y}")
        
        self.transient(parent)
        self.grab_set()
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="🤔 What would you like to do?",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            main_frame,
            text="The app can continue running in the background",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack()
        
        ctk.CTkButton(
            btn_frame,
            text="📥 Minimize",
            width=110,
            height=38,
            corner_radius=10,
            command=self._minimize
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Exit",
            width=90,
            height=38,
            corner_radius=10,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self._exit
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=90,
            height=38,
            corner_radius=10,
            fg_color="transparent",
            border_width=2,
            command=self._cancel
        ).pack(side="left", padx=5)
        
        self.bind("<Escape>", lambda e: self._cancel())
    
    def _minimize(self):
        self.result = "minimize"
        self.destroy()
    
    def _exit(self):
        self.result = "exit"
        self.destroy()
    
    def _cancel(self):
        self.result = None
        self.destroy()

# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("   🔊 CLIPBOARD ENGLISH READER v1.1")
    print("=" * 60)
    print("   Copy text → Automatic TTS playback")
    print("   Press Ctrl+R anywhere to re-read last text")
    print("   Minimize to tray to keep running in background")
    print("=" * 60)
    
    app = App()
    app.mainloop()
