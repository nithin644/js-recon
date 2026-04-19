#!/usr/bin/env python3

import argparse
import requests
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme

custom_theme = Theme({
    "markdown.h1": "bold magenta",
    "markdown.h2": "bold cyan",
    "markdown.h3": "bold yellow",
    "markdown.text": "bright_white",
    "markdown.item.bullet": "bold bright_yellow",
    "markdown.strong": "bold bright_green",
    "markdown.emph": "italic bright_cyan",
    "markdown.code": "cyan on bright_black",
    "markdown.block_quote": "bold bright_red"
})

console = Console(theme=custom_theme)

API_KEY = "<Replace with UR API Key>"
API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

PROMPT_TEMPLATE = """
You are an expert security researcher and bug hunter.
Your task is to analyze the following JavaScript code from an Attacker's perspective.
URL: {url}

Focus on finding:
1. Hidden API endpoints (undocumented or sensitive)
2. Hardcoded secrets, API keys, tokens, or credentials
3. Authentication and Authorization flaws
4. Business logic vulnerabilities
5. Interesting feature flags or developer comments
6. Client-side vulnerabilities like DOM XSS, etc.

Analyze the code thoroughly. Provide your output in a professional MARKDOWN format.
Use emojis for section headers and assign a severity rating (🔴 High, 🟡 Medium, 🟢 Low, ⚪ Info) to findings.

Use this exactly structured MARKDOWN format:

# 🕵️‍♂️ JavaScript Reconnaissance Report

## 📊 Summary
(Brief overview of what the file does and overall risk level with an emoji)

## 🖧 Endpoints Discovered
- **[Method] /path/to/endpoint** - (Note if interesting/private) - **Severity: ⚪ Info**

## 🔑 Secrets & Keys
- **Potential Secret** - (Description and reasoning) - **Severity: 🔴 High**
(If none, say "✅ No Secrets found")

## 🛡️ Auth & Logic Analysis
(Analyze auth flows, roles, or business logic quirks) - **Severity: 🟡 Medium**

## ⚠️ Potential Vulnerabilities
> **[Vulnerability Type]** - (Specific security risks with reasoning) - **Severity: 🔴 High**
(CRITICAL: For High severity findings, you MUST start the line with a blockquote `>` so it highlights correctly!)

## 📝 Interesting Notes
(Any other findings, developer comments, tech stack details)

JavaScript Code:
"""

def fetch_js(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        console.print(f"[red]Error fetching {url}: {e}[/red]")
        return None

def analyze_js(url, js_code):
    prompt = PROMPT_TEMPLATE.format(url=url) + "\n" + js_code[:20000]

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "stream": False
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        console.print(f"[red]API Error: {e}[/red]")
        return None

def process_url(url):
    console.print(f"\n[bold cyan]✨ Analyzing:[/bold cyan] [underline]{url}[/underline]")
    js = fetch_js(url)
    if not js:
        return

    result = analyze_js(url, js)
    if result:
        console.print("\n")
        console.print(Panel(Markdown(result), title="[bold green]Report Generated[/bold green]", border_style="cyan"))
        console.print("\n")

def main():
    parser = argparse.ArgumentParser(description="JavaScript Recon Tool (AI Powered)")
    parser.add_argument("-u", "--url", help="Single JS URL")
    parser.add_argument("-f", "--file", help="File containing JS URLs")
    args = parser.parse_args()

    if not args.url and not args.file:
        parser.print_help()
        sys.exit(1)

    if args.url:
        process_url(args.url)

    if args.file:
        try:
            with open(args.file, "r") as f:
                urls = [line.strip() for line in f if line.strip()]
            for url in urls:
                process_url(url)
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")

if __name__ == "__main__":
    main()