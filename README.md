# Valorant System Optimizer

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Riot Vanguard Safe](https://img.shields.io/badge/Vanguard-Safe-brightgreen.svg)](README.md#seguran-a-e-conformidade-com-o-riot-vanguard)

Aplicativo desktop leve, minimalista e moderno (Dark Mode) para otimizar o **VALORANT** com foco máximo em **FPS** e estabilidade de **Frame Times**, respeitando estritamente as diretrizes do **Riot Vanguard** — sem modificação de memória, sem injetores, sem alteração de arquivos `.pak`. Apenas ajustes de arquivos de configuração locais permitidos e otimizações de sistema operacional.

---

## Índice

- [Visão Geral](#visão-geral)
- [Segurança e Conformidade com o Riot Vanguard](#segurança-e-conformidade-com-o-riot-vanguard)
- [Funcionalidades Detalhadas](#funcionalidades-detalhadas)
- [Passo a Passo de Instalação e Uso](#passo-a-passo-de-instalação-e-uso)
- [Como Compilar o Executável (`.exe`) e o Instalador](#como-compilar-o-executável-e-o-instalador)
- [Estrutura de Arquivos do Projeto](#estrutura-de-arquivos-do-projeto)
- [Aviso Legal (Disclaimer)](#aviso-legal-disclaimer)

---

## Visão Geral

O **Valorant System Optimizer** é um aplicativo desktop leve e minimalista desenvolvido em **Python com CustomTkinter**, focado em economizar recursos e tokens de processamento, ajudando jogadores competitivos de VALORANT a alcançar o máximo de FPS e estabilidade de quadros.

A interface segue o estilo **HUD Tático Dark Mode**, inspirada na interface do próprio VALORANT e em editores de código modernos, com cores frias (ciano elétrico) e design minimalista.

> **Não são usados injetores, DLLs, ou modificações de memória.** Todas as alterações são feitas apenas em arquivos de configuração locais permitidos pelo usuário e comandos administrativos seguros do Windows.

---

## Segurança e Conformidade com o Riot Vanguard

O aplicativo foi projetado para ser **100% compatível com as diretrizes do Riot Vanguard**. Nenhuma das funcionalidades realizadas pelo software envolve:

| ❌ O QUE O PROJETO NÃO FAZ | ✅ O QUE O PROJETO FAZ |
|---|---|
| Modificar memória do jogo | Editar `GameUserSettings.ini` (arquivo local do usuário) |
| Injetar DLLs ou código externo | Ajustar prioridade de processo via API do Windows |
| Alterar arquivos `.pak` ou recursos do jogo | Limpar arquivos temporários e logs do próprio usuário |
| Contornar sistemas anti-cheat | Executar comandos de sistema permitidos (powercfg, registro, etc.) |
| Acessar memória RAM do processo do jogo | Backup automático antes de qualquer alteração no `.ini` |

**Conclusão:** O uso deste software não configura modificação de cliente, não inibe detecções do Vanguard e não resulta em banimento por modificação de arquivos protegidos.

---

## Funcionalidades Detalhadas (Como Funciona Cada Módulo)

A interface é dividida em 5 abas principais:

### Aba 1 — Arquivos & Cache

| Recurso | O que faz | Comando/Ajuste Aplicado |
|---------|-----------|--------------------------|
| Limpeza Profunda de Cache | Remove arquivos temporários do sistema, logs do Valorant/Riot Client e cache de shaders DirectX | `os.remove()` em pastas temporárias, sem modificar instalação do jogo |
| Otimização `GameUserSettings.ini` | Localiza perfis (UUIDs) e aplica ajustes gráficos de desempenho máximo | Edição de seções `[SystemSettings]`, `[/Script/Engine.Engine]`, `[/Script/VALORANT-Valo.ValoGameUserSettings]` |
| Reversão de Backup (Undo) | Lista e restaura backups automáticos criados antes de cada otimização | Cópia de segurança com timestamp (`*.bak_YYYYMMDD_HHMMSS`) |
| Verificação de Integrência | Abre o Riot Client para verificação de arquivos corrompidos | `RiotClientServices.exe --repair` ou abertura manual do cliente |
| Limpeza Expandida | Remove arquivos de `%TEMP%`, cache do Edge, logs do Windows e Temp do sistema | Remove arquivos antigos (>1 dia) de pastas temporárias |
| Limpeza do Windows Update | Remove pacotes antigos de atualização do Windows | Para o serviço `wuauserv`, limpa `SoftwareDistribution\Download`, reinicia o serviço |
| Esvaziamento da Lixeira | Limpa a Lixeira de todas as unidades | `Clear-RecycleBin -Force` via PowerShell |

### Aba 2 — Game Booster & RAM

| Recurso | O que faz |
|---------|-----------|
| Modo Foco Automático | Monitora o processo `VALORANT-Win64-Shipping.exe` e, quando detectado, eleva sua prioridade para **Alta** e reduz a prioridade de navegadores/launchers secundários |
| Limpeza de Standby List | Tenta liberar a memória em espera (Standby Memory) do Windows via `EmptyStandbyList.exe` (Sysinternals RamMap) ou instruções manuais |

### Aba 3 — Rede & Netcode

| Recurso | O que faz |
|---------|-----------|
| Otimização TCP/IP | Aplica `TcpAckFrequency=1` e `TCPNoDelay=1` no registro do Windows (`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces`) |
| Gerenciamento de Energia da Placa de Rede | Desativa o gerenciamento de energia da placa Ethernet/Wi-Fi via PowerShell (`Disable-NetAdapterPowerManagement`) |
| Limpeza de Cache de Rede | Executa `ipconfig /flushdns` e `arp -d *` com privilégios elevados |

### Aba 4 — Otimizações do Windows

| Recurso | O que faz |
|---------|-----------|
| Plano de Energia | **Tutorial passo a passo** para ativar o plano oculto "Desempenho Máximo" (Ultimate Performance) via `powercfg` |
| Desativar Recursos Inúteis | Desativa Xbox Game Bar, Game DVR e gravações em segundo plano via Registro (`HKCU`) |
| Painel de Diagnóstico | Orienta sobre perfil XMP/DOCP da RAM, limite de FPS ideal (monitor − 3 FPS) e Modo de Jogo do Windows |
| Gerenciamento do SysMain | Ativa ou desativa o serviço SysMain (SuperFetch) para SSDs de alta performance |

### Aba 5 — Configuração

| Recurso | O que faz |
|---------|-----------|
| Caminho do VALORANT | Define o caminho da pasta do VALORANT para localizar o `GameUserSettings.ini` |
| Descrições das Funções | Explica o que cada função do aplicativo faz |
| Segurança (Riot Vanguard) | Explica que não há injetores, modificação de memória ou alteração de .pak |

---

## Passo a Passo de Instalação e Uso

### Opção A: Usuários Finais (via `.bat`)

O aplicativo é distribuído como código-fonte Python. Para executar sem compilar:

1. Baixe o repositório completo deste GitHub (clique em **Code** → **Download ZIP**).
2. Extraia a pasta `valorant-system-optimizer`.
3. Dê duplo-clique no arquivo `executar.bat`.
4. Na primeira execução, clique no botão **"Configurar Caminho Valorant"** e informe a pasta onde o VALORANT está instalado (ex: `D:\Riot Games\VALORANT`).
5. O aplicativo detectará automaticamente a pasta `Saved\Config` e estará pronto para uso.

> ⚠️ **Importante:** Execute o `executar.bat` como **Administrador** (clique com o botão direito → Executar como administrador) para que as funções de rede, plano de energia e limpeza de cache do Windows Update funcionem corretamente.

### Opção B: Desenvolvedores (Rodando via Código-Fonte)

**Requisitos:**
- Windows 10 ou 11
- Python 3.10 ou superior
- Git

**Passos:**

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/valorant-system-optimizer.git
cd valorant-system-optimizer

# 2. Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o aplicativo
python src/main.py
```

> **Nota:** Execute sempre a partir da pasta raiz do repositório (`cd valorant-system-optimizer && python src/main.py`) ou configure o `PYTHONPATH` adequadamente.

Onde baixar o executável (.exe) pronto?
O executável já está compilado e disponível diretamente neste repositório:

Basta baixar o arquivo .exe da versão mais recente e executar.

Como executáveis não assinados digitalmente podem acionar um aviso do Windows SmartScreen, clique em "Mais informações" e depois em "Executar assim mesmo".

O código-fonte permanece aberto neste repositório e pode ser auditado ou compilado manualmente por qualquer pessoa.

O projeto inclui um script `build_exe.bat` que automatiza todo o processo:

```cmd
cd valorant-system-optimizer
build_exe.bat
```

Alternativamente, execute manualmente:

```cmd
# Instale as dependências de build
pip install -r requirements.txt

# Gere o executável
python -m PyInstaller --onefile --windowed --name FpsPlusPlus src/main.py
```

O executável será gerado na pasta `dist/`.

#### Gerar o instalador (`.exe` de instalação)

O projeto inclui um script para o **Inno Setup**:

1. Baixe e instale o [Inno Setup](https://jrsoftware.org/is.php).
2. Abra o arquivo `valorant_optimizer_installer.iss` no Inno Setup Compiler.
3. Clique em **Build**.
4. O instalador será gerado na pasta `installer_output/`.

---

## Estrutura de Arquivos do Projeto

```
valorant-system-optimizer/
├── .github/                  # Configurações específicas do GitHub
│   └── ISSUE_TEMPLATE/       # Modelos para reporte de bugs e sugestões
├── assets/                   # Capturas de tela (prints da UI) para o README e ícones
│   └── icon.ico
├── build/                    # Scripts de empacotamento e instalador
│   ├── build_exe.bat
│   ├── build_icon.py
│   ├── valorant_optimizer.spec
│   └── valorant_optimizer_installer.iss
├── src/                      # Código-fonte principal da aplicação
│   ├── __init__.py
│   ├── main.py               # Ponto de entrada da aplicação
│   ├── styles.py             # Paleta de cores, fontes e dimensões (Dark Mode)
│   ├── utils.py              # Utilitários: admin check, comandos SO, detecção de pastas, limpeza
│   ├── settings_manager.py   # Gerencia config.json, backup com timestamp e telemetria
│   ├── config_dialog.py      # Popup modal para configurar caminho do VALORANT
│   ├── lang.py               # Sistema de tradução PT/EN
│   └── tabs/                 # Subpasta com as 5 abas da interface
│       ├── __init__.py
│       ├── file_cache_tab.py      # Aba 1: Arquivos & Cache
│       ├── game_booster_tab.py    # Aba 2: Game Booster & RAM
│       ├── network_tab.py         # Aba 3: Rede & Netcode
│       ├── windows_tab.py         # Aba 4: Otimizações do Windows
│       └── settings_tab.py        # Aba 5: Configuração
├── .gitignore                # Filtro de arquivos ignorados pelo Git
├── executar.bat              # Atalho rápido na raiz para rodar via Python
├── LICENSE                   # Licença MIT
├── README.md                 # Esta documentação
└── requirements.txt          # Lista de dependências Python
```

---

## Aviso Legal (Disclaimer)

Este projeto é desenvolvido de forma independente e **não possui afiliação oficial com a Riot Games, Riot Vanguard ou a equipe de desenvolvimento do VALORANT**. Todas as marcas registradas pertencem aos seus respectivos proprietários.

O uso deste aplicativo é de responsabilidade do usuário. Embora o software respeite as diretrizes do Riot Vanguard e não modifique memória, não injete DLLs e não altere arquivos `.pak`, o usuário assume total responsabilidade por qualquer consequência decorrente do uso do software.

**Não nos responsabilizamos por banimentos, suspensões ou qualquer outra ação tomada pela Riot Games ou seus sistemas anti-cheat.** Recomendamos que o usuário leia os Termos de Serviço do VALORANT antes de utilizar qualquer ferramenta de otimização de terceiros.

---

**Desenvolvido com foco em desempenho, segurança e transparência.**  
Se encontrar bugs ou tiver sugestões, abra uma issue neste repositório.
