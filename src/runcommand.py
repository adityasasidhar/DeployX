import subprocess
def run_command(command, name):
    print(f"\n🔍 Running {name}...")
    subprocess.run(command, shell=True)