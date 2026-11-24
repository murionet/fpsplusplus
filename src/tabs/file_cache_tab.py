"""
file_cache_tab.py
Aba 1: Arquivos & Cache - Limpeza profunda, otimização INI, limpeza expandida
"""

import os
import logging
import configparser
import customtkinter as ctk
from styles import (
    COLOR_BG, COLOR_PANEL, COLOR_SURFACE, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_WARNING,
    COLOR_ACCENT, FONT_FAMILY, FONT_FAMILY_TITLE, FONT_FAMILY_BODY, FONT_FAMILY_DATA, FONT_SIZE_TITLE,
    FONT_SIZE_SUBTITLE, FONT_SIZE_BODY, FONT_SIZE_SMALL, CARD_CORNER_RADIUS,
    BUTTON_HEIGHT, BUTTON_CORNER_RADIUS,
    BUTTON_CORNER_RADIUS, PADDING_MAIN, PADDING_CARD
)
from utils import (
    find_valorant_config_dir, list_profile_dirs, find_game_user_settings,
    safe_remove_dir_contents, run_cmd, is_admin,
    detect_valorant_installation, get_folder_size_mb,
    remove_folder_contents_and_report, stop_service, start_service,
    empty_recycle_bin,
    ERROS_SEM_SOLUCAO_MANUAL,
)
from settings_manager import (
    get_valorant_config_path, list_available_backups, restore_backup,
    backup_file,
)

logger = logging.getLogger("ValorantOptimizer")

# Mensagens educativas para cada função
INSTRUCOES_MANUAIS_CACHE = {
    "cache_expandido": (
        "COMO LIMPAR DIRETÓRIOS TEMPORÁRIOS MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite '%TEMP%' e pressione Enter.\n"
        "2. Selecione todos os arquivos (Ctrl + A) e exclua (Shift + Delete).\n"
        "3. Pressione Win + R, digite '%WINDIR%\\Logs' e pressione Enter.\n"
        "4. Exclua todos os arquivos da pasta.\n"
        "5. Para o cache do Edge: Pressione Win + R, digite:\n"
        "   %LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Cache\n"
        "6. Exclua todo o conteúdo da pasta.\n"
        "\nNota: Alguns arquivos podem estar em uso e não poderão ser excluídos. Isso é normal."
    ),
    "windows_update": (
        "COMO LIMPAR CACHE DO WINDOWS UPDATE MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite 'services.msc' e pressione Enter.\n"
        "2. Localize o serviço 'Windows Update' (wuauserv).\n"
        "3. Clique com o botão direito > Parar.\n"
        "4. Pressione Win + R, digite: C:\\Windows\\SoftwareDistribution\\Download\n"
        "5. Exclua todo o conteúdo da pasta.\n"
        "6. Volte ao services.msc, clique com o botão direito no 'Windows Update' > Iniciar.\n"
    ),
    "lixeira": (
        "COMO ESVAZIAR A LIXEIRA MANUALMENTE:\n\n"
        "1. Clique com o botão direito no ícone da Lixeira na área de trabalho.\n"
        "2. Selecione 'Esvaziar Lixeira'.\n"
        "3. Confirme a ação.\n\n"
        "Ou: Abra o Explorador de Arquivos > Lixeira > Esvaziar Lixeira na faixa de opções."
    ),
    "ini_otimizacao": (
        "COMO OTIMIZAR GAMEUSERSETTINGS.INI MANUALMENTE:\n\n"
        "1. Pressione Win + R, digite '%LOCALAPPDATA%\\VALORANT\\Saved\\Config' e pressione Enter.\n"
        "2. Entre em uma das pastas (UUID) e localize 'GameUserSettings.ini'.\n"
        "3. Clique com o botão direito > Abrir com > Bloco de Notas.\n"
        "4. Procure ou adicione as seguintes linhas em '[SystemSettings]':\n"
        "   r.VSync=0\n   r.ShadowQuality=0\n   r.BloomQuality=0\n   r.MotionBlurQuality=0\n   r.MotionBlurQuality=0\n   r.DepthOfFieldQuality=0\n   r.LensFlareQuality=0\n   r.AmbientOcclusionLevels=0\n   r.PostProcessAAQuality=0\n   r.Tonemapper.Sharpen=0\n   r.DynamicShadows=0\n   r.DynamicShadowsMeshDistance=0\n   r.Shadow.MaxCSMCascades=1\n   r.Shadow.MaxWholeSceneShadowDistance=1000\n\n"
        "5. Salve o arquivo e reinicie o VALORANT.\n\n"
        "Faça um backup do arquivo antes de editar."
    ),
    "integridade": (
        "COMO VERIFICAR INTEGRIDADE DO JOGO MANUALMENTE:\n\n"
        "1. Abra o Riot Client.\n"
        "2. Clique no ícone de engrenagem (Configurações) no canto superior direito.\n"
        "3. Vá em 'Jogos' > 'VALORANT'.\n"
        "4. Clique em 'Verificar' ou 'Reparar'.\n"
        "5. Aguarde o processo ser concluído e reinicie o computador.\n\n"
        "O Riot Client fará a verificação e reparo automático dos arquivos corrompidos."
    ),
}

class FileCacheTab(ctk.CTkFrame):
    """Aba de Arquivos & Cache."""

    def __init__(self, parent, status_callback, **kwargs):
        super().__init__(parent, fg_color=COLOR_BG, **kwargs)
        self.status_callback = status_callback
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text="Arquivos & Cache",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
            text_color=COLOR_TEXT,
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=PADDING_MAIN)

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Limpeza de arquivos temporários e otimização do GameUserSettings.ini",
            font=(FONT_FAMILY, FONT_SIZE_SUBTITLE),
            text_color=COLOR_TEXT_MUTED,
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, PADDING_MAIN), sticky="w", padx=PADDING_MAIN)

        # Scrollable frame
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLOR_PRIMARY,
            scrollbar_button_hover_color=COLOR_PRIMARY_HOVER,
        )
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        self.grid_rowconfigure(2, weight=1)

        # ============ Card 1: Limpeza Profunda de Cache ============
        card1 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card1.pack(fill="x", pady=(0, 8), padx=5)
        card1.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card1, text="1. LIMPEZA PROFUNDA DE CACHE DO JOGO",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card1,
            text="Remove arquivos temporários (%TEMP%), logs antigos do Valorant/Riot Client e cache de shaders da placa de vídeo para evitar micro-stutters.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_clean = ctk.CTkButton(
            card1,
            text="EXECUTAR LIMPEZA DE CACHE",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_clean_cache,
        )
        btn_clean.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # ============ Card 2: Otimização INI ============
        card2 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card2.pack(fill="x", pady=(0, 8), padx=5)
        card2.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card2, text="2. OTIMIZAÇÃO DO GAMEUSERSETTINGS.INI",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card2,
            text="Localiza os perfis (UUID) do VALORANT e aplica ajustes de desempenho gráfico (desativa VSync, pós-processo pesado, sombras). Cria backup automático antes de editar.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.btn_apply_ini = ctk.CTkButton(
            card2,
            text="APLICAR OTIMIZAÇÃO INI",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_apply_ini,
        )
        self.btn_apply_ini.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.lbl_ini_result = ctk.CTkLabel(
            card2,
            text="",
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_ini_result.grid(row=3, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # ============ Card 3: Reversão de Backup (Undo) ============
        card3 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card3.pack(fill="x", pady=(0, 8), padx=5)
        card3.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card3, text="3. REVERSÃO DE BACKUP (UNDO)",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card3,
            text="Lista e restaura backups do GameUserSettings.ini criados pelo aplicativo. Use caso alguma otimização cause instabilidade no jogo.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_backups_frame = ctk.CTkFrame(card3, fg_color="transparent")
        btn_backups_frame.grid(row=2, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))
        btn_backups_frame.grid_columnconfigure(0, weight=1)

        self.btn_list_backups = ctk.CTkButton(
            btn_backups_frame,
            text="LISTAR BACKUPS DISPONÍVEIS",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_list_backups,
        )
        self.btn_list_backups.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.btn_restore_backup = ctk.CTkButton(
            btn_backups_frame,
            text="RESTAURAR SELECIONADO",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_SURFACE,
            hover_color="#2a2a33",
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_restore_backup,
            state="disabled",
        )
        self.btn_restore_backup.grid(row=0, column=1, sticky="ew")

        self.backup_combobox = ctk.CTkComboBox(
            btn_backups_frame,
            values=["Nenhum backup"],
            width=260,
            state="disabled",
        )
        self.backup_combobox.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        self.lbl_backup_result = ctk.CTkLabel(
            card3,
            text="",
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_backup_result.grid(row=3, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self._backups_list = []  # lista de caminhos de backup

        # ============ Card 4: Verificação de Integridade ============
        card4 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card4.pack(fill="x", pady=(0, 8), padx=5)
        card4.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card4, text="4. VERIFICAÇÃO DE INTEGRIDADE DO JOGO",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card4,
            text="Abre o Riot Client e dispara a verificação de integridade dos arquivos do VALORANT, sem modificar memória nem injetar código.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_integrity = ctk.CTkButton(
            card4,
            text="VERIFICAR INTEGRIDADE DO JOGO",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_integrity,
        )
        btn_integrity.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # ============ Card 5: Limpeza Expandida ============
        card5 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card5.pack(fill="x", pady=(0, 8), padx=5)
        card5.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card5, text="5. LIMPEZA EXPANDIDA DE DIRETÓRIOS TEMPORÁRIOS",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card5,
            text="Varre e expurga dados residuais do sistema: %TEMP%, cache do Microsoft Edge, %WINDIR%\\Logs e %SYSTEMROOT%\\Temp. Retorna o volume total liberado em MB.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_clean_expanded = ctk.CTkButton(
            card5,
            text="EXECUTAR LIMPEZA EXPANDIDA",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_clean_expanded,
        )
        btn_clean_expanded.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.lbl_clean_result = ctk.CTkLabel(
            card5,
            text="",
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_clean_result.grid(row=3, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # ============ Card 6: Limpeza do Windows Update ============
        card6 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card6.pack(fill="x", pady=(0, 8), padx=5)
        card6.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card6, text="6. LIMPEZA DE CACHE DE ATUALIZAÇÕES DO WINDOWS",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card6,
            text="Remove pacotes de instalação antigos do Windows Update de C:\\Windows\\SoftwareDistribution\\Download. Requer privilégios de Administrador.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_clean_wu = ctk.CTkButton(
            card6,
            text="LIMPAR CACHE DO WINDOWS UPDATE",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_clean_windows_update,
        )
        btn_clean_wu.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.lbl_wu_result = ctk.CTkLabel(
            card6,
            text="",
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_wu_result.grid(row=3, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        # ============ Card 7: Esvaziamento da Lixeira ============
        card7 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card7.pack(fill="x", pady=(0, PADDING_MAIN), padx=5)
        card7.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card7, text="7. ESVAZIAMENTO DA LIXEIRA (RECYCLE BIN)",
            font=(FONT_FAMILY_TITLE, 13, "bold"), text_color=COLOR_ACCENT,
        ).grid(row=0, column=0, sticky="w", padx=PADDING_CARD, pady=(PADDING_CARD, 5))

        ctk.CTkLabel(
            card7,
            text="Esvazia todas as Lixeiras de todas as unidades de armazenamento ligadas ao sistema de forma silenciosa via PowerShell.",
            font=(FONT_FAMILY_BODY, FONT_SIZE_BODY),
            text_color=COLOR_TEXT_MUTED,
            wraplength=700, justify="left",
        ).grid(row=1, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        btn_empty_recycle = ctk.CTkButton(
            card7,
            text="ESVAZIAR LIXEIRA",
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=(FONT_FAMILY_BODY, 12, "bold"),
            command=self._on_empty_recycle_bin,
        )
        btn_empty_recycle.grid(row=2, column=0, sticky="ew", padx=PADDING_CARD, pady=(0, PADDING_CARD))

        self.lbl_recycle_result = ctk.CTkLabel(
            card7,
            text="",
            font=(FONT_FAMILY_DATA, FONT_SIZE_SMALL),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_recycle_result.grid(row=3, column=0, sticky="w", padx=PADDING_CARD, pady=(0, PADDING_CARD))

    # Métodos auxiliares continuam aqui...
    def _set_status(self, message: str, color: str = COLOR_TEXT_MUTED):
        if self.status_callback:
            self.status_callback(message, color)

    def _mostrar_instrucao_manual_cache(self, tipo_acao: str, erro_detalhe: str = ""):
        instrucao = INSTRUCOES_MANUAIS_CACHE.get(tipo_acao, ERROS_SEM_SOLUCAO_MANUAL)
        mensagem_completa = f"{instrucao}\n\nDetalhe do erro: {erro_detalhe}"
        self._set_status(mensagem_completa, COLOR_WARNING)

    def _on_clean_cache(self):
        self._set_status("Limpando cache e arquivos temporários...", COLOR_PRIMARY)
        try:
            total_removidos = 0
            total_erros = 0
            mensagens = []

            temp_path = os.environ.get("TEMP", "")
            if temp_path and os.path.isdir(temp_path):
                r, e = safe_remove_dir_contents(temp_path, max_age_days=1)
                total_removidos += r
                total_erros += e
                mensagens.append(f"%TEMP%: {r} arquivo(s) removido(s)")

            local_app_data = os.environ.get("LOCALAPPDATA", "")
            valorant_logs = os.path.join(local_app_data, "VALORANT", "Saved", "Logs")
            if os.path.isdir(valorant_logs):
                r, e = safe_remove_dir_contents(valorant_logs, max_age_days=1)
                total_removidos += r
                total_erros += e
                mensagens.append(f"Logs VALORANT: {r} arquivo(s) removido(s)")

            riot_logs = os.path.join(local_app_data, "Riot Games", "Riot Client", "Logs")
            if os.path.isdir(riot_logs):
                r, e = safe_remove_dir_contents(riot_logs, max_age_days=1)
                total_removidos += r
                total_erros += e
                mensagens.append(f"Logs Riot Client: {r} arquivo(s) removido(s)")

            shader_paths = [
                os.path.join(local_app_data, "NVIDIA", "DXCache"),
                os.path.join(local_app_data, "AMD", "DXCache"),
                os.path.join(local_app_data, "Microsoft", "DirectX"),
            ]
            for sp in shader_paths:
                if os.path.isdir(sp):
                    r, e = safe_remove_dir_contents(sp, max_age_days=7)
                    total_removidos += r
                    total_erros += e
                    mensagens.append(f"Shader Cache ({os.path.basename(sp)}): {r} removido(s)")

            msg = f"Limpeza concluída: {total_removidos} arquivo(s) removido(s)"
            if total_erros > 0:
                msg += f", {total_erros} erro(es) ignorado(s)"

            self._set_status(msg, COLOR_SUCCESS if total_erros == 0 else COLOR_WARNING)
            for m in mensagens:
                print(f"[INFO] {m}")

        except Exception as exc:
            self._mostrar_instrucao_manual_cache("cache_expandido", str(exc))
            logger.error("Erro na limpeza de cache: %s", exc)

    def _on_clean_expanded(self):
        self._set_status("Limpando cache e arquivos temporários...", COLOR_PRIMARY)
        try:
            total_removidos = 0
            total_erros = 0
            total_mb = 0.0
            detalhes = []

            temp_path = os.environ.get("TEMP", "")
            if temp_path and os.path.isdir(temp_path):
                r, e, mb = remove_folder_contents_and_report(temp_path, max_age_days=1)
                total_removidos += r
                total_erros += e
                total_mb += mb
                detalhes.append(f"%TEMP%: {mb:.2f} MB")

            local_app_data = os.environ.get("LOCALAPPDATA", "")
            edge_cache = os.path.join(
                local_app_data,
                "Microsoft", "Edge", "User Data", "Default", "Cache"
            )
            if os.path.isdir(edge_cache):
                r, e, mb = remove_folder_contents_and_report(edge_cache, max_age_days=1)
                total_removidos += r
                total_erros += e
                total_mb += mb
                detalhes.append(f"Edge Cache: {mb:.2f} MB")

            windir_logs = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Logs")
            if os.path.isdir(windir_logs):
                r, e, mb = remove_folder_contents_and_report(windir_logs, max_age_days=7)
                total_removidos += r
                total_erros += e
                total_mb += mb
                detalhes.append(f"Windows Logs: {mb:.2f} MB")

            systemroot_temp = os.path.join(os.environ.get("SYSTEMROOT", "C:\\Windows"), "Temp")
            if os.path.isdir(systemroot_temp):
                r, e, mb = remove_folder_contents_and_report(systemroot_temp, max_age_days=1)
                total_removidos += r
                total_erros += e
                total_mb += mb
                detalhes.append(f"SystemRoot\\Temp: {mb:.2f} MB")

            detalhes_str = " | ".join(detalhes) if detalhes else "Nenhum diretório encontrado"
            msg = (
                f"Limpeza concluída: {total_removidos} arquivo(s) removido(s), "
                f"{total_mb:.2f} MB liberados. | {detalhes_str}"
            )
            if total_erros > 0:
                msg += f" ({total_erros} erro(es) ignorado(s))"

            self.lbl_clean_result.configure(
                text=f"Liberado: {total_mb:.2f} MB", text_color=COLOR_SUCCESS
            )
            self._set_status(msg, COLOR_SUCCESS if total_erros == 0 else COLOR_WARNING)

        except Exception as exc:
            self._mostrar_instrucao_manual_cache("cache_expandido", str(exc))
            logger.error("Erro na limpeza expandida: %s", exc)

    # ============ Card 2: Otimização INI ============
    def _on_apply_ini(self):
        """Aplica otimização no GameUserSettings.ini de todos os perfis encontrados."""
        self._set_status("Buscando perfis do VALORANT...", COLOR_PRIMARY)
        try:
            caminho_custom = get_valorant_config_path()
            config_root = find_valorant_config_dir(custom_root=caminho_custom)

            if not config_root:
                self.lbl_ini_result.configure(
                    text="Pasta Config do VALORANT não encontrada. Configure o caminho na aba Configuração.",
                    text_color=COLOR_DANGER,
                )
                self._set_status("Pasta Config não encontrada.", COLOR_WARNING)
                return

            profiles = list_profile_dirs(config_root)
            if not profiles:
                self.lbl_ini_result.configure(
                    text="Nenhum perfil do VALORANT encontrado.",
                    text_color=COLOR_WARNING,
                )
                self._set_status("Nenhum perfil encontrado.", COLOR_WARNING)
                return

            ajustes = {
                "SystemSettings": {
                    "r.VSync": "0",
                    "r.ShadowQuality": "0",
                    "r.BloomQuality": "0",
                    "r.MotionBlurQuality": "0",
                    "r.DepthOfFieldQuality": "0",
                    "r.LensFlareQuality": "0",
                    "r.AmbientOcclusionLevels": "0",
                    "r.PostProcessAAQuality": "0",
                    "r.Tonemapper.Sharpen": "0",
                    "r.DynamicShadows": "0",
                    "r.DynamicShadowsMeshDistance": "0",
                    "r.Shadow.MaxCSMCascades": "1",
                    "r.Shadow.MaxWholeSceneShadowDistance": "1000",
                },
            }

            total_editados = 0
            total_erros = 0
            for profile_dir in profiles:
                ini_path = find_game_user_settings(profile_dir)
                if not ini_path:
                    continue
                # Cria backup automático antes de editar
                backup_file(ini_path)

                try:
                    parser = configparser.ConfigParser()
                    parser.read(ini_path, encoding="utf-8")

                    for secao, valores in ajustes.items():
                        if not parser.has_section(secao):
                            parser.add_section(secao)
                        for chave, valor in valores.items():
                            parser.set(secao, chave, valor)

                    with open(ini_path, "w", encoding="utf-8") as f:
                        parser.write(f)

                    total_editados += 1
                except Exception as exc:
                    logger.error("Erro ao editar %s: %s", ini_path, exc)
                    total_erros += 1

            msg = f"INI otimizado em {total_editados} perfil(is)."
            if total_erros > 0:
                msg += f" ({total_erros} erro(es))."

            self.lbl_ini_result.configure(text=msg, text_color=COLOR_SUCCESS if total_erros == 0 else COLOR_WARNING)
            self._set_status(msg, COLOR_SUCCESS if total_erros == 0 else COLOR_WARNING)

        except Exception as exc:
            self._mostrar_instrucao_manual_cache("ini_otimizacao", str(exc))
            logger.error("Erro na otimização INI: %s", exc)

    # ============ Card 3: Backup / Undo ============
    def _on_list_backups(self):
        """Lista os backups disponíveis no combo box."""
        self._set_status("Listando backups...", COLOR_PRIMARY)
        try:
            caminho_custom = get_valorant_config_path()
            config_root = find_valorant_config_dir(custom_root=caminho_custom)

            if not config_root:
                self.lbl_backup_result.configure(
                    text="Pasta Config do VALORANT não encontrada.",
                    text_color=COLOR_WARNING,
                )
                self._set_status("Pasta Config não encontrada.", COLOR_WARNING)
                return

            profiles = list_profile_dirs(config_root)
            backups_encontrados = []
            for profile_dir in profiles:
                ini_path = find_game_user_settings(profile_dir)
                if not ini_path:
                    continue
                lista = list_available_backups(ini_path)
                for bk in lista:
                    backups_encontrados.append((bk, profile_dir))

            self._backups_list = backups_encontrados

            if not backups_encontrados:
                self.backup_combobox.configure(values=["Nenhum backup encontrado"], state="disabled")
                self.btn_restore_backup.configure(state="disabled")
                self.lbl_backup_result.configure(text="Nenhum backup encontrado.", text_color=COLOR_TEXT_MUTED)
                self._set_status("Nenhum backup disponível.", COLOR_TEXT_MUTED)
                return

            labels = []
            for bk_path, prof_dir in backups_encontrados:
                nome_perfil = os.path.basename(prof_dir)
                nome_arquivo = os.path.basename(bk_path)
                labels.append(f"{nome_perfil} | {nome_arquivo}")

            self.backup_combobox.configure(values=labels, state="readonly")
            self.backup_combobox.set(labels[0])
            self.btn_restore_backup.configure(state="normal")
            self.lbl_backup_result.configure(
                text=f"{len(backups_encontrados)} backup(s) disponível(is).",
                text_color=COLOR_SUCCESS,
            )
            self._set_status(f"{len(backups_encontrados)} backup(s) listado(s).", COLOR_SUCCESS)

        except Exception as exc:
            self._mostrar_instrucao_manual_cache("backup", str(exc))
            logger.error("Erro ao listar backups: %s", exc)

    def _on_restore_backup(self):
        """Restaura o backup selecionado no combo box."""
        if not self._backups_list:
            return
        indice = self.backup_combobox.current()
        if indice < 0 or indice >= len(self._backups_list):
            return

        backup_path, profile_dir = self._backups_list[indice]
        ini_path = find_game_user_settings(profile_dir)
        if not ini_path:
            self.lbl_backup_result.configure(
                text="Arquivo GameUserSettings.ini não encontrado no perfil.",
                text_color=COLOR_DANGER,
            )
            return

        if restore_backup(backup_path, ini_path):
            self.lbl_backup_result.configure(
                text=f"Backup restaurado: {os.path.basename(backup_path)}",
                text_color=COLOR_SUCCESS,
            )
            self._set_status("Backup restaurado com sucesso.", COLOR_SUCCESS)
        else:
            self.lbl_backup_result.configure(
                text="Falha ao restaurar backup.",
                text_color=COLOR_DANGER,
            )
            self._set_status("Falha ao restaurar backup.", COLOR_DANGER)

    # ============ Card 4: Integridade ============
    def _on_integrity(self):
        """Abre o Riot Client para verificação de integridade do VALORANT."""
        self._set_status("Verificando integridade do jogo...", COLOR_PRIMARY)
        try:
            riot_client = r"C:\Program Files\Riot Client\RiotClientServices.exe"
            if not os.path.isfile(riot_client):
                # tenta caminho alternativo
                riot_client = r"C:\Riot Games\Riot Client\RiotClientServices.exe"

            if os.path.isfile(riot_client):
                ok, msg = run_cmd(f'"{riot_client}" --repair', timeout=30)
                if ok:
                    self._set_status("Riot Client iniciado para verificação de integridade.", COLOR_SUCCESS)
                else:
                    # Tenta apenas abrir o cliente
                    ok2, msg2 = run_cmd(f'"{riot_client}"', timeout=30)
                    if ok2:
                        self._set_status("Riot Client aberto. Use a opção Verificar/Reparar manualmente.", COLOR_WARNING)
                    else:
                        self._set_status(f"Falha ao abrir Riot Client: {msg2}", COLOR_DANGER)
            else:
                self._mostrar_instrucao_manual_cache("integridade", "RiotClientServices.exe não encontrado.")
                logger.error("RiotClientServices.exe não encontrado.")
        except Exception as exc:
            self._mostrar_instrucao_manual_cache("integridade", str(exc))
            logger.error("Erro na verificação de integridade: %s", exc)

    # ============ Card 6: Windows Update ============
    def _on_clean_windows_update(self):
        """Para o wuauserv, limpa SoftwareDistribution\\Download e reinicia o serviço."""
        if not is_admin():
            self._set_status("Execute como Administrador para limpar o Windows Update.", COLOR_WARNING)
            return

        self._set_status("Limpando cache do Windows Update...", COLOR_PRIMARY)
        try:
            wu_path = r"C:\Windows\SoftwareDistribution\Download"
            if not os.path.isdir(wu_path):
                self.lbl_wu_result.configure(text="Pasta do Windows Update não encontrada.", text_color=COLOR_WARNING)
                self._set_status("Pasta do Windows Update não encontrada.", COLOR_WARNING)
                return

            # Para o serviço
            ok_stop, _ = stop_service("wuauserv", timeout=30)

            r, e, mb = remove_folder_contents_and_report(wu_path, max_age_days=1)

            # Reinicia o serviço (ignora erro se já estiver rodando)
            start_service("wuauserv", timeout=30)

            msg = f"Windows Update: {r} arquivo(s) removido(s), {mb:.2f} MB liberados."
            if e > 0:
                msg += f" ({e} erro(es) ignorado(s))."

            self.lbl_wu_result.configure(text=msg, text_color=COLOR_SUCCESS if e == 0 else COLOR_WARNING)
            self._set_status(msg, COLOR_SUCCESS if e == 0 else COLOR_WARNING)

        except Exception as exc:
            self._mostrar_instrucao_manual_cache("windows_update", str(exc))
            logger.error("Erro na limpeza do Windows Update: %s", exc)

    # ============ Card 7: Lixeira ============
    def _on_empty_recycle_bin(self):
        """Esvazia a lixeira de todas as unidades via PowerShell."""
        self._set_status("Esvaziando lixeira...", COLOR_PRIMARY)
        try:
            ok, msg = empty_recycle_bin()
            if ok:
                self.lbl_recycle_result.configure(text="Lixeira esvaziada com sucesso.", text_color=COLOR_SUCCESS)
                self._set_status("Lixeira esvaziada com sucesso.", COLOR_SUCCESS)
            else:
                self.lbl_recycle_result.configure(text=msg, text_color=COLOR_DANGER)
                self._set_status(msg, COLOR_DANGER)
        except Exception as exc:
            self._mostrar_instrucao_manual_cache("lixeira", str(exc))
            logger.error("Erro ao esvaziar lixeira: %s", exc)

    def refresh_translations(self):
        """Reconstroi a UI da aba com os textos do idioma corrente."""
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()