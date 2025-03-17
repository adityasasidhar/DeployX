import os
import requests
import json

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
