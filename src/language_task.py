import os
import collections
def get_lang_percentage(directory):
    lange_extension = {
        "Ada": [".adb", ".ads"], "Bash": [".sh", ".bash"], "C": [".c", ".h"], "C#": [".cs"],
        "C++": [".cpp", ".cc", ".cxx", ".hpp", ".hxx"], "CMake": [".cmake"],
        "COBOL": [".cbl", ".cob", ".cpy"], "CSS": [".css", ".scss", ".sass", ".less"], "Dart": [".dart"],
        "Dockerfile": [".dockerfile"], "Elixir": [".ex", ".exs"], "Erlang": [".erl", ".hrl"],
        "F#": [".fs", ".fsi", ".fsx"], "Fortran": [".f90", ".f95", ".f03", ".f"], "Go": [".go"],
        "GraphQL": [".graphql", ".gql"], "Haskell": [".hs", ".lhs"], "HTML": [".html", ".htm"],
        "Java": [".java", ".class", ".jar"], "JavaScript": [".js", ".mjs", ".cjs", ".jsx"],
        "Jupyter Notebook": [".ipynb"], "JSON": [".json", ".geojson", ".json5"], "Julia": [".jl"],
        "Kotlin": [".kt", ".kts"], "Lisp": [".lisp", ".cl", ".el"], "Lua": [".lua"], "Makefile": [".mk"],
        "Markdown": [".md", ".markdown"], "MATLAB": [".m"], "Objective-C": [".m", ".mm"],
        "Pascal": [".pas", ".pp"], "Perl": [".pl", ".pm"],
        "PHP": [".php", ".php3", ".php4", ".php5", ".phtml"], "PowerShell": [".ps1", ".psm1"],
        "Prolog": [".pl", ".pro"], "Python": [".py"], "R": [".r", ".R"], "Racket": [".rkt"],
        "Ruby": [".rb", ".erb", ".rake"], "Rust": [".rs", ".rlib"], "Scala": [".scala", ".sc"],
        "Scheme": [".scm", ".ss"], "Shell": [".sh", ".bash", ".zsh"], "SQL": [".sql"],
        "Swift": [".swift"], "Tcl": [".tcl"], "TypeScript": [".ts", ".tsx"], "VHDL": [".vhdl", ".vhd"],
        "Verilog": [".v", ".vh"], "XML": [".xml", ".xsd", ".xsl", ".xslt"], "YAML": [".yaml", ".yml"]
    }

    lang_counts = collections.defaultdict(int)
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            for lang, extensions in lange_extension.items():
                if ext in extensions:
                    try:
                        with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                            line_count = sum(1 for _ in f)
                            lang_counts[lang] += line_count
                            total_lines += line_count
                    except:
                        continue
    if total_lines == 0:
        return {}
    lang_percentages = {lang: round((count / total_lines) * 100, 1) for lang, count in lang_counts.items()}
    return lang_percentages
