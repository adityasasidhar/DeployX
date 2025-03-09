import os
import collections

def get_lang_percentage(directory):
    lange_extension = {
        "Python": [".py"],
        "HTML": [".html", ".htm"],
        "JavaScript": [".js", ".mjs", ".cjs", ".jsx"],
        "CSS": [".css", ".scss", ".sass", ".less"],
        "Markdown": [".md", ".markdown"],
        "JSON": [".json", ".geojson", ".json5"],
        "YAML": [".yaml", ".yml"],
        "XML": [".xml", ".xsd", ".xsl", ".xslt"],
        "Java": [".java", ".class", ".jar"],
        "C": [".c", ".h"],
        "C++": [".cpp", ".cc", ".cxx", ".hpp", ".hxx"],
        "C#": [".cs"],
        "PHP": [".php", ".php3", ".php4", ".php5", ".phtml"],
        "Ruby": [".rb", ".erb", ".rake"],
        "Shell": [".sh", ".bash", ".zsh"],
        "Perl": [".pl", ".pm"],
        "R": [".r", ".R"],
        "Go": [".go"],
        "Rust": [".rs", ".rlib"],
        "Swift": [".swift"],
        "Kotlin": [".kt", ".kts"],
        "TypeScript": [".ts", ".tsx"],
        "Dart": [".dart"],
        "Scala": [".scala", ".sc"],
        "Lua": [".lua"],
        "Haskell": [".hs", ".lhs"],
        "Objective-C": [".m", ".mm"],
        "SQL": [".sql"],
        "PowerShell": [".ps1", ".psm1"],
        "MATLAB": [".m"],
        "Julia": [".jl"],
        "Elixir": [".ex", ".exs"],
        "F#": [".fs", ".fsi", ".fsx"],
        "Fortran": [".f90", ".f95", ".f03", ".f"],
        "COBOL": [".cbl", ".cob", ".cpy"],
        "Ada": [".adb", ".ads"],
        "Erlang": [".erl", ".hrl"],
        "Lisp": [".lisp", ".cl", ".el"],
        "Scheme": [".scm", ".ss"],
        "Prolog": [".pl", ".pro"],
        "VHDL": [".vhdl", ".vhd"],
        "Verilog": [".v", ".vh"],
        "Pascal": [".pas", ".pp"],
        "Racket": [".rkt"],
        "Tcl": [".tcl"],
        "GraphQL": [".graphql", ".gql"],
        "Dockerfile": [".dockerfile"],
        "Makefile": [".mk"],
        "CMake": [".cmake"],
        "Bash": [".sh", ".bash"],
        "Jupyter Notebook": [".ipynb"]
    }
    lang_counts = collections.defaultdict(int)
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            for lang, extensions in lange_extension.items():
                if ext in extensions:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        line_count = sum(1 for _ in f)
                        lang_counts[lang] += line_count
                        total_lines += line_count
    if total_lines == 0:
        print("❌ No files found to scan!")
        return
    lang_percentages = {lang: round((count / total_lines) * 100, 1) for lang, count in lang_counts.items()}
    print("\n📊 Language Percentage:", lang_percentages)