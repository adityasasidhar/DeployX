import os

def get_path():
    for root, dirs, files in os.walk(os.getcwd()):
        print(f"Directory: {root}")
        for d in dirs:
            print(f"  Subdirectory: {d}")
        for f in files:
            print(f"  File: {f}")
