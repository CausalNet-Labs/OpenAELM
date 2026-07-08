"""
==============================================================================
aelm.py
Advanced Employment & Labor Model (AELM)
Main Application
==============================================================================
"""

import sys
import requests

from config import *
from system_prompt import SYSTEM_PROMPT

conversation_history = []
hf_token = None

HELP_TEXT = """
================ AELM =================

help           Show commands
clear          Clear conversation memory
config         Show configuration
version        Show version
resume         Resume mode
job            Job mode
analyze        Full analysis
rewrite        Rewrite resume
ats            ATS analysis
coverletter    Cover letter
interview      Interview mode
dashboard      Strategic dashboard
export         Export results
exit           Quit

=======================================
"""

def get_token():
    token = input("Hugging Face API Token: ").strip()
    if not token:
        print("API token required.")
        sys.exit(1)
    return token

def build_messages():
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.extend(conversation_history[-MAX_HISTORY:])
    return msgs

def call_model(user_text):
    conversation_history.append({"role":"user","content":user_text})

    payload = {
        "model": MODEL,
        "messages": build_messages(),
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=TIMEOUT
        )
        r.raise_for_status()
        data = r.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        conversation_history.pop()
        return f"[ERROR] {e}"

    conversation_history.append(
        {"role":"assistant","content":reply}
    )

    return reply

def clear():
    conversation_history.clear()
    print("[Memory Cleared]\n")

def show_config():
    print(f"""
Application : {APP_NAME}
Version     : {VERSION}
Model       : {MODEL}
Temperature : {TEMPERATURE}
Max Tokens  : {MAX_TOKENS}
History     : {MAX_HISTORY}
""")

def command(cmd):
    c = cmd.lower()

    if c == "help":
        print(HELP_TEXT)
        return True

    if c == "clear":
        clear()
        return True

    if c == "config":
        show_config()
        return True

    if c == "version":
        print(VERSION)
        return True

    if c == "exit":
        print("Goodbye.")
        sys.exit(0)

    return False

def main():
    global hf_token

    print(BANNER)

    hf_token = get_token()

    print("\nAELM Ready.\n")

    while True:

        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user:
            continue

        if command(user):
            continue

        print("\nAELM\n------------------------------")
        print(call_model(user))
        print()

if __name__ == "__main__":
    main()
