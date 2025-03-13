from src.runcommand import run_command
from lxml import etree, html

def run_htmlhint(files):
    if files:
        run_command(f"htmlhint {' '.join(files)}", "HTMLHint")


def is_valid_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        html.fromstring(content)
        return True
    except etree.XMLSyntaxError:
        return False


print(is_valid_html('../TestStaticSite/index.html'))