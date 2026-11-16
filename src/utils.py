"""
utils.py
Funções utilitárias compartilhadas: verificação de administrador,
execução segura de comandos do sistema, localização de pastas do VALORANT
e manipulação segura de arquivos.
"""

import os
import ctypes
import subprocess
import logging
import configparser
import shutil
from typing import Optional, Tuple, List
from datetime import datetime, timedelta

try:
    import tkinter.filedialog as fd
except Exception:
    fd = None

logger = logging.getLogger("ValorantOptimizer")

# ============================================================================
# NOVO: Detecção heurística de instalação do VALORANT (Fase 1)
# ============================================================================
COMMON_VALORANT_PATHS = [
    r"C:\Riot Games\VALORANT",
    r"D:\Riot Games\VALORANT",
    r"E:\Riot Games\VALORANT",
    r"C:\Games\Riot Games\VALORANT",
    r"D:\Games\Riot Games\VALORANT",
]


def is_admin() -> bool:
    """
    Verifica se o script está sendo executado com privilégios de Administrador.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def _get_powershell_path() -> str:
    """
    Retorna o caminho completo do powershell.exe.
    """
    caminhos = [
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
        "powershell.exe",
    ]
    for caminho in caminhos:
        if os.path.isfile(caminho) or caminho == "powershell.exe":
            return caminho
    return "powershell.exe"


def run_cmd(command: str, shell: bool = True, timeout: int = 30) -> Tuple[bool, str]:
    """
    Executa um comando do sistema de forma segura.
    Retorna (sucesso, saida_ou_erro).
    """
    try:
        # Se o comando começa com powershell, usa caminho completo
        if command.strip().lower().startswith("powershell"):
            ps_path = _get_powershell_path()
            command = command.replace("powershell", ps_path, 1)

        resultado = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        if resultado.returncode == 0:
            return True, resultado.stdout.strip()
        else:
            return False, resultado.stderr.strip() or f"Código de saída: {resultado.returncode}"
    except subprocess.TimeoutExpired:
        return False, "Tempo limite esgotado ao executar o comando."
    except Exception as exc:  # pylint: disable=broad-except
        return False, str(exc)


def find_valorant_config_dir() -> Optional[str]:
    """
    Localiza o diretório de configurações do VALORANT em %localappdata%.
    """
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        return None

    config_root = os.path.join(local_app_data, "VALORANT", "Saved", "Config")
    return config_root if os.path.isdir(config_root) else None


def list_profile_dirs(config_root: str) -> List[str]:
    """
    Lista subpastas de perfis (UUIDs) dentro da pasta Config.
    """
    profiles: List[str] = []
    try:
        for entry in os.listdir(config_root):
            full_path = os.path.join(config_root, entry)
            if os.path.isdir(full_path):
                profiles.append(full_path)
    except OSError as exc:
        logger.error("Erro ao listar perfis: %s", exc)
    return profiles


def find_game_user_settings(profile_dir: str) -> Optional[str]:
    """
    Verifica se GameUserSettings.ini existe dentro de um perfil.
    """
    ini_path = os.path.join(profile_dir, "GameUserSettings.ini")
    return ini_path if os.path.isfile(ini_path) else None


def safe_remove(path: str) -> bool:
    """
    Remove um arquivo de forma segura, ignorando erros de arquivo em uso.
    """
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
    except OSError:
        pass
    return False


def safe_remove_dir_contents(folder: str, max_age_days: int = 1) -> Tuple[int, int]:
    """
    Remove arquivos de uma pasta, ignorando arquivos em uso ou protegidos.
    max_age_days: remove apenas arquivos mais antigos que X dias (opcional).
    Retorna (removidos, erros).
    """
    removidos = 0
    erros = 0
    limite = datetime.now() - timedelta(days=max_age_days)

    try:
        for entry in os.listdir(folder):
            full_path = os.path.join(folder, entry)
            if not os.path.isfile(full_path):
                continue
            try:
                # Pula arquivos muito recentes (menos de 1 dia) para evitar bloqueios
                mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
                if mtime > limite:
                    continue
                os.remove(full_path)
                removidos += 1
            except OSError:
                erros += 1
    except OSError:
        erros += 1
    return removidos, erros


# --------------------------------------------------------------------------
# NOVO: Detecção heurística de instalação do VALORANT (Fase 1)
# --------------------------------------------------------------------------
def detect_valorant_installation() -> Optional[str]:
    """
    Tenta localizar automaticamente a pasta raiz do VALORANT
    em caminhos conhecidos da Riot Games.
    Retorna o caminho da pasta raiz ou None se não encontrar.
    """
    for base in COMMON_VALORANT_PATHS:
        if os.path.isdir(base):
            # Verifica se existe Saved\Config dentro
            config_check = os.path.join(base, "Saved", "Config")
            if os.path.isdir(config_check):
                return base
    return None


def select_valorant_folder_gui(parent=None) -> Optional[str]:
    """
    Abre um seletor nativo de pastas do Windows.
    Retorna o caminho selecionado ou None se cancelado.
    """
    if fd is None:
        return None
    try:
        folder = fd.askdirectory(
            parent=parent,
            title="Selecione a pasta de instalação do VALORANT",
            initialdir=os.path.expanduser("~"),
        )
        if folder:
            return folder
    except Exception:
        pass
    return None


# ============================================================================
# NOVO: Limpeza expandida de diretórios temporários (Fase 1)
# ============================================================================
def get_folder_size_mb(folder: str) -> float:
    """
    Calcula o tamanho total de uma pasta em Megabytes.
    Retorna 0.0 se a pasta não existir ou houver erro.
    """
    if not os.path.isdir(folder):
        return 0.0
    total_bytes = 0
    try:
        for entry in os.listdir(folder):
            full_path = os.path.join(folder, entry)
            if os.path.isfile(full_path):
                try:
                    total_bytes += os.path.getsize(full_path)
                except OSError:
                    pass
            elif os.path.isdir(full_path):
                try:
                    total_bytes += get_folder_size_mb(full_path) * 1024 * 1024
                except OSError:
                    pass
    except OSError:
        pass
    return total_bytes / (1024 * 1024)


def remove_folder_contents_and_report(folder: str, max_age_days: int = 1) -> Tuple[int, int, float]:
    """
    Remove arquivos de uma pasta e reporta o espaço liberado em MB.
    Retorna (removidos, erros, mb_liberado).
    """
    if not os.path.isdir(folder):
        return 0, 0, 0.0

    tamanho_antes = get_folder_size_mb(folder)
    removidos, erros = safe_remove_dir_contents(folder, max_age_days=max_age_days)
    tamanho_depois = get_folder_size_mb(folder)
    mb_liberado = max(0.0, tamanho_antes - tamanho_depois)
    return removidos, erros, mb_liberado


# ============================================================================
# NOVO: Gerenciamento de serviços Windows (Fase 1)
# ============================================================================
def stop_service(service_name: str, timeout: int = 30) -> Tuple[bool, str]:
    """
    Para um serviço do Windows via PowerShell.
    Retorna (sucesso, mensagem).
    """
    comando = f'Stop-Service -Name "{service_name}" -Force -ErrorAction SilentlyContinue'
    ok, saida = run_cmd(f'powershell -Command "{comando}"', timeout=timeout)
    if ok:
        return True, f"Serviço '{service_name}' parado com sucesso."
    return False, f"Falha ao parar '{service_name}': {saida}"


def start_service(service_name: str, timeout: int = 30) -> Tuple[bool, str]:
    """
    Inicia um serviço do Windows via PowerShell.
    Retorna (sucesso, mensagem).
    """
    comando = f'Start-Service -Name "{service_name}" -ErrorAction SilentlyContinue'
    ok, saida = run_cmd(f'powershell -Command "{comando}"', timeout=timeout)
    if ok:
        return True, f"Serviço '{service_name}' iniciado com sucesso."
    return False, f"Falha ao iniciar '{service_name}': {saida}"


def set_valorant_priority_high() -> tuple[bool, str]:
    """
    Define a prioridade do processo VALORANT como Alta.
    Retorna (sucesso, mensagem).
    """
    try:
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] and proc.info["name"].lower() == VALORANT_EXE.lower():
                    proc.nice(PRIORIDADE_ALTA)
                    return True, f"Prioridade Alta aplicada ao VALORANT (PID {proc.pid})."
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False, "VALORANT não está em execução no momento."
    except Exception as exc:
        logger.error("Falha ao elevar prioridade do VALORANT: %s", exc)
        return False, f"Erro: {exc}"


# ============================================================================
# NOVO: Esvaziamento da Lixeira (Recycle Bin) (Fase 1)
# ============================================================================
def empty_recycle_bin() -> Tuple[bool, str]:
    """
    Esvazia a lixeira de todas as unidades via PowerShell.
    Retorna (sucesso, mensagem).
    """
    comando = 'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'
    ok, saida = run_cmd(f'powershell -Command "{comando}"', timeout=30)
    if ok:
        return True, "Lixeira esvaziada com sucesso."
    return False, f"Falha ao esvaziar lixeira: {saida}"


# ============================================================================
# NOVO: Gerenciamento do SysMain / SuperFetch (Fase 1)
# ============================================================================
def get_sysmain_status() -> str:
    """
    Retorna o status do serviço SysMain (SuperFetch).
    """
    return get_service_status("SysMain")


def set_sysmain_status(enable: bool) -> Tuple[bool, str]:
    """
    Ativa ou desativa o serviço SysMain.
    Se enable=False, para o serviço e define desabilitado.
    Se enable=True, inicia o serviço e define automático.
    Retorna (sucesso, mensagem).
    """
    # Primeiro para ou inicia
    if enable:
        ok, msg = start_service("SysMain")
        if not ok:
            return False, msg
        # Define início automático
        comando = 'Set-Service -Name "SysMain" -StartupType Automatic -ErrorAction SilentlyContinue'
        run_cmd(f'powershell -Command "{comando}"', timeout=15)
        return True, "SysMain (SuperFetch) ativado e definido como Automático."
    else:
        ok, msg = stop_service("SysMain")
        if not ok:
            return False, msg
        # Define desabilitado
        comando = 'Set-Service -Name "SysMain" -StartupType Disabled -ErrorAction SilentlyContinue'
        run_cmd(f'powershell -Command "{comando}"', timeout=15)
        return True, "SysMain (SuperFetch) desativado e definido como Desabilitado."


# Mensagem centralizada de erro sem solução manual automática.
ERROS_SEM_SOLUCAO_MANUAL = (
    "No momento não é possível realizar esta ação automaticamente.\n"
    "Estamos trabalhando para resolver este problema em uma próxima atualização.\n"
    "Tente executar o aplicativo como Administrador ou reinicie o computador e tente novamente."
)