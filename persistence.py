import json
import sys
from pathlib import Path

DEFAULTS = {
    'high_score': 0,
}

def _safe_log(message):
    try:
        if sys.stdout is not None:
            print(message)
    except Exception:
        pass

def _get_save_paths():
    if getattr(sys, 'frozen', False):
        legacy_file = (Path(sys.executable).parent / 'save_data.json').resolve()
    else:
        legacy_file = (Path(__file__).parent / 'save_data.json').resolve()

    try:
        save_dir = Path.home() / ".coin_game"
        data_file = (save_dir / 'save_data.json').resolve()
    except RuntimeError:
        save_dir = legacy_file.parent
        data_file = legacy_file

    return save_dir, data_file, legacy_file

def load():
    save_dir, data_file, legacy_file = _get_save_paths()
    
    if data_file.exists():
        target_file = data_file
    elif legacy_file.exists():
        target_file = legacy_file
    else:
        return DEFAULTS.copy()

    try:
        with open(target_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        _safe_log(f"Warning: Failed to load game data. {e}")
        return DEFAULTS.copy()
        
    if not isinstance(data, dict):
        _safe_log("Warning: Failed to load game data. Parsed JSON is not a dictionary.")
        return DEFAULTS.copy()
        
    out = DEFAULTS.copy()
    out.update(data)
    return out

def save(data: dict):
    save_dir, data_file, legacy_file = _get_save_paths()
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
        with open(data_file, 'w') as f:
            json.dump(data, f)
    except OSError as e:
        _safe_log(f"Warning: Failed to save game data. {e}")
