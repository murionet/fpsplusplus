"""
system_optimizer.py
Funções de otimização do sistema para o VALORANT.
"""

import os
import logging
import psutil
import winreg
from utils import run_cmd

logger = logging.getLogger("ValorantOptimizer")

VALORANT_EXE = "VALORANT-Win64-Shipping.exe"

def set_valorant_priority_high() -> tuple[bool, str]:
    """
    Define a prioridade do processo VALORANT como Alta.
    """
    try:
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"] and proc.info["name"].lower() == VALORANT_EXE.lower():
                    proc.nice(psutil.HIGH_PRIORITY_CLASS)
                    return True, f"Prioridade Alta aplicada ao VALORANT (PID {proc.pid})."
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False, "VALORANT não está em execução."
    except Exception as exc:
        logger.error("Falha ao elevar prioridade do VALORANT: %s", exc)
        return False, f"Erro: {exc}"