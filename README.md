# 🌌 GuinaOS: Web-Based Encrypted Virtual Machine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Von_Neumann-orange?style=for-the-badge)

> **A conceptual Operating System and Virtual Machine written in pure Python, featuring a custom Instruction Set Architecture (ISA), encrypted Virtual File System (VFS), and a reactive WebCLI via WebSockets.**

GuinaOS is an educational/experimental project that simulates a complete (but minimal) computer system running inside the browser — with encryption at its core.

## ✨ Features

- Custom 8-bit-ish ISA with poetic mnemonics (materializar, duplicar, fundir, etc.)

- Deterministic XOR-based encryption using a fixed seed (2026) + shuffled ASCII table

- In-memory encrypted "hard disk" (guina_hd_proprietary.json)

- Web-based terminal with real-time command execution

- FastAPI + WebSockets backend

- No external dependencies beyond Python standard libs + FastAPI/uvicorn

## 🏗️ Architecture

The system uses a strict 4-layer isolation model for maximum separation between emulation, security and interface.

**Layer 0 – Security**  
Handles deterministic XOR encryption/decryption using fixed seed (2026) + shuffled 95-character ASCII table.

**Layer 1 – VFS (Virtual File System)**  
Manages the encrypted virtual disk (`guina_hd_proprietary.json`) with sector-based storage (directories as sectors + binary file blobs).

**Layer 2 – Virtual CPU**  
The execution engine: fetches encrypted bytes from VFS → decrypts opcodes on-the-fly → executes instructions in registers.

**Layer 3 – Kernel Shell**  
Command interpreter that understands high-level commands like `importar`, `executar`, `sonar`.

**Layer 4 – Web Bridge / Interface**  
FastAPI backend + WebSockets that connects the browser terminal to the kernel, streaming output in real-time.

Flow summary:  
User Browser ↔ WebSocket ↔ FastAPI (Layer 4) ↔ Kernel Shell (Layer 3) ↔ Virtual CPU (Layer 2) & VFS (Layer 1) ↔ Crypto Core (Layer 0)

🛠️ Installation & Quick Start
Prerequisites

Python 3.10+
pip

Steps

Clone the repositoryBashgit clone https://github.com/jonasguinami/GuinaOS.git
/cd GuinaOS

Install dependencies
Bash/ pip install fastapi uvicorn

Start the server
Bash/ python -m uvicorn server:app --reload

Open in browser http://localhost:8000
or
Open index.html directly (if you prefer static serving)


💻 Ghinamys – The Proprietary Language
GuinaOS executes Ghinamys programs (.ghina source → .es encrypted binary).
Typical Workflow

# 1. Bash/ Write your program
examples/protocolo.ghina

# 2. Compile to encrypted binary
python CompilerGhina.py protocolo.ghina

🔮 Roadmap

 -Core Kernel & VFS
 -Virtual CPU
 -WebSocket-based WebCLI
 -Multi-threading / concurrent processes
 -Graphical mode (Canvas API integration)
 -Network stack (P2P encrypted chat)
 -Better error reporting & debugging tools

👨‍💻 Author

Jonas Guinami

-Architect & AI Researcher
GitHub: @jonasguinami
Feel free to open issues, fork it, or just play around in the terminal.
Any feedback is super welcome! 🚀
