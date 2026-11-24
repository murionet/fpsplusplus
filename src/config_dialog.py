"""
config_dialog.py
Popup modal para configurar o caminho da pasta do VALORANT.
Bloqueia a janela principal ate que o usuario informe o caminho valido.
"""

import os
import customtkinter as ctk

from styles import (
    COLOR_BG, COLOR_PANEL, COLOR_SURFACE, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_ACCENT,
    FONT_FAMILY, FONT_SIZE_BODY, FONT_SIZE_SMALL, BUTTON_HEIGHT, BUTTON_CORNER_RADIUS
)
from settings_manager import set_valorant_config_path, get_valorant_config_path
from utils import select_valorant_folder_gui


class ValorantConfigDialog(ctk.CTkToplevel):
    """Dialog modal para configurar o caminho da pasta do VALORANT.
    Bloqueia a interacao com a janela principal ate ser fechado.
    """

    def __init__(self, parent, callback=None):
        super().__init__(parent)

        self.callback = callback
        self.result_path = None
        self.modal_result = False

        self.title("Configurar Valorant - Caminho Obrigatorio")
        self.geometry("600x400")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()
        self.focus_force()

        self._center_on_parent(parent)
        self._build_ui()

    def _center_on_parent(self, parent):
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        dialog_w = 600
        dialog_h = 400

        x = parent_x + (parent_w - dialog_w) // 2
        y = parent_y + (parent_h - dialog_h) // 2

        self.geometry(f"{dialog_w}x{dialog_h}+{x}+{y}")

    def _build_ui(self):
        self.container = ctk.CTkFrame(self, fg_color=COLOR_PANEL, corner_radius=12)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self.container,
            text="Configuracao Obrigatoria do VALORANT",
            font=(FONT_FAMILY, 18, "bold"),
            text_color=COLOR_TEXT,
        )
        self.lbl_title.grid(row=0, column=0, pady=(20, 10), padx=30, sticky="w")

        self.lbl_subtitle = ctk.CTkLabel(
            self.container,
            text=r"Informe a pasta raiz da instalacao do VALORANT."
                 r"\nExemplo: D:\Riot Games\VALORANT\n\n"
                 r"O aplicativo procurara automaticamente a pasta Saved\Config dentro dela.",
            font=(FONT_FAMILY, 12),
            text_color=COLOR_TEXT_MUTED,
            justify="left",
        )
        self.lbl_subtitle.grid(row=1, column=0, pady=(0, 15), padx=30, sticky="w")

        self.entry_path = ctk.CTkEntry(
            self.container,
            placeholder_text="Cole aqui o caminho da pasta do VALORANT",
            width=380,
            height=40,
            corner_radius=BUTTON_CORNER_RADIUS,
            font=(FONT_FAMILY, 12),
        )
        self.entry_path.grid(row=2, column=0, pady=(0, 10), padx=(30, 5), sticky="ew")

        self.btn_procurar = ctk.CTkButton(
            self.container,
            text="Procurar…",
            width=80,
            height=40,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_SURFACE,
            hover_color="#2a2a33",
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY, 12, "bold"),
            command=self._on_procurar,
        )
        self.btn_procurar.grid(row=2, column=0, pady=(0, 10), padx=(5, 30), sticky="e")
        self.container.grid_columnconfigure(0, weight=1)

        self.lbl_feedback = ctk.CTkLabel(
            self.container,
            text="",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_feedback.grid(row=3, column=0, pady=(0, 15), padx=30, sticky="w")

        saved = get_valorant_config_path()
        if saved:
            self.entry_path.insert(0, saved)
            self.lbl_feedback.configure(
                text=f"Caminho salvo anteriormente: {saved}", text_color=COLOR_SUCCESS
            )

        self.btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.btn_frame.grid(row=4, column=0, pady=(0, 20), padx=30, sticky="e")

        self.btn_cancelar = ctk.CTkButton(
            self.btn_frame,
            text="Sair do Aplicativo",
            width=140,
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_DANGER,
            hover_color="#dc2626",
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY, 12, "bold"),
            command=self._on_cancel,
        )
        self.btn_cancelar.pack(side="left", padx=(0, 10))

        self.btn_salvar = ctk.CTkButton(
            self.btn_frame,
            text="Salvar e Continuar",
            width=160,
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY, 12, "bold"),
            command=self._on_save,
        )
        self.btn_salvar.pack(side="left")

        self.entry_path.bind("<Return>", lambda e: self._on_save())

    def _on_procurar(self):
        """Abre o seletor de pastas nativo do Windows e preenche o campo."""
        pasta = select_valorant_folder_gui(parent=self)
        if pasta:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, pasta)
            self.lbl_feedback.configure(
                text=f"Pasta selecionada: {pasta}", text_color=COLOR_SUCCESS
            )

    def _validar_caminho(self, caminho: str) -> bool:
        if not caminho or not caminho.strip():
            return False

        caminho = caminho.strip()

        if os.path.isdir(caminho):
            return True

        config_path = os.path.join(caminho, "Saved", "Config")
        if os.path.isdir(config_path):
            return True

        variacoes = [
            os.path.join(caminho, "VALORANT", "Saved", "Config"),
            os.path.join(caminho, "Saved", "Config"),
        ]
        for v in variacoes:
            if os.path.isdir(v):
                return True

        return False

    def _obter_config_root(self, caminho: str) -> str | None:
        """
        Resolve a pasta Saved\\Config a partir do caminho informado pelo usuário.
        O usuário pode informar a raiz da instalação (ex: D:\\Riot Games\\VALORANT)
        ou já a pasta Saved\\Config diretamente.
        """
        if not caminho or not caminho.strip():
            return None

        caminho = caminho.strip()

        if not os.path.isdir(caminho):
            return None

        # Se o usuário já apontou diretamente para a pasta Saved\Config
        if os.path.isfile(os.path.join(caminho, "GameUserSettings.ini")) or \
           any(d.startswith("{") for d in os.listdir(caminho) if os.path.isdir(os.path.join(caminho, d))):
            return caminho

        # Caso contrário, procurar Saved\Config dentro do caminho informado
        possiveis = [
            os.path.join(caminho, "Saved", "Config"),
            os.path.join(caminho, "VALORANT", "Saved", "Config"),
        ]

        for p in possiveis:
            if os.path.isdir(p):
                return p

        # Fallback: retorna o próprio caminho (o app irá re-resolver depois)
        return caminho

    def _on_save(self):
        caminho = self.entry_path.get().strip()

        if not caminho:
            self.lbl_feedback.configure(
                text="Erro: Informe o caminho da pasta do VALORANT.", text_color=COLOR_DANGER
            )
            return

        if not self._validar_caminho(caminho):
            self.lbl_feedback.configure(
                text="Erro: Pasta não encontrada. Verifique o caminho informado.",
                text_color=COLOR_DANGER,
            )
            return

        config_root = self._obter_config_root(caminho)
        if not config_root:
            self.lbl_feedback.configure(
                text="Erro: Não foi possível localizar a pasta Saved\\Config.",
                text_color=COLOR_DANGER,
            )
            return

        set_valorant_config_path(caminho)

        self.result_path = config_root
        self.modal_result = True

        if self.callback:
            self.callback(config_root)

        self.destroy()

    def _on_cancel(self):
        self.modal_result = False
        self.destroy()
        if self.callback:
            self.callback(None)


def solicitar_caminho_valorant(parent, callback=None) -> str | None:
    dialog = ValorantConfigDialog(parent, callback=callback)
    parent.wait_window(dialog)
    return dialog.result_path