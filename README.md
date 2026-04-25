# 🚀  AI - JS Recon Tool

A powerful **AI-assisted JavaScript reconnaissance CLI tool** designed for bug hunters and security researchers.  
It fetches JavaScript files, analyzes them from an attacker’s perspective, and generates structured security reports using AI.

---

## 🔍 About the Tool

JS Recon helps you:

- 🕵️ Discover hidden or undocumented API endpoints  
- 🔑 Detect hardcoded secrets, API keys, and tokens  
- 🛡️ Analyze authentication & authorization logic  
- ⚠️ Identify potential vulnerabilities (XSS, IDOR, CSRF, SSRF, etc.)  
- 🧠 Understand business logic flows and client-side validations  
- 📊 Generate clean, structured Markdown reports  

All results are beautifully rendered in the terminal using **Rich** and saved locally for later use.

---

## ⚙️ How It Works

1. 📥 Accepts a JavaScript URL or list of URLs  
2. 🌐 Fetches JavaScript content safely  
3. ✂️ Trims large files for efficient processing  
4. 🤖 Sends code to OpenAI API for analysis  
5. 📑 Receives structured Markdown report  
6. 🎨 Displays colorful output in terminal 
---

## 🧰 Installation

### 📌 1. Clone the Repository

```bash
git clone https://github.com/nithin644/js-recon.git
cd js-recon
pip3 install -r requirements.txt
 Set OpenAI API Key
python3 js-recon.py -u https://example.com/app.js
```

## 🧾 Report Structure

Each report contains:

- 📊 **Summary**
- 🖧 **Endpoints Discovered**
- 🔑 **Secrets & Keys**
- 🛡️ **Auth & Logic Analysis**
- ⚠️ **Potential Vulnerabilities**
- 📝 **Interesting Notes**

## Demo 
<video src="https://github.com/user-attachments/assets/46fb8c9d-691c-4a17-bd15-0825b1273054" controls width="600"></video>
