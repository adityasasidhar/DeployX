import os
import requests
import shutil
from testing import (
    collect_relevant_files
)

with open('api keys/groq.txt', 'r') as f:
    api_key = f.read().strip()


url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def analyze_all_code_files(directory, api_key_path='api keys/groq.txt'):
    try:
        # Read API key
        with open(api_key_path, 'r') as f:
            api_key = f.read().strip()

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Collect all code from directory
        combined_code = ""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.py', '.js', '.java', '.cpp', '.c', '.html', '.css')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                            combined_code += f"\n--- File: {file} ---\n{code}\n"
                    except Exception as e:
                        print(f"Skipped {file_path}: {e}")

        if not combined_code.strip():
            return "No code files found in the directory."

        # Prepare instructions and payload
        instructions = (
            "Review the following code files for errors only. Do NOT fix anything. Just:\n"
            "1. Mention file name and line/section with issues.\n"
            "2. Explain briefly what the error is.\n"
            "3. Suggest a fix (but do not rewrite code).\n"
            "4. Keep explanations short.\n"
        )

        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "system", "content": "You are a senior software engineer and expert code reviewer."},
                {"role": "user", "content": f"{combined_code}\n\n{instructions}"}
            ],
            "temperature": 0.3,
            "max_tokens": 4096
        }

        # Make API call
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()

    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"
    except Exception as e:
        return f"Error: {e}"



def clean_code_block(code_text):
    lines = code_text.strip().splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()

def fix_the_code(code):

    instructions = ("Fix the syntax errors and make sure the function returns the sum correctly. "
                    "Don't give any explanations, just give clean formatted code, no comments, no extra text.")
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional software engineer and expert code reviewer. "
                    "You must return only the corrected and working version of the code, clean and properly formatted."
                )
            },
            {
                "role": "user",
                "content": f"Fix this code:\n\n{code}\n\nInstructions: {instructions}\n\nOnly return the fixed code. No explanations."
            }
        ],
        "temperature": 0.2,
        "max_tokens": 2048
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        raw_code = response.json()['choices'][0]['message']['content'].strip()
        return clean_code_block(raw_code)


    else:
        print("❌ Error:", response.status_code, response.text)
        return None

def fix_a_project(project_path):
    project_path = os.path.abspath(project_path)
    fixed_project_path = os.path.join(os.path.dirname(project_path), 'fixed_' + os.path.basename(project_path))

    if not os.path.exists(project_path):
        print(f"❌ The path '{project_path}' does not exist.")
        return False

    # Copy entire project to the new "fixed" directory
    if os.path.exists(fixed_project_path):
        shutil.rmtree(fixed_project_path)
    shutil.copytree(project_path, fixed_project_path)

    print(f"\n🔧 Fixing project and saving results to: {fixed_project_path}")

    file_types = collect_relevant_files(fixed_project_path)

    # Process HTML, CSS, Python files
    for extension in ['.html', '.css', '.py']:
        for file in file_types[extension]:
            print(f"\n⚙️ Processing {extension.upper()} file: {file}")
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()

                # Always pass through AI
                fixed_code = fix_the_code(code)

                if fixed_code:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(fixed_code)
                    print(f"✅ Fixed: {file}")
                else:
                    print(f"❌ AI returned empty for: {file}")
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")

    # Process JS files the same way
    for file in file_types['.js']:
        print(f"\n⚙️ Processing JS file: {file}")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()

            # Always send JS through AI too
            fixed_code = fix_the_code(code)

            if fixed_code:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                print(f"✅ Fixed JS: {file}")
            else:
                print(f"❌ AI returned empty for: {file}")
        except Exception as e:
            print(f"❌ Error processing JS file {file}: {e}")

    print("\n🎉 All files have been processed and saved to:", fixed_project_path)
