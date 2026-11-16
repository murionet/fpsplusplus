import sys
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

tabs_dir = os.path.join(src_dir, "tabs")
if tabs_dir not in sys.path:
    sys.path.insert(0, tabs_dir)

try:
    from file_cache_tab import FileCacheTab
    print("OK - file_cache_tab importou com sucesso!")
except Exception as e:
    print(f"ERRO ao importar file_cache_tab: {e}")

try:
    from game_booster_tab import GameBoosterTab
    print("OK - game_booster_tab importou com sucesso!")
except Exception as e:
    print(f"ERRO ao importar game_booster_tab: {e}")

try:
    from network_tab import NetworkTab
    print("OK - network_tab importou com sucesso!")
except Exception as e:
    print(f"ERRO ao importar network_tab: {e}")

try:
    from windows_tab import WindowsTab
    print("OK - windows_tab importou com sucesso!")
except Exception as e:
    print(f"ERRO ao importar windows_tab: {e}")

try:
    from settings_tab import SettingsTab
    print("OK - settings_tab importou com sucesso!")
except Exception as e:
    print(f"ERRO ao importar settings_tab: {e}")

try:
    from config_dialog import ValorantConfigDialog
    print("OK - config_dialog importou com sucesso!")
except Exception as e:
    print(f"ERRO ao importar config_dialog: {e}")