"""
network_tab.py
Aba 3: Rede & Netcode
- Otimização TCP/IP (TcpAckFrequency, TCPNoDelay) via Registro/PowerShell
- Desativar gerenciamento de energia da placa de rede
- Limpeza de cache DNS/ARP
"""

import os
import logging
import winreg
import customtkinter as ctk
from styles import (
    COLOR_BG, COLOR_PANEL, COLOR_SURFACE, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_WARNING,
    COLOR_ACCENT, COLOR_TOGGLE_ON, COLOR_TOGGLE_OFF,
    FONT_FAMILY, FONT_FAMILY_BODY, FONT_FAMILY_DATA, FONT_FAMILY_TITLE,
    FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL,
    CARD_CORNER_RADIUS, BUTTON_HEIGHT, BUTTON_CORNER_RADIUS,
    PADDING_MAIN, PADDING_CARD
)
from utils import is_admin, run_cmd, set_valorant_priority_high, ERROS_SEM_SOLUCAO_MANUAL

logger = logging.getLogger("ValorantOptimizer")

REG_INTERFACES_PATH = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"

INSTRUCOES_MANUAIS_NETWORK = {
    "tcp_ip": (
        "COMO OTIMIZAR TCP/IP MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite 'regedit' e pressione Enter.\n"
        "2. Navegue até: HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\n"
        "3. Expanda a pasta 'Interfaces' e clique em cada subpasta (GUIDs).\n"
        "4. Para cada subpasta, clique com o botão direito em um espaço vazio > Novo > Valor DWORD (32 bits).\n"
        "5. Crie o valor 'TcpAckFrequency' e defina como 1.\n"
        "6. Crie o valor 'TCPNoDelay' e defina como 1.\n"
        "7. Reinicie o computador para aplicar.\n"
    ),
    "energia_rede": (
        "COMO DESATIVAR GERENCIAMENTO DE ENERGIA DA PLACA DE REDE MANUALMENTE:\n\n"
        "1. Pressione Win + X e clique em 'Gerenciador de Dispositivos'.\n"
        "2. Expanda 'Placas de rede'.\n"
        "3. Clique com o botão direito em sua placa Ethernet ou Wi-Fi ativa > Propriedades.\n"
        "4. Vá na aba 'Gerenciamento de energia'.\n"
        "5. DESMARQUE a opção 'Permitir que o computador desligue este dispositivo para economizar energia'.\n"
        "6. Clique em OK e reinicie o computador.\n"
    ),
    "dns_arp": (
        "COMO LIMPAR CACHE DNS E ARP MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite 'cmd' e pressione Ctrl + Shift + Enter (executar como Administrador).\n"
        "2. No Prompt de Comando, digite o seguinte comando e pressione Enter:\n"
        "   ipconfig /flushdns\n"
        "3. Aguarde a mensagem 'Cache de resolução de DNS foi limpo com sucesso'.\n"
        "4. Em seguida, digite o comando abaixo e pressione Enter:\n"
        "   arp -d *\n"
        "5. Reinicie o computador para aplicar todas as alterações.\n"
    ),
}

class NetworkTab(ctk.CTkFrame):
    """Aba de Rede & Netcode."""

    def __init__(self, parent, status_callback, **kwargs):
        super().__init__(parent, fg_color=COLOR_BG, **kwargs)
        self.status_callback = status_callback
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Rede & Netcode",
            font=(FONT_FAMILY_TITLE, FONT_SIZE_TITLE, "bold"),
            text_color=COLOR_TEXT,
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=PADDING_MAIN)

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Otimização de parâmetros TCP/IP e gerenciamento de energia da placa de rede",
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

        # Card 1: Otimização TCP/IP
        card1 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card1.pack(fill="x", pady=(0, 8), padx=5)
        card1.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card1, text="1. OTIMIZAÇÃO DE TCP/IP PARA JOGOS",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card1,
            text="Aplica TcpAckFrequency=1 e TCPNoDelay=1 em todas as interfaces de rede "
                 "para reduzir a latência (ping) e melhorar o registro de tiros. "
                 "Requer privilégios de Administrador.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_tcp = ctk.CTkButton(
            card1,
            text="Aplicar Otimização TCP/IP",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_optimize_tcp,
        )
        btn_tcp.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # Card 2: Prioridade do Processo
        card2 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card2.pack(fill="x", pady=(0, 8), padx=5)
        card2.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card2, text="2. Gerenciamento de Energia da Placa de Rede",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card2,
            text="Desativa o gerenciamento de energia da placa Ethernet/Wi-Fi para evitar "
                 "oscilações de pacotes e latência instável.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_net_power = ctk.CTkButton(
            card2,
            text="Desativar Gerenciamento de Energia da Rede",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_disable_net_power,
        )
        btn_net_power.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        card3 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card3.pack(fill="x", pady=(0, PADDING_MAIN), padx=5)
        card3.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card3, text="3. Limpeza de Cache de Rede (DNS/ARP)",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 6))

        ctk.CTkLabel(
            card3,
            text="Executa ipconfig /flushdns e arp -d para limpar cache de sockets locais "
                 "e mitigar perdas de pacotes por corrupção na tabela de roteamento.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_cache = ctk.CTkButton(
            card3,
            text="Limpar Cache e Logs",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_cleanup_cache,
        )
        btn_cache.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

    def _set_status(self, message: str, color: str = COLOR_TEXT_MUTED):
        if self.status_callback:
            self.status_callback(message, color)

    def _mostrar_instrucao_manual_network(self, tipo_acao: str, erro: str = ""):
        instrucao = INSTRUCOES_MANUAIS_NETWORK.get(tipo_acao, ERROS_SEM_SOLUCAO_MANUAL)
        mensagem_completa = f"{instrucao}\n\nDetalhe do erro: {erro_detalhe}"
        self._set_status(mensagem_completa, COLOR_WARNING)

    def _verificar_admin(self) -> bool:
        if not is_admin():
            self._set_status(
                "Execute o aplicativo como Administrador para alterar rede/registro.",
                COLOR_WARNING
            )
            return False
        return True

    def _aplicar_tcp_ip(self) -> tuple[bool, str]:
        """
        Aplica TcpAckFrequency=1 e TCPNoDelay=1 em todas as interfaces de rede.
        """
        try:
            raiz = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_INTERFACES_PATH, 0, winreg.KEY_READ | winreg.KEY_WRITE)
        except Exception as exc:
            return False, f"Não foi possível acessar o registro de rede: {exc}"

        alteradas = 0
        erros = 0
        try:
            i = 0
            while True:
                try:
                    guid = winreg.EnumKey(raiz, i)
                    i += 1
                except OSError:
                    break

                caminho_interface = f"{REG_INTERFACES_PATH}\\{guid}"
                try:
                    chave = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, caminho_interface, 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(chave, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(chave, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
                    winreg.CloseKey(chave)
                    alteradas += 1
                except Exception:
                    erros += 1
        finally:
            winreg.CloseKey(raiz)

        if alteradas > 0:
            return True, f"TCP/IP otimizado em {alteradas} interface(s) de rede."
        if erros > 0:
            return False, f"Falha ao otimizar {erros} interface(s)."
        return False, "Nenhuma interface de rede encontrada."

    def _desativar_energia_rede(self) -> tuple[bool, str]:
        """
        Desativa o gerenciamento de energia da placa de rede (Ethernet/Wi-Fi)
        via PowerShell para evitar oscilações de pacotes e latência instável.
        """
        comando = (
            "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | "
            "Disable-NetAdapterPowerManagement -Confirm:$false -ErrorAction SilentlyContinue"
        )
        ok, msg = run_cmd(f'powershell -Command "{comando}"', timeout=30)
        if ok:
            return True, "Gerenciamento de energia da placa de rede desativado com sucesso."
        return False, f"Falha ao desativar gerenciamento de energia da rede: {msg}"

    def _on_disable_net_power(self):
        if not self._verificar_admin():
            return
        self._set_status("Desativando gerenciamento de energia da rede...", COLOR_PRIMARY)
        try:
            ok, msg = self._desativar_energia_rede()
            if ok:
                self._set_status(msg, COLOR_SUCCESS)
            else:
                self._set_status(msg, COLOR_DANGER)
        except Exception as exc:
            self._mostrar_instrucao_manual_network("desativar_energia_rede", str(exc))
            logger.error("Erro ao desativar energia da rede: %s", exc)

    def _on_cleanup_cache(self):
        if not self._verificar_admin():
            return
        self._set_status("Limpando cache de rede...", COLOR_PRIMARY)
        try:
            ok, msg = self._flush_network_cache()
            if ok:
                self._set_status(msg, COLOR_SUCCESS)
            else:
                self._set_status(msg, COLOR_DANGER)
        except Exception as exc:
            self._mostrar_instrucao_manual_network("limpeza_cache", str(exc))
            logger.error("Erro na limpeza de cache de rede: %s", exc)

    def _flush_network_cache(self) -> tuple[bool, str]:
        comandos = [
            "ipconfig /flushdns",
            "arp -d *",
        ]
        sucessos = 0
        erros = 0
        mensagens = []
        for cmd in comandos:
            ok, msg = run_cmd(f"ipconfig {cmd}", timeout=30)
            if ok:
                sucessos += 1
                mensagens.append(f"{cmd}: OK")
            else:
                erros += 1
                mensagens.append(f"{cmd}: Falha - {msg}")

        if erros == 0:
            return True, f"Cache DNS e ARP limpos com sucesso: {sucessos} arquivo(s) removido(s)."
        if sucessos > 0:
            return True, f"Parcial: {sucessos} arquivo(s) removido(s), {erros} erro(s)."
        return False, "Falha ao limpar cache de rede."

    def _on_set_priority(self):
        """Define prioridade Alta para o processo VALORANT."""
        if not self._verificar_admin():
            return
        self._set_status("Definindo prioridade Alta...", COLOR_PRIMARY)
        try:
            ok, msg = set_valorant_priority_high()
            if ok:
                self._set_status(msg, COLOR_SUCCESS)
            else:
                self._set_status(msg, COLOR_DANGER)
        except Exception as exc:  # pylint: disable=broad-except
            self._mostrar_instrucao_manual_network("definir_prioridade", str(exc))
            logger.error("Erro ao definir prioridade: %s", exc)

    def _on_optimize_tcp(self):
        """Callback: aplicar otimização TCP/IP."""
        if not self._verificar_admin():
            return
        self._set_status("Aplicando otimização TCP/IP...", COLOR_PRIMARY)
        try:
            ok, msg = self._aplicar_tcp_ip()
            if ok:
                self._set_status(msg, COLOR_SUCCESS)
            else:
                self._set_status(msg, COLOR_DANGER)
        except Exception as exc:  # pylint: disable=broad-except
            self._mostrar_instrucao_manual_network("tcp_ip", str(exc))
            logger.error("Erro na otimização TCP: %s", exc)

