from runcommand import *

def run_pylint(files):
    if files:
        run_command(f"pylint {' '.join(files)}", "Pylint")

def run_flake8(files):
    if files:
        run_command(f"flake8 {' '.join(files)}", "Flake8")

def run_mypy(files):
    if files:
        run_command(f"mypy {' '.join(files)}", "Mypy")

def run_bandit(files):
    if files:
        run_command(f"bandit -r {' '.join(files)}", "Bandit")