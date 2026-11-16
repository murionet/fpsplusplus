"""
locale.py - Sistema de tradução para Valorant System Optimizer / FPS++
Suporta: Português (PT) e Inglês (EN)
"""

from typing import Dict

# Dicionário de traduções
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Título da janela
    "app_title": {
        "pt": "Fps++",
        "en": "Fps++",
    },
    # Subtítulo
    "app_subtitle": {
        "pt": "Otimizacao de SO e arquivos locais - Sem injetores - Sem modificacao de memoria",
        "en": "OS and local files optimization - No injectors - No memory modification",
    },
    # Aba 1: Arquivos & Cache
    "tab_files": {
        "pt": "Arquivos & Cache",
        "en": "Files & Cache",
    },
    # Aba 2: Game Booster & RAM
    "tab_booster": {
        "pt": "Game Booster & RAM",
        "en": "Game Booster & RAM",
    },
    # Aba 3: Rede & Netcode
    "tab_network": {
        "pt": "Rede & Netcode",
        "en": "Network & Netcode",
    },
    # Aba 4: Otimizações do Windows
    "tab_windows": {
        "pt": "Otimizacoes do Windows",
        "en": "Windows Optimizations",
    },
    # Aba 5: Configuração
    "tab_settings": {
        "pt": "Configuracao",
        "en": "Settings",
    },
    # Botão de idioma
    "btn_language": {
        "pt": "EN",
        "en": "PT",
    },
    # Barra de status
    "status_ready": {
        "pt": "Pronto.",
        "en": "Ready.",
    },
    # --- Aba 1: Arquivos & Cache ---
    "card_cache_title": {
        "pt": "1. LIMPEZA PROFUNDA DE CACHE DO JOGO",
        "en": "1. DEEP GAME CACHE CLEANUP",
    },
    "cache_desc": {
        "pt": "Remove arquivos temporarios (%TEMP%), logs antigos do Valorant/Riot Client e cache de shaders da placa de video para evitar micro-stutters.",
        "en": "Removes temporary files (%TEMP%), old Valorant/Riot Client logs and DirectX shader cache from graphics card to avoid micro-stutters.",
    },
    "btn_clean_cache": {
        "pt": "EXECUTAR LIMPEZA DE CACHE",
        "en": "RUN CACHE CLEANUP",
    },
    "card_ini_title": {
        "pt": "2. OTIMIZACAO DO GAMEUSERSETTINGS.INI",
        "en": "2. GAMEUSERSETTINGS.INI OPTIMIZATION",
    },
    "ini_desc": {
        "pt": "Localiza automaticamente os perfis (UUIDs) do VALORANT e aplica ajustes de desempenho grafico (desativa VSync, pos-processo pesado, sombras).",
        "en": "Automatically locates VALORANT profiles (UUIDs) and applies performance graphics settings (disables VSync, heavy post-processing, shadows).",
    },
    "btn_apply_ini": {
        "pt": "APLICAR OTIMIZACAO INI",
        "en": "APPLY INI OPTIMIZATION",
    },
    "card_backup_title": {
        "pt": "3. REVERSÃO DE BACKUP (UNDO)",
        "en": "3. BACKUP REVERSAL (UNDO)",
    },
    "backup_desc": {
        "pt": "Lista e restaura backups do GameUserSettings.ini criados pelo aplicativo. Use caso alguma otimizacao cause instabilidade no jogo.",
        "en": "Lists and restores GameUserSettings.ini backups created by the application. Use if some optimization causes game instability.",
    },
    "btn_list_backups": {
        "pt": "LISTAR BACKUPS DISPONIVEIS",
        "en": "LIST AVAILABLE BACKUPS",
    },
    "btn_restore_backup": {
        "pt": "RESTAURAR SELECIONADO",
        "en": "RESTORE SELECTED",
    },
    "no_backups": {
        "pt": "Nenhum backup encontrado.",
        "en": "No backups found.",
    },
    "card_riot_title": {
        "pt": "4. VERIFICACAO DE INTEGRIDADE DO JOGO",
        "en": "4. GAME INTEGRITY CHECK",
    },
    "integrity_desc": {
        "pt": "Abre o Riot Client e dispara a verificacao de integridade dos arquivos do VALORANT, corrompidos ou ausentes, sem modificar memoria nem injetar codigo.",
        "en": "Opens Riot Client and triggers VALORANT file integrity check for corrupted or missing files, without modifying memory or injecting code.",
    },
    "btn_integrity": {
        "pt": "VERIFICAR INTEGRIDADE DO JOGO",
        "en": "VERIFY GAME INTEGRITY",
    },
    "card_expanded_title": {
        "pt": "5. LIMPEZA EXPANDIDA DE DIRETORIOS TEMPORARIOS",
        "en": "5. EXPANDED TEMPORARY DIRECTORIES CLEANUP",
    },
    "expanded_desc": {
        "pt": "Varre e expurga dados residuais do sistema e aplicacoes de terceiros: %TEMP%, cache do Microsoft Edge, %WINDIR%\\Logs e %SYSTEMROOT%\\Temp. Retorna o volume total liberado em MB.",
        "en": "Scans and purges residual data from system and third-party applications: %TEMP%, Microsoft Edge cache, %WINDIR%\\Logs and %SYSTEMROOT%\\Temp. Returns total space freed in MB.",
    },
    "btn_clean_expanded": {
        "pt": "EXECUTAR LIMPEZA EXPANDIDA",
        "en": "RUN EXPANDED CLEANUP",
    },
    "card_wu_title": {
        "pt": "6. LIMPEZA DE CACHE DE ATUALIZACOES DO WINDOWS",
        "en": "6. WINDOWS UPDATE CACHE CLEANUP",
    },
    "wu_desc": {
        "pt": "Remove pacotes de instalacao antigos do Windows Update da pasta C:\\Windows\\SoftwareDistribution\\Download. O servico wuauserv e parado temporariamente e reiniciado automaticamente. Requer privilegios de Administrador.",
        "en": "Removes old Windows Update installation packages from C:\\Windows\\SoftwareDistribution\\Download. wuauserv service is stopped temporarily and restarted automatically. Requires Administrator privileges.",
    },
    "btn_clean_wu": {
        "pt": "LIMPAR CACHE DO WINDOWS UPDATE",
        "en": "CLEAN WINDOWS UPDATE CACHE",
    },
    "card_recycle_title": {
        "pt": "7. ESVAZIAMENTO DA LIXEIRA (RECYCLE BIN)",
        "en": "7. RECYCLE BIN EMPTYING",
    },
    "recycle_desc": {
        "pt": "Esvazia todas as Lixeiras de todas as unidades de armazenamento ligadas ao sistema de forma silenciosa via PowerShell.",
        "en": "Empties the Recycle Bin of all storage drives connected to the system silently via PowerShell.",
    },
    "btn_empty_recycle": {
        "pt": "ESVAZIAR LIXEIRA",
        "en": "EMPTY RECYCLE BIN",
    },
    # --- Aba 2: Game Booster & RAM ---
    "card_focus_title": {
        "pt": "1. MODO FOCO AUTOMATICO (PROCESS MONITOR)",
        "en": "1. AUTOMATIC FOCUS MODE (PROCESS MONITOR)",
    },
    "focus_desc": {
        "pt": "Quando ativado, o app detecta o lancamento do VALORANT-Win64-Shipping.exe, eleva sua prioridade para 'Alta' e reduz a prioridade de navegadores/launchers em segundo plano.",
        "en": "When enabled, the app detects VALORANT-Win64-Shipping.exe launch, elevates its priority to 'High' and reduces browsers/launchers background priority.",
    },
    "btn_toggle_focus": {
        "pt": "ATIVAR MODO FOCO",
        "en": "ENABLE FOCUS MODE",
    },
    "btn_toggle_focus_off": {
        "pt": "DESACTIVAR MODO FOCO",
        "en": "DISABLE FOCUS MODE",
    },
    "status_monitor_on": {
        "pt": "Monitor: Ativo",
        "en": "Monitor: Active",
    },
    "status_monitor_off": {
        "pt": "Monitor: Desativado",
        "en": "Monitor: Inactive",
    },
    "card_ram_title": {
        "pt": "2. LIMPEZA DE STANDBY LIST (RAM)",
        "en": "2. STANDBY LIST CLEANUP (RAM)",
    },
    "ram_desc": {
        "pt": "Tenta liberar a memoria em espera (Standby Memory) do Windows, que pode causar perda de desempenho apos varias partidas seguidas.",
        "en": "Attempts to free Windows Standby Memory, which can cause performance loss after several consecutive matches.",
    },
    "btn_clean_ram": {
        "pt": "LIMPAR STANDBY LIST",
        "en": "CLEAN STANDBY LIST",
    },
    # --- Aba 3: Rede & Netcode ---
    "card_tcp_title": {
        "pt": "1. OTIMIZACAO DE TCP/IP PARA JOGOS",
        "en": "1. TCP/IP OPTIMIZATION FOR GAMES",
    },
    "tcp_desc": {
        "pt": "Aplica TcpAckFrequency=1 e TCPNoDelay=1 em todas as interfaces de rede para reduzir a latencia (ping) e melhorar o registro de tiros. Requer privilegios de Administrador.",
        "en": "Applies TcpAckFrequency=1 and TCPNoDelay=1 on all network interfaces to reduce latency (ping) and improve shot registration. Requires Administrator privileges.",
    },
    "btn_tcp": {
        "pt": "APLICAR OTIMIZACAO TCP/IP",
        "en": "APPLY TCP/IP OPTIMIZATION",
    },
    "card_net_title": {
        "pt": "2. GERENCIAMENTO DE ENERGIA DA PLACA DE REDE",
        "en": "2. NETWORK CARD POWER MANAGEMENT",
    },
    "net_desc": {
        "pt": "Desativa o gerenciamento de energia da placa Ethernet/Wi-Fi para evitar oscilacoes de pacotes e latencia instavel.",
        "en": "Disables Ethernet/Wi-Fi network card power management to avoid packet oscillation and unstable latency.",
    },
    "btn_net_power": {
        "pt": "DESACTIVAR GERENCIAMENTO DE ENERGIA",
        "en": "DISABLE POWER MANAGEMENT",
    },
    "card_dns_title": {
        "pt": "3. LIMPEZA DE CACHE DE REDE (DNS/ARP)",
        "en": "3. NETWORK CACHE CLEANUP (DNS/ARP)",
    },
    "dns_desc": {
        "pt": "Executa ipconfig /flushdns e arp -d para limpar cache de sockets locais e mitigar perdas de pacotes por corrupcao na tabela de roteamento.",
        "en": "Executes ipconfig /flushdns and arp -d to clear local socket cache and mitigate packet loss due to routing table corruption.",
    },
    "btn_dns": {
        "pt": "LIMPAR DNS E ARP",
        "en": "CLEAN DNS AND ARP",
    },
    # --- Aba 4: Otimizacoes do Windows ---
    "card_energy_title": {
        "pt": "1. PLANO DE ENERGIA DE DESEMPENHO MAXIMO",
        "en": "1. MAXIMUM PERFORMANCE POWER PLAN",
    },
    "energy_desc": {
        "pt": "Habilita e aplica o plano oculto 'Desempenho Maximo' (Ultimate Performance) via linha de comando, priorizando a CPU para jogos.",
        "en": "Enables and applies the hidden 'Ultimate Performance' power plan via command line, prioritizing CPU for games.",
    },
    "btn_energy": {
        "pt": "APLICAR DESEMPENHO MAXIMO",
        "en": "APPLY MAXIMUM PERFORMANCE",
    },
    "card_gamebar_title": {
        "pt": "2. DESATIVACAO DE RECURSOS INUTEIS",
        "en": "2. DISABLE USELESS RESOURCES",
    },
    "gamebar_desc": {
        "pt": "Desativa o Xbox Game Bar, Game DVR e gravacoes em segundo plano que consomem recursos de hardware silenciosamente.",
        "en": "Disables Xbox Game Bar, Game DVR and background recordings that silently consume hardware resources.",
    },
    "btn_gamebar": {
        "pt": "DESACTIVAR GAME BAR E GAME DVR",
        "en": "DISABLE GAME BAR AND GAME DVR",
    },
    "card_diag_title": {
        "pt": "3. PAINEL DE DIAGNOSTICO E ALERTAS",
        "en": "3. DIAGNOSTIC AND ALERTS PANEL",
    },
    "diag_text": {
        "pt": "XMP/DOCP: Verifique na BIOS se o perfil XMP (Intel) ou DOCP (AMD) da memoria RAM esta ativado. Sem ele, a RAM opera em velocidade padrao, reduzindo o FPS minimo. Limite de FPS ideal: defina no VALORANT um limite igual a taxa do monitor menos 3 quadros. Exemplos: 144 Hz → 141 FPS | 240 Hz → 237 FPS | 165 Hz → 162 FPS. Isso estabiliza o Frame Time com VRR / G-Sync / FreeSync ativo. Modo de Jogo: certifique-se de que o 'Modo de Jogo' do Windows esta Ativado.",
        "en": "XMP/DOCP: Check in BIOS if XMP (Intel) or DOCP (AMD) RAM profile is enabled. Without it, RAM operates at standard speed, reducing minimum FPS. Ideal FPS limit: set in VALORANT a limit equal to monitor refresh rate minus 3 frames. Examples: 144 Hz → 141 FPS | 240 Hz → 237 FPS | 165 Hz → 162 FPS. This stabilizes Frame Time with VRR / G-Sync / FreeSync active. Game Mode: make sure Windows 'Game Mode' is Enabled.",
    },
    "card_sysmain_title": {
        "pt": "4. GERENCIAMENTO DO SYSMAIN (SUPERFETCH)",
        "en": "4. SYSMAIN (SUPERFETCH) MANAGEMENT",
    },
    "sysmain_desc": {
        "pt": "O SysMain (antigo SuperFetch) pré-carrega aplicativos na RAM. Em SSDs de alta performance, desativá-lo pode reduzir gravacoes desnecessarias em segundo plano. Requer privilegios de Administrador.",
        "en": "SysMain (formerly SuperFetch) pre-loads applications into RAM. On high-performance SSDs, disabling it can reduce unnecessary background writes. Requires Administrator privileges.",
    },
    "btn_sysmain_disable": {
        "pt": "DESACTIVAR SYSMAIN",
        "en": "DISABLE SYSMAIN",
    },
    "btn_sysmain_enable": {
        "pt": "ATIVAR SYSMAIN",
        "en": "ENABLE SYSMAIN",
    },
    "sysmain_status_on": {
        "pt": "Status: ATIVO (Running)",
        "en": "Status: ACTIVE (Running)",
    },
    "sysmain_status_off": {
        "pt": "Status: DESATIVADO (Stopped)",
        "en": "Status: INACTIVE (Stopped)",
    },
    # --- Aba 5: Configuracao ---
    "card_path_title": {
        "pt": "1. CAMINHO DA PASTA DO VALORANT",
        "en": "1. VALORANT FOLDER PATH",
    },
    "path_desc": {
        "pt": "Informe a pasta raiz da instalacao do VALORANT (ex: D:\\Riot Games\\VALORANT). O aplicativo procurara automaticamente a subpasta Saved\\Config dentro dela.",
        "en": "Enter the VALORANT installation root folder (ex: D:\\Riot Games\\VALORANT). The application will automatically look for the Saved\\Config subfolder inside it.",
    },
    "btn_change_path": {
        "pt": "ALTERAR CAMINHO (POPUP)",
        "en": "CHANGE PATH (POPUP)",
    },
    "btn_reset_path": {
        "pt": "USAR PADRAO",
        "en": "USE DEFAULT",
    },
    "card_desc_title": {
        "pt": "2. O QUE CADA FUNCAO FAZ",
        "en": "2. WHAT EACH FUNCTION DOES",
    },
    "card_security_title": {
        "pt": "3. SEGURANCA (RIOT VANGUARD)",
        "en": "3. SECURITY (RIOT VANGUARD)",
    },
    "security_text": {
        "pt": "SEGURANCA (RIOT VANGUARD)\n\nEste aplicativo NAO modifica memoria, NAO injeta DLLs e NAO altera arquivos .pak do VALORANT.\nTodas as acoes sao:\n• Edicao local do GameUserSettings.ini (com backup automatico)\n• Comandos administrativos seguros do Windows (registro, powercfg, etc.)\n• Limpeza de pastas de cache e temp do proprio usuario",
        "en": "SECURITY (RIOT VANGUARD)\n\nThis application DOES NOT modify memory, DOES NOT inject DLLs and DOES NOT alter VALORANT .pak files.\nAll actions are:\n• Local GameUserSettings.ini editing (with automatic backup)\n• Safe Windows administrative commands (registry, powercfg, etc.)\n• Cleanup of user's own cache and temp folders",
    },
    # Erros comuns
    "err_admin": {
        "pt": "Execute o aplicativo como Administrador.",
        "en": "Run the application as Administrator.",
    },
    "err_no_path": {
        "pt": "Pasta do VALORANT nao encontrada. Configure o caminho na aba 'Configuracao'.",
        "en": "VALORANT folder not found. Configure the path in 'Settings' tab.",
    },
    "err_no_profiles": {
        "pt": "Nenhum perfil do VALORANT encontrado.",
        "en": "No VALORANT profiles found.",
    },
    "err_no_cache": {
        "pt": "Nenhuma pasta de cache encontrada para limpeza.",
        "en": "No cache folder found for cleanup.",
    },
}

# Idioma atual (padrão: inglês)
_current_lang = "en"


def set_language(lang_code: str):
    """Define o idioma atual da aplicação."""
    global _current_lang
    if lang_code in ("en", "pt"):
        _current_lang = lang_code


def get_language() -> str:
    """Retorna o idioma atual."""
    return _current_lang


def t(key: str) -> str:
    """
    Retorna o texto traduzido para a chave dada no idioma atual.
    Se a chave não existir, retorna a própria chave.
    """
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(_current_lang, key)
    return key