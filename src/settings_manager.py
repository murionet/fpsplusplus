"""
settings_manager.py
Gerencia o arquivo de configuracao local do aplicativo,
incluindo o caminho personalizado da pasta do VALORANT,
backup com timestamp, reversao e telemetria de acoes.
"""

import os
import sys
import json
import shutil
import logging
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger("ValorantOptimizer")

SETTINGS_FILE = "config.json"
TELEMETRY_FILE = "optimizer_log.json"


def _get_base_dir() -> str:
    """
    Retorna o diretório base para gravação de arquivos de configuração e telemetria.
    Quando empacotado pelo PyInstaller (sys.frozen), usa o diretório do .exe
    para manter o aplicativo portátil. Em modo desenvolvimento, usa a pasta src/.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

DEFAULT_CONFIG = {
    "valorant_config_path": "",  # vazio = usar padrao %LOCALAPPDATA%
    "last_optimization": None,
    "auto_priority": False,
}


def load_config() -> dict:
    """
    Carrega o arquivo de configuracao local (config.json).
    Retorna o dicionario de configuracao ou valores padrao se nao existir.
    """
    config_path = os.path.join(_get_base_dir(), SETTINGS_FILE)
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, value in DEFAULT_CONFIG.items():
                data.setdefault(key, value)
            return data
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Erro ao carregar configuracao: %s", exc)
            return dict(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> bool:
    """
    Salva o arquivo de configuracao local (config.json).
    Retorna True se sucesso.
    """
    config_path = os.path.join(_get_base_dir(), SETTINGS_FILE)
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logger.info("Configuracao salva em %s", config_path)
        return True
    except OSError as exc:
        logger.error("Erro ao salvar configuracao: %s", exc)
        return False


def get_valorant_config_path() -> Optional[str]:
    """
    Retorna o caminho personalizado da pasta Config do VALORANT,
    ou None se nao estiver definido (usa padrao do sistema).
    """
    config = load_config()
    custom_path = config.get("valorant_config_path", "")
    if custom_path and os.path.isdir(custom_path):
        return custom_path
    return None


def set_valorant_config_path(path: str) -> bool:
    """
    Define o caminho personalizado da pasta Config do VALORANT.
    Retorna True se sucesso.
    """
    config = load_config()
    config["valorant_config_path"] = path
    return save_config(config)


# ============================================================================
# NOVO: Backup com Timestamp (Fase 1)
# ============================================================================
def backup_file(path: str) -> Optional[str]:
    """
    Cria um backup do arquivo com timestamp antes de modificá-lo.
    Formato: GameUserSettings.ini.bak_20261114_223000
    Retorna o caminho do backup ou None.
    """
    if not os.path.isfile(path):
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}.bak_{timestamp}"
    try:
        shutil.copy2(path, backup_path)
        logger.info("Backup criado com timestamp: %s", backup_path)
        return backup_path
    except OSError as exc:
        logger.error("Falha ao criar backup de %s: %s", path, exc)
        return None


def list_available_backups(ini_path: str) -> List[str]:
    """
    Lista todos os backups disponíveis para um determinado arquivo .ini.
    Retorna lista ordenada do mais recente para o mais antigo.
    """
    if not os.path.isfile(ini_path):
        return []

    directory = os.path.dirname(ini_path)
    basename = os.path.basename(ini_path)
    backup_prefix = basename + ".bak_"

    backups: List[str] = []
    try:
        for entry in os.listdir(directory):
            if entry.startswith(backup_prefix):
                full_path = os.path.join(directory, entry)
                if os.path.isfile(full_path):
                    backups.append(full_path)
    except OSError:
        pass

    backups.sort(reverse=True)  # mais recente primeiro
    return backups


def restore_backup(backup_path: str, target_path: str) -> bool:
    """
    Restaura um backup sobre o arquivo alvo.
    Retorna True se sucesso.
    """
    try:
        if not os.path.isfile(backup_path):
            return False
        shutil.copy2(backup_path, target_path)
        logger.info("Backup restaurado: %s -> %s", backup_path, target_path)
        return True
    except OSError as exc:
        logger.error("Falha ao restaurar backup: %s", exc)
        return False


# ============================================================================
# NOVO: Telemetria de Acoes (Fase 1)
# ============================================================================
def log_action(acao: str, detalhe: str, sucesso: bool):
    """
    Registra uma acao executada no arquivo de telemetria local.
    Mantém apenas os últimos 200 registros.
    """
    entrada = {
        "timestamp": datetime.now().isoformat(),
        "acao": acao,
        "detalhe": detalhe,
        "sucesso": sucesso,
    }
    try:
        historico: List[dict] = []
        telemetry_path = os.path.join(_get_base_dir(), TELEMETRY_FILE)
        if os.path.exists(telemetry_path):
            with open(telemetry_path, "r", encoding="utf-8") as f:
                historico = json.load(f)
        historico.append(entrada)
        historico = historico[-200:]
        with open(telemetry_path, "w", encoding="utf-8") as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)
    except Exception:
        pass