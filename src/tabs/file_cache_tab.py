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
    COLOR_ACCENT, FONT_FAMILY, FONT_FAMILY_TITLE, FONT_FAMILY_BODY, FONT_SIZE_TITLE,
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

        # Card 1: Limpeza de Cache
        card1 = ctk.CTkFrame(self.scroll, fg_color=COLOR_PANEL, corner_radius=CARD_CORNER_RADIUS)
        card1.pack(fill="x", pady=(0, 8), padx=5)
        card1.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card1, text="1. Limpeza Profunda de Cache do Jogo",
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

        # ... resto do código continua aqui
        # (restante do método _build_ui)
    
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

    # ... resto do código continua com os demais métodos ...