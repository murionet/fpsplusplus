"""
main.py
Valorant System Optimizer - Unificado
Interface Dark Mode minimalista, abas superiores.
Sem injetores, sem modificacao de memoria, sem alteracao de arquivos .pak.
Respeita estritamente as regras do Riot Vanguard.
"""

import os
import sys
import customtkinter as ctk

# -------------------------------------------------------------------------
# Garante que os modulos locais (styles, utils, tabs, etc.) sejam encontrados
# tanto em desenvolvimento (codigo-fonte) quanto empacotado (PyInstaller .exe).
# -------------------------------------------------------------------------
if getattr(sys, "frozen", False):
    # Executavel compilado: o PyInstaller extrai os modulos para um diretorio
    # temporario (_MEIPASS) e o diretorio do .exe fica disponível em sys.executable.
    base_dir = os.path.dirname(sys.executable)
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        if meipass not in sys.path:
            sys.path.insert(0, meipass)
        # Adiciona explicitamente o diretorio src/ empacotado dentro do _MEIPASS
        src_inside_meipass = os.path.join(meipass, "src")
        if os.path.isdir(src_inside_meipass) and src_inside_meipass not in sys.path:
            sys.path.insert(0, src_inside_meipass)
        tabs_inside_meipass = os.path.join(meipass, "src", "tabs")
        if os.path.isdir(tabs_inside_meipass) and tabs_inside_meipass not in sys.path:
            sys.path.insert(0, tabs_inside_meipass)
else:
    # Modo desenvolvimento: o diretorio onde este arquivo main.py esta localizado
    # (normalmente src/) e a subpasta tabs/ sao adicionados ao caminho.
    # Isso funciona independente de de onde o usuario execute o comando python.
    arquivo_dir = os.path.dirname(os.path.abspath(__file__))
    if arquivo_dir not in sys.path:
        sys.path.insert(0, arquivo_dir)

    tabs_dir = os.path.join(arquivo_dir, "tabs")
    if tabs_dir not in sys.path:
        sys.path.insert(0, tabs_dir)

    # Fallback: se o usuario copiou so o main.py para fora da pasta src/,
    # procura por styles.py no diretorio atual e em subpastas comuns.
    try:
        from styles import COLOR_BG  # noqa: F401
    except ImportError:
        candidatos = [
            os.path.join(os.getcwd(), "src"),
            os.path.join(os.getcwd()),
            os.path.join(os.path.dirname(arquivo_dir), "src"),
        ]
        for cand in candidatos:
            if cand not in sys.path and os.path.isfile(os.path.join(cand, "styles.py")):
                sys.path.insert(0, cand)
                break

try:
    from styles import (
        COLOR_BG, COLOR_PANEL, COLOR_SURFACE, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
        COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_WARNING,
        COLOR_ACCENT, FONT_FAMILY, FONT_FAMILY_BODY, FONT_FAMILY_DATA,
        FONT_SIZE_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
        BUTTON_HEIGHT, BUTTON_CORNER_RADIUS, PADDING_MAIN,
        FONT_SIZE_SUBTITLE, FONT_SIZE_SMALL, FONT_SIZE_DATA
    )
    from file_cache_tab import FileCacheTab
    from game_booster_tab import GameBoosterTab
    from network_tab import NetworkTab
    from windows_tab import WindowsTab
    from settings_tab import SettingsTab
    from settings_manager import (
        get_valorant_config_path, set_valorant_config_path
    )
    from config_dialog import ValorantConfigDialog
    from utils import detect_valorant_installation
    from lang import get_language, set_language, t
except ImportError as exc:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Erro ao iniciar o aplicativo",
        "Nao foi possivel carregar os modulos locais do aplicativo.\n\n"
        "Isso acontece quando o codigo-fonte (.py) e executado diretamente "
        "em vez do executavel compilado (.exe).\n\n"
        "Solucao: nao abra o arquivo main.py. Abra o arquivo:\n"
        "ValorantSystemOptimizer_v1.0.0.exe\n\n"
        "Detalhe tecnico: " + str(exc)
    )
    sys.exit(1)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ValorantOptimizerApp(ctk.CTk):
    """Janela principal do aplicativo unificado."""

    def __init__(self):
        super().__init__()

        self.title(t("app_title"))
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)

        self.header = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=0)
        self.header.pack(fill="x", padx=0, pady=0)
        self.header.grid_columnconfigure(1, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self.header,
            text=t("app_title"),
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            text_color=COLOR_TEXT,
        )
        self.lbl_title.grid(row=0, column=0, padx=PADDING_MAIN, pady=(12, 2), sticky="w")

        self.lbl_subtitle = ctk.CTkLabel(
            self.header,
            text=t("app_subtitle"),
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_subtitle.grid(row=1, column=0, padx=PADDING_MAIN, pady=(0, 12), sticky="w")

        self.btn_lang = ctk.CTkButton(
            self.header,
            text="EN" if get_language() == "pt" else "PT",
            width=40,
            height=28,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_SURFACE,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 11, "bold"),
            command=self._toggle_language,
        )
        self.btn_lang.grid(row=0, column=2, rowspan=2, padx=PADDING_MAIN, pady=12, sticky="e")

        # Guarda a fábrica de tabs para poder recriá-las ao trocar de idioma.
        # Cada entrada: (translation_key, ClasseDaTab, instancia_da_tab)
        self._tab_specs = [
            ("tab_files", FileCacheTab),
            ("tab_booster", GameBoosterTab),
            ("tab_network", NetworkTab),
            ("tab_windows", WindowsTab),
            ("tab_settings", SettingsTab),
        ]
        self._tab_instances: dict = {}  # translation_key -> instancia da tab

        self._build_tabs()

    def _build_tabs(self):
        """Cria (ou recria) o tabview e todas as abas com os títulos no idioma atual."""
        # Se já existe um tabview, destrói antes de recriar.
        if hasattr(self, "tabview") and self.tabview is not None:
            self.tabview.destroy()

        self.tabview = ctk.CTkTabview(
            self,
            fg_color=COLOR_BG,
            segmented_button_fg_color=COLOR_SURFACE,
            segmented_button_selected_color=COLOR_PRIMARY,
            segmented_button_selected_hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
        )
        self.tabview.pack(fill="both", expand=True, padx=PADDING_MAIN, pady=(0, PADDING_MAIN))

        self._tab_instances.clear()
        for key, cls in self._tab_specs:
            tab_frame = self.tabview.add(t(key))
            tab_frame.grid_columnconfigure(0, weight=1)
            tab_frame.grid_rowconfigure(0, weight=1)
            instance = cls(tab_frame, self._set_status)
            instance.grid(row=0, column=0, sticky="nsew")
            self._tab_instances[key] = instance

        self.status_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.status_frame.pack(fill="x", padx=PADDING_MAIN, pady=(0, 10))
        self.status_frame.grid_columnconfigure(0, weight=1)

        self.status_var = ctk.StringVar(value=t("status_ready"))
        self.status_bar = ctk.CTkLabel(
            self.status_frame,
            textvariable=self.status_var,
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.status_bar.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.btn_config_path = ctk.CTkButton(
            self.status_frame,
            text=t("btn_config_path"),
            width=180,
            height=28,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 11, "bold"),
            command=self._abrir_dialog_caminho,
        )
        self.btn_config_path.grid(row=0, column=1, sticky="e")

        caminho_salvo = get_valorant_config_path()
        if caminho_salvo:
            self._set_status("Caminho configurado: " + str(caminho_salvo), COLOR_SUCCESS)
        else:
            caminho_auto = detect_valorant_installation()
            if caminho_auto:
                set_valorant_config_path(caminho_auto)
                self._set_status(
                    "VALORANT detectado automaticamente: " + str(caminho_auto),
                    COLOR_SUCCESS
                )
            else:
                self._set_status(
                    "Nenhum caminho do VALORANT configurado. Clique em Configurar Caminho Valorant.",
                    COLOR_WARNING
                )

    def _set_status(self, message: str, color: str = COLOR_TEXT_MUTED):
        self.status_var.set(message)
        self.status_bar.configure(text_color=color)

    def _toggle_language(self):
        current = get_language()
        new_lang = "pt" if current == "en" else "en"
        set_language(new_lang)
        self.btn_lang.configure(text="EN" if new_lang == "pt" else "PT")
        self._rebuild_ui()

    def _rebuild_ui(self):
        self.title(t("app_title"))
        self.lbl_title.configure(text=t("app_title"))
        self.lbl_subtitle.configure(text=t("app_subtitle"))
        self.btn_lang.configure(text="EN" if get_language() == "pt" else "PT")
        self.btn_config_path.configure(text=t("btn_config_path"))

        # Recria as abas com os novos títulos do idioma selecionado.
        self._build_tabs()

        # Notifica cada tab para atualizar seus textos internos.
        for instance in self._tab_instances.values():
            if hasattr(instance, "refresh_translations"):
                instance.refresh_translations()

        self._set_status(self.status_var.get(), COLOR_TEXT_MUTED)

    def _abrir_dialog_caminho(self):
        def ao_salvar(config_root):
            if config_root:
                self._set_status("Caminho configurado: " + str(config_root), COLOR_SUCCESS)
            else:
                self._set_status("Operacao cancelada.", COLOR_TEXT_MUTED)

        dialog = ValorantConfigDialog(self, callback=ao_salvar)
        self.wait_window(dialog)


def main():
    app = ValorantOptimizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()