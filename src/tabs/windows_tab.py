"""
windows_tab.py
Aba 4: Otimizações do Windows
- Plano de Energia Desempenho Máximo (Ultimate Performance)
- Desativação de Xbox Game Bar e Game DVR
- Painel de Diagnóstico e Alertas (informativo)
"""

import os
import logging
import winreg
import customtkinter as ctk
from styles import (
    COLOR_BG, COLOR_PANEL, COLOR_SURFACE, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_WARNING,
    COLOR_ACCENT, FONT_FAMILY, FONT_FAMILY_BODY, FONT_FAMILY_DATA, FONT_FAMILY_TITLE,
    FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    CARD_CORNER_RADIUS, BUTTON_HEIGHT, BUTTON_CORNER_RADIUS,
    PADDING_MAIN, PADDING_CARD
)
from utils import is_admin, run_cmd, ERROS_SEM_SOLUCAO_MANUAL

logger = logging.getLogger("ValorantOptimizer")

INSTRUCOES_MANUAIS_WINDOWS = {
    "plano_energia": (
        "COMO ATIVAR O PLANO DE DESEMPENHO MÁXIMO MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite 'powercfg.cpl' e pressione Enter.\n"
        "2. Na janela Opções de Energia, clique em 'Mostrar planos adicionais'.\n"
        "3. Selecione o plano 'Desempenho Máximo' (Ultimate Performance).\n"
        "4. Se não estiver listado, execute como Administrador o comando:\n"
        "   powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61\n"
        "5. Depois vá em Opções de Energia e selecione 'Desempenho Máximo'.\n"
        "6. Reinicie o computador para aplicar.\n"
    ),
    "desativar_energia_rede": (
        "COMO DESATIVAR GERENCIAMENTO DE ENERGIA DA PLACA DE REDE MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite 'devmgmt.msc' e pressione Enter.\n"
        "2. Expanda 'Placas de rede'.\n"
        "3. Clique com o botão direito em sua placa Ethernet ou Wi-Fi ativa > Propriedades.\n"
        "4. Vá na aba 'Gerenciamento de energia'.\n"
        "5. DESMARQUE a opção 'Permitir que o computador desligue este dispositivo para economizar energia'.\n"
        "6. Clique em OK e reinicie o computador.\n"
    ),
    "sysmain": (
        "COMO DESATIVAR SYSMAIN (SUPERFETCH) MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite 'services.msc' e pressione Enter.\n"
        "2. Localize o serviço 'SysMain' (ou 'SuperFetch').\n"
        "3. Clique com o botão direito > Propriedades.\n"
        "4. Em 'Tipo de inicialização', selecione 'Desabilitado'.\n"
        "5. Clique em 'Parar' e depois em 'Aplicar' e 'OK'.\n"
        "6. Reinicie o computador.\n"
    ),
}

class WindowsTab(ctk.CTkFrame):
    """Aba de Otimizações do Windows."""

    def __init__(self, parent, status_callback, **kwargs):
        super().__init__(parent, fg_color=COLOR_BG, **kwargs)
        self.status_callback = status_callback
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Otimizações do Windows",
            font=(FONT_FAMILY_TITLE, FONT_SIZE_TITLE, "bold"),
            text_color=COLOR_ACCENT,
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=PADDING_MAIN)

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Plano de energia, desativação de recursos inúteis e diagnóstico do sistema",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
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

        # Card 1: Plano de Energia
        card1 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card1.pack(fill="x", pady=(0, 8), padx=5)
        card1.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card1, text="1. Plano de Energia de Desempenho Máximo",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card1,
            text="Habilita e aplica o plano oculto 'Desempenho Máximo' (Ultimate Performance) "
                 "via linha de comando, priorizando a CPU para jogos.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_energy = ctk.CTkButton(
            card1,
            text="Aplicar Desempenho Máximo",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_aplicar_energia,
        )
        btn_energy.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # Card 2: Desativar Recursos (Game Bar / Game DVR)
        card2 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card2.pack(fill="x", pady=(0, 8), padx=5)
        card2.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card2, text="2. Desativação de Recursos Inúteis",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card2,
            text="Desativa o Xbox Game Bar, Game DVR e gravações em segundo plano que "
                 "consumem recursos de hardware silenciosamente.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_recursos = ctk.CTkButton(
            card2,
            text="Desativar Game Bar e Game DVR",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_desativar_recursos,
        )
        btn_recursos.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # Card 3: Diagnóstico
        card3 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card3.pack(fill="x", pady=(0, PADDING_MAIN), padx=5)
        card3.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card3, text="3. Painel de Diagnóstico e Alertas",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card3,
            text="Orientações técnicas de desempenho do sistema.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_diag = ctk.CTkButton(
            card3,
            text="Exibir Diagnóstico",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_diagnostico,
        )
        btn_diag.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

    def _set_status(self, message: str, color: str = COLOR_TEXT_MUTED):
        if self.status_callback:
            self.status_callback(message, color)

    def _mostrar_instrucao_manual_windows(self, tipo_acao: str, erro_detalhe: str = ""):
        instrucao = INSTRUCOES_MANUAIS_WINDOWS.get(tipo_acao, ERROS_SEM_SOLUCAO_MANUAL)
        mensagem_completa = f"{instrucao}\n\nDetalhe do erro: {erro_detalhe}"
        self._set_status(mensagem_completa, COLOR_WARNING)

    def _verificar_admin(self) -> bool:
        if not is_admin():
            self._set_status(
                "Execute o aplicativo como Administrador para alterar plano de energia.",
                COLOR_WARNING
            )
            return False
        return True

    def _aplicar_ultimate_performance(self) -> tuple[bool, str]:
        """
        Duplica o plano Ultimate Performance (se não existir) e tenta ativá-lo.
        """
        guid_ultimate = "e9a42b02-d5df-448d-aa00-03f14749eb61"

        # Primeiro tenta duplicar o plano
        ok, saida = run_cmd(
            f'powercfg -duplicatescheme {guid_ultimate}',
            timeout=30,
        )
        if not ok:
            # Pode falhar se já existir; tentamos continuar para ativar
            logger.warning("Duplicação do plano pode já existir: %s", saida)

        # Tenta ativar diretamente pelo GUID
        ok, saida = run_cmd(
            f"powercfg -setactive {guid_ultimate}",
            timeout=30,
        )
        if ok:
            return True, "Plano de energia 'Desempenho Máximo' ativado."

        # Tenta listar planos e buscar pelo nome
        ok, saida = run_cmd("powercfg -list", timeout=30)
        if not ok:
            return False, "Não foi possível listar planos de energia."

        guid_encontrado = None
        for linha in saida.splitlines():
            linha = linha.strip()
            if "Desempenho Máximo" in linha or "Ultimate Performance" in linha:
                partes = linha.split("(")
                if len(partes) >= 2:
                    guid = partes[1].replace(")", "").strip()
                    guid_encontrado = guid
                    break

        if not guid_encontrado:
            return False, "Plano 'Desempenho Máximo' não encontrado após duplicação."

        ok, saida = run_cmd(f"powercfg -setactive {guid_encontrado}", timeout=30)
        if ok:
            return True, "Plano de energia 'Desempenho Máximo' ativado."
        return False, f"Falha ao ativar plano: {saida}"

    def _desativar_game_bar_dvr(self) -> tuple[bool, str]:
        """Desativa Xbox Game Bar e Game DVR via Registro (HKCU)."""
        alteracoes = [
            (
                r"System\GameConfigStore",
                "GameDVR_Enabled",
                0,
            ),
            (
                r"Software\Microsoft\GameBar",
                "AllowAutoGameMode",
                0,
            ),
            (
                r"Software\Microsoft\Windows\CurrentVersion\GameDVR",
                "AppCaptureEnabled",
                0,
            ),
        ]

        sucessos = 0
        erros = 0

        for subchave, nome, valor in alteracoes:
            try:
                chave = winreg.CreateKeyEx(
                    winreg.HKEY_CURRENT_USER, subchave, 0, winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(chave, nome, 0, winreg.REG_DWORD, valor)
                winreg.CloseKey(chave)
                sucessos += 1
            except Exception as exc:
                logger.error("Falha ao definir %s\\%s: %s", subchave, nome, exc)
                erros += 1

        if sucessos > 0:
            return True, f"Game Bar e Game DVR desativados ({sucessos} chave(s) atualizada(s))."
        return False, "Não foi possível desativar os recursos. Tente como Administrador."

    def _on_aplicar_energia(self):
        """Callback: aplicar otimização de energia."""
        if not self._verificar_admin():
            return
        self._set_status("Aplicando otimizações de energia...", COLOR_PRIMARY)
        try:
            ok, msg = self._aplicar_ultimate_performance()
            if ok:
                self._set_status(msg, COLOR_SUCCESS)
            else:
                self._set_status(msg, COLOR_DANGER)
        except Exception as exc:  # pylint: disable=broad-except
            self._set_status(f"Erro ao aplicar energia: {exc}", COLOR_DANGER)
            logger.error("Erro ao aplicar energia: %s", exc)

    def _on_desativar_recursos(self):
        """Callback: desativar recursos inúteis (Game Bar / Game DVR)."""
        if not self._verificar_admin():
            return
        self._set_status("Desativando recursos inúteis...", COLOR_PRIMARY)
        try:
            ok, msg = self._desativar_game_bar_dvr()
            if ok:
                self._set_status(msg, COLOR_SUCCESS)
            else:
                self._set_status(msg, COLOR_DANGER)
        except Exception as exc:  # pylint: disable=broad-except
            self._set_status(f"Erro ao desativar recursos: {exc}", COLOR_DANGER)
            logger.error("Erro ao desativar Game Bar/DVR: %s", exc)

    def _on_diagnostico(self):
        """Callback: exibir painel de diagnóstico informativo."""
        diagnostico = (
            "XMP/DOCP: Verifique na BIOS se o perfil XMP (Intel) ou DOCP (AMD) da memória RAM "
            "está ativado. Sem ele, a RAM opera em velocidade padrão, reduzindo o FPS mínimo.\n"
            "Limite de FPS ideal: defina no VALORANT um limite igual à taxa do monitor menos 3 quadros.\n"
            "Exemplos: 144 Hz → 141 FPS | 240 Hz → 237 FPS | 165 Hz → 162 FPS.\n"
            "Isso estabiliza o Frame Time com VRR / G-Sync / FreeSync ativo.\n"
            "Modo de Jogo: certifique-se de que o 'Modo de Jogo' do Windows está Ativado."
        )
        self._set_status(diagnostico, COLOR_TEXT_MUTED)

    def refresh_translations(self):
        """Reconstroi a UI da aba com os textos do idioma corrente."""
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()
