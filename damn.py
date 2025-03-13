import subprocess

def check_js_syntax(file_path):
    try:
        result = subprocess.run(["node", "--check", file_path], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print("Exception occurred:", e)
        return False


print(check_js_syntax("TestStaticSite/script.js"))