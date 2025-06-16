import os

# Get the script directory for relative file references
exe_dir = os.path.dirname(os.path.abspath(__file__))
python_exe = os.path.join(exe_dir, "python", "python311", "python.exe")
pythonw_exe = os.path.join(exe_dir, "python", "python311", "pythonw.exe")

FILE_PATHS = {
    "app": os.path.join(exe_dir, 'app'),
    "tokens": os.path.join(exe_dir, 'token.json'),
    "creds": os.path.join(exe_dir, 'credentials.json'),
    "autocharge_state": os.path.join(exe_dir, 'autocharge_state.json'),
    "battery_level": os.path.join(exe_dir, 'battery_level.config'),
    "tapo_creds": os.path.join(exe_dir, 'tapo_creds.config')
}

