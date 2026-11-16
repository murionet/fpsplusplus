"""
game_booster_tab.py
Aba 2: Game Booster & RAM
- Modo Foco Automático (monitor de processo VALORANT)
- Limpeza de Standby List (RAM)
"""

import os
import logging
import threading
from typing import Optional
import customtkinter as ctk
import psutil
from utils import ERROS_SEM_SOLUCAO_MANUAL
from styles import (
    COLOR_BG, COLOR_PANEL, COLOR_SURFACE, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_WARNING,
    COLOR_ACCENT, COLOR_TOGGLE_ON, COLOR_TOGGLE_OFF,
    FONT_FAMILY, FONT_FAMILY_BODY, FONT_FAMILY_DATA, FONT_FAMILY_TITLE,
    FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    CARD_CORNER_RADIUS, BUTTON_HEIGHT, BUTTON_CORNER_RADIUS,
    PADDING_MAIN, PADDING_CARD
)

logger = logging.getLogger("ValorantOptimizer")

VALORANT_EXE = "VALORANT-Win64-Shipping.exe"
PRIORIDADE_ALTA = psutil.HIGH_PRIORITY_CLASS
PRIORIDADE_BAIXA = psutil.BELOW_NORMAL_PRIORITY_CLASS

# Lista de executáveis em segundo plano cuja prioridade será reduzida
# quando o Modo Foco detectar o VALORANT em execução.
PROCESSOS_SECUNDARIOS = [
    "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe",
    "discord.exe", "steam.exe", "epicgameslauncher.exe", "spotify.exe",
]

INSTRUCOES_MANUAIS_GAME_BOOSTER = {
    "monitor_auto": (
        "COMO DEFINIR PRIORIDADE ALTA MANUALMENTE:\n\n"
        "1. Pressione Ctrl + Shift + Esc para abrir o Gerenciador de Tarefas.\n"
        "2. Vá na aba 'Detalhes'.\n"
        "3. Localize o processo VALORANT-Win64-Shipping.exe.\n"
        "4. Clique com o botão direito > Definir prioridade > Alta.\n\n"
        "COMO REDUZIR PRIORIDADE DE NAVEGADORES:\n"
        "1. No mesmo Gerenciador de Tarefas, localize chrome.exe, msedge.exe, etc.\n"
        "2. Clique com o botão direito > Definir prioridade > Baixa.\n"
    ),
    "standby_list": (
        "COMO LIMPAR STANDBY LIST MANUALMENTE:\n\n"
        "1. Baixe o RamMap (Sysinternals) no site oficial da Microsoft.\n"
        "2. Execute como Administrador.\n"
        "3. Vá em Empty > Empty Standby List.\n"
        "4. Confirme a ação.\n"
    ),
}

class GameBoosterTab(ctk.CTkFrame):
    """Aba de Game Booster & RAM."""

    def __init__(self, parent, status_callback, **kwargs):
        super().__init__(parent, fg_color=COLOR_BG, **kwargs)
        self.status_callback = status_callback

        self.monitor_ativo = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_stop_event = threading.Event()

        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Game Booster & RAM",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            text_color=COLOR_TEXT,
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=PADDING_MAIN)

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Monitor automático de processo e liberação de memória RAM em standby",
            font=(FONT_FAMILY_BODY, FONT_SIZE_SUBTITLE),
            text_color=COLOR_TEXT_MUTED,
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, PADDING_MAIN), sticky="w", padx=PADDING_MAIN)

        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLOR_PRIMARY,
            scrollbar_button_hover_color=COLOR_PRIMARY_HOVER,
        )
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self.grid_rowconfigure(2, weight=1)

        # Card 1: Modo Foco
        card1 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card1.pack(fill="x", pady=(0, 8), padx=0)
        card1.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card1, text="1. MODO FOCO AUTOMÁTICO",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card1,
            text="Quando ativado, o app detecta o lançamento do VALORANT-Win64-Shipping.exe, "
                 "eleva a prioridade para Alta e reduz a prioridade de navegadores/launchers.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.btn_toggle = ctk.CTkButton(
            card1,
            text="ATIVAR MODO FOCO",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._toggle_monitor,
        )
        self.btn_toggle.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.lbl_monitor_status = ctk.CTkLabel(
            card1,
            text="Monitor: Desativado",
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_monitor_status.grid(row=3, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # Card 2: Limpeza de Standby List
        card2 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card2.pack(fill="x", pady=(0, PADDING_MAIN), padx=0)
        card2.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card2, text="2. LIMPEZA DE STANDBY LIST (RAM)",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card2,
            text="Tenta liberar a memória em espera (Standby Memory) do Windows, "
                 "que pode causar perda de desempenho após várias partidas seguidas.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.btn_clean_standby = ctk.CTkButton(
            card2,
            text="LIMPAR STANDBY LIST",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_clean_standby,
        )
        self.btn_clean_standby.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

    def _set_status(self, message: str, color: str = COLOR_TEXT_MUTED):
        if self.status_callback:
            self.status_callback(message, color)

    def _mostrar_instrucao_manual_booster(self, tipo_acao: str, erro_detalhe: str = ""):
        instrucao = INSTRUCOES_MANUAIS_GAME_BOOSTER.get(tipo_acao, ERROS_SEM_SOLUCAO_MANUAL)
        mensagem_completa = f"{instrucao}\n\nDetalhe do erro: {erro_detalhe}"
        self._set_status(mensagem_completa, COLOR_WARNING)

    def _toggle_monitor(self):
        if not self.monitor_ativo:
            self._iniciar_monitor()
        else:
            self._parar_monitor()

    def _iniciar_monitor(self):
        self.monitor_ativo = True
        self.monitor_stop_event.clear()
        self.btn_toggle.configure(text="Desativar Modo Foco", fg_color=COLOR_DANGER, hover_color="#b30000")
        self.lbl_monitor_status.configure(text="Monitor: Ativo", text_color=COLOR_SUCCESS)
        self._set_status("Modo Foco ativado. Aguardando VALORANT...", COLOR_PRIMARY)

        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def _parar_monitor(self):
        self.monitor_ativo = False
        self.monitor_stop_event.set()
        self.btn_toggle.configure(text="Ativar Modo Foco", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER)
        self.lbl_monitor_status.configure(text="Monitor: Desativado", text_color=COLOR_TEXT_MUTED)
        self._set_status("Modo Foco desativado.", COLOR_TEXT_MUTED)

    def _monitor_loop(self):
        valorant_ja_otimizado = False
        while not self.monitor_stop_event.is_set():
            try:
                proc_encontrado = None
                for proc in psutil.process_iter(["pid", "name"]):
                    try:
                        if proc.info["name"] and proc.info["name"].lower() == VALORANT_EXE.lower():
                            proc_encontrado = proc
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                if proc_encontrado and not valorant_ja_otimizado:
                    self._aplicar_foco(proc_encontrado)
                    valorant_ja_otimizado = True

                if not proc_encontrado:
                    valorant_ja_otimizado = False

            except Exception as exc:
                logger.error("Erro no loop do monitor: %s", exc)

            self.monitor_stop_event.wait(2.0)

    def _aplicar_foco(self, proc_valorant):
        try:
            proc_valorant.nice(PRIORIDADE_ALTA)
            pid = proc_valorant.pid
            self._set_status(f"VALORANT detectado (PID {pid}). Prioridade Alta aplicada.", COLOR_SUCCESS)
            logger.info("Prioridade Alta aplicada ao PID %d", pid)
        except Exception as exc:
            logger.error("Falha ao elevar prioridade do VALORANT: %s", exc)
            self._set_status("Falha ao elevar prioridade do VALORANT (execute como Admin).", COLOR_DANGER)

        reduzidos = 0
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                nome = proc.info["name"]
                if nome and nome.lower() in PROCESSOS_SECUNDARIOS:
                    proc.nice(PRIORIDADE_BAIXA)
                    reduzidos += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if reduzidos > 0:
            logger.info("Prioridade reduzida em %d processo(s) secundário(s).", reduzidos)

    def _on_clean_standby(self):
        self._set_status("Limpando Standby List...", COLOR_PRIMARY)
        try:
            ok, msg = self._limpar_standby_list()
            if ok:
                self._set_status(msg, COLOR_SUCCESS)
            else:
                self._mostrar_instrucao_manual_booster("standby_list", msg)
        except Exception as exc:
            self._mostrar_instrucao_manual_booster("standby_list", str(exc))
            logger.error("Erro na limpeza de standby: %s", exc)

    def _limpar_standby_list(self) -> Tuple[bool, str]:
        try:
            import subprocess
            resultado = subprocess.run(
                "EmptyStandbyList.exe",
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            if resultado.returncode == 0:
                return True, "Standby List liberada com sucesso (EmptyStandbyList)."
            return False, f"EmptyStandbyList falhou: {(resultado.stdout or resultado.stderr).strip()}"
        except Exception as exc:
            return False, f"Ferramenta EmptyStandbyList não encontrada: {exc}. "
            "Recomendamos baixar o RamMap (Sysinternals) e usar 'Empty Standby List' manualmente."