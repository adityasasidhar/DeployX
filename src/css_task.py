import cssutils as cssutils

def run_css_linter(files):
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            css = f.read()
            parser = cssutils.CSSParser()
            try:
                parser.parseString(css)
                print(f"✅ {file} passed CSS linting")
            except Exception as e:
                print(f"❌ {file} has CSS issues:\n{e}")