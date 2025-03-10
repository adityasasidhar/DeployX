from src.runcommand import run_command

def run_htmlhint(files):
    if files:
        run_command(f"htmlhint {' '.join(files)}", "HTMLHint")