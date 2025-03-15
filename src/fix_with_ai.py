import requests

# Read API key securely from a file
with open('../api keys/groq.txt', 'r') as f:
    api_key = f.read().strip()

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def clean_code_block(code_text):
    """Remove triple backticks and language hints like ```python."""
    lines = code_text.strip().splitlines()
    # Remove ```python or ``` from first line
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    # Remove ending ``` if present
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()

def fix_the_code(code, instructions):
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

# 🔍 Example usage
bad_code = """
def add(a, b)
    return a + b
"""

instructions = ("Fix the syntax errors and make sure the function returns the sum correctly. "
                "Don't give any explanations, just give clean formatted code, no comments, no extra text.")

fixed_code = fix_the_code(bad_code, instructions)

if fixed_code:
    print("\n✅ Fixed Code:\n")
    print(fixed_code)
