"""
Local entry point for AELM (no Hugging Face required)
"""

from config import APP_NAME, VERSION, MODEL
from cli import run

def banner():
    print("=" * 60)
    print(f"{APP_NAME} v{VERSION}")
    print("Advanced Employment & Labor Model")
    print("Mode : Local Terminal")
    print(f"Default Model Setting: {MODEL}")
    print("=" * 60)
    print("No API keys required.\n")

def main():
    banner()
    run()

if __name__ == "__main__":
    main()
