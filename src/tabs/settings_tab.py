"""
settings_tab.py
Aba de Configuracao
Permite ao usuario definir o caminho personalizado da pasta Config do VALORANT
via popup modal e visualizar informacoes sobre cada funcionalidade do aplicativo.
"""

import os
import customtkinter as ctk
from styles import (
    COLOR_BG, COLOR_PANEL, COLOR_SURFACE, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_WARNING,
    COLOR_ACCENT, FONT_FAMILY, FONT_FAMILY_BODY, FONT_FAMILY_DATA, FONT_FAMILY_TITLE,
    FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    CARD_CORNER_RADIUS, BUTTON_HEIGHT, BUTTON_CORNER_RADIUS, PADDING_MAIN, PADDING_CARD
)
from settings_manager import (
    get_valorant_config_path, set_valorant_config_path
)
from config_dialog import ValorantConfigDialog


class SettingsTab(ctk.CTkFrame):
    """Aba de Configuracao - caminho do VALORANT e descricoes."""

    def __init__(self, parent, status_callback, **kwargs):
        super().__init__(parent, fg_color=COLOR_BG, **kwargs)
        self.status_callback = status_callback
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Configuracao",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            text_color=COLOR_TEXT,
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=PADDING_MAIN)

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Defina o caminho da pasta do VALORANT e leia o que cada funcao faz.",
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE),
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

        # Card 1: Caminho do VALORANT
        card_path = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card_path.pack(fill="x", pady=(0, 8), padx=5)
        card_path.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card_path, text="1. CAMINHO DA PASTA DO VALORANT",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card_path,
            text="Informe a pasta raiz da instalacao do VALORANT (ex: D:\\Riot Games\\VALORANT). "
                 "O aplicativo procurara automaticamente a subpasta Saved\\Config dentro dela.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.lbl_caminho_atual = ctk.CTkLabel(
            card_path,
            text="",
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_caminho_atual.grid(row=2, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_frame = ctk.CTkFrame(card_path, fg_color="transparent")
        btn_frame.grid(row=3, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_alterar = ctk.CTkButton(
            btn_frame,
            text="ALTERAR CAMINHO (POPUP)",
            width=160,
            height=32,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 11, "bold"),
            command=self._on_alterar_caminho,
        )
        btn_alterar.pack(side="left", padx=(0, 8))

        btn_reset = ctk.CTkButton(
            btn_frame,
            text="USAR PADRAO",
            width=120,
            height=32,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_SURFACE,
            hover_color="#2a2a33",
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 11, "bold"),
            command=self._on_reset_path,
        )
        btn_reset.pack(side="left")

        self._atualizar_label_caminho()

        # Card 2: Descricoes das Funcoes
        card_desc = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card_desc.pack(fill="x", pady=(0, 8), padx=5)
        card_desc.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card_desc, text="2. O QUE CADA FUNCAO FAZ",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        descricoes = [
            (
                "Arquivos & Cache",
                "Limpeza de arquivos temporarios (%TEMP%), logs antigos do Valorant/Riot Client e "
                "cache de shaders da placa de video. Otimiza o GameUserSettings.ini (desativa "
                "VSync, pos-processo pesado, sombras) para maximizar FPS. Inclui backup automatico "
                "e reversao de alteracoes."
            ),
            (
                "Game Booster & RAM",
                "Monitora o processo VALORANT-Win64-Shipping.exe e, quando detectado, eleva a "
                "prioridade para Alta e reduz a prioridade de navegadores/launchers em segundo plano. "
                "Libera a memoria RAM em standby (Standby List)."
            ),
            (
                "Rede & Netcode",
                "Aplica TcpAckFrequency=1 e TCPNoDelay=1 no registro para reduzir latencia (ping). "
                "Desativa o gerenciamento de energia da placa de rede para evitar oscilacoes de pacotes. "
                "Inclui limpeza de cache DNS e ARP."
            ),
            (
                "Otimizacoes do Windows",
                "Ativa o plano de energia Desempenho Maximo (Ultimate Performance). Desativa "
                "Xbox Game Bar, Game DVR e gravacoes em segundo plano. Exibe diagnostico (XMP/DOCP, "
                "limite de FPS ideal) e gerenciamento do SysMain/SuperFetch."
            ),
        ]

        row = 1
        for titulo, descricao in descricoes:
            ctk.CTkLabel(
                card_desc, text=titulo,
                font=(FONT_FAMILY_BODY, 12, "bold"), text_color=COLOR_SUCCESS,
            ).grid(row=row, column=0, sticky="w", padx=PADDING_CARD, pady=(6, 2))

            ctk.CTkLabel(
                card_desc, text=descricao,
                font=(FONT_FAMILY_BODY, FONT_SIZE_SMALL),
                text_color=COLOR_TEXT_MUTED,
                wraplength=700, justify="left",
            ).grid(row=row + 1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, 6))

            row += 2

        card_seg = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card_seg.pack(fill="x", pady=(0, PADDING_MAIN), padx=5)
        card_seg.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card_seg, text="3. SEGURANCA (RIOT VANGUARD)",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card_seg,
            text="SEGURANCA (RIOT VANGUARD)\n\n"
                 "Este aplicativo NAO modifica memoria, NAO injeta DLLs e NAO altera arquivos .pak do VALORANT.\n"
                 "Todas as acoes sao:\n"
                 "• Edicao local do GameUserSettings.ini (com backup automatico)\n"
                 "• Comandos administrativos seguros do Windows (registro, powercfg, etc.)\n"
                 "• Limpeza de pastas de cache e temp do proprio usuario",
            font=(FONT_FAMILY_BODY, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
            justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

    def _atualizar_label_caminho(self):
        caminho = get_valorant_config_path()
        if caminho:
            self.lbl_caminho_atual.configure(
                text="Caminho atual: " + caminho,
                text_color=COLOR_SUCCESS,
            )
        else:
            self.lbl_caminho_atual.configure(
                text="Usando caminho padrao do Windows (%LOCALAPPDATA%)",
                text_color=COLOR_TEXT_MUTED,
            )

    def _set_status(self, message: str, color: str = COLOR_TEXT_MUTED):
        if self.status_callback:
            self.status_callback(message, color)

    def _on_alterar_caminho(self):
        def ao_salvar(config_root):
            if config_root:
                self._atualizar_label_caminho()
                self._set_status("Caminho configurado: " + str(config_root), COLOR_SUCCESS)
            else:
                self._set_status("Operacao cancelada.", COLOR_TEXT_MUTED)

        dialog = ValorantConfigDialog(self, callback=ao_salvar)
        self.wait_window(dialog)

    def _on_reset_path(self):
        if set_valorant_config_path(""):
            self._atualizar_label_caminho()
            self._set_status("Caminho redefinido para padrao.", COLOR_SUCCESS)

    def refresh_translations(self):
        """Reconstroi a UI da aba com os textos do idioma corrente."""
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()