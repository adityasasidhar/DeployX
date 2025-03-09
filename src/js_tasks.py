import esprima

def run_js_linter(files):
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            js_code = f.read()
            try:
                esprima.parseScript(js_code)
                print(f"✅ {file} passed JavaScript linting")
            except Exception as e:
                print(f"❌ {file} has JavaScript issues:\n{e}")