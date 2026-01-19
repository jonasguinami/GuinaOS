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

4-layer isolation model:

```mermaid
graph TD
    User([User Browser]) -- WebSocket --- Server[Layer 4: Web Bridge<br>FastAPI + WebSockets]
    Server --- Kernel[Layer 3: Kernel Shell<br>Command interpreter]
    Kernel --- CPU[Layer 2: Virtual CPU<br>Opcode fetch & execute]
    Kernel --- VFS[Layer 1: Virtual File System<br>Encrypted sectors]
    CPU --- Security[Layer 0: Crypto Core<br>XOR + shuffled charset]
    VFS --- Security

    style User fill:#00f3ff,stroke:#333,color:#000
    style Security fill:#bc13fe,stroke:#333,color:#fff

Layer Breakdown

Layer 0 – Security
Handles deterministic encryption/decryption (fixed seed 2026 + shuffled 95-char ASCII table)
Layer 1 – VFS
Manages the virtual disk (guina_hd_proprietary.json) with sector-based storage (directories + binary blobs)
Layer 2 – CPU
Fetches encrypted bytes → decrypts opcodes on-the-fly → executes instructions
Layer 3 – Kernel
Command interpreter (importar, executar, sonar, etc.)
Layer 4 – Interface
FastAPI server that bridges WebSocket → HTML5 terminal

🛠️ Installation & Quick Start
Prerequisites

Python 3.10+
pip

Steps

Clone the repositoryBashgit clone https://github.com/jonasguinami/GuinaOS.git
cd GuinaOS
Install dependenciesBashpip install fastapi uvicorn
Start the serverBashpython -m uvicorn server:app --reload
Open in browser
http://localhost:8000
or
Open index.html directly (if you prefer static serving)


💻 Ghinamys – The Proprietary Language
GuinaOS executes Ghinamys programs (.ghina source → .es encrypted binary).
Typical Workflow
Bash# 1. Write your program
#    examples/logic.ghina

# 2. Compile to encrypted binary
python CompilerGhina_v4.py logic.ghina

# 3. Use the WebCLI:
jonas.architect:~ $ importar binario_seguro.es
jonas.architect:~ $ executar binario_seguro.es
Instruction Set (v1.1 – Stable)

MnemonicHexDescriptionModern Equivalentmaterializar0x10Load value into REG_AMOV EAX, valduplicar0x11Copy REG_A → REG_BMOV EBX, EAXfundir0x20Add REG_B to REG_AADD EAX, EBXdrenar0x21Subtract REG_B from REG_ASUB EAX, EBXcaptar0x50Read from sensor / inputSTDIN / SCANFprojetar0x60Print REG_A to consoleSTDOUT / PRINTencerrar0xFFHalt CPU executionHALT / EXIT
(More instructions planned for future versions)
🔮 Roadmap

 Core Kernel & VFS
 Virtual CPU
 WebSocket-based WebCLI
 Multi-threading / concurrent processes
 Graphical mode (Canvas API integration)
 Network stack (P2P encrypted chat)
 Better error reporting & debugging tools

👨‍💻 Author
Jonas Guinami
Architect & AI Researcher
GitHub: @jonasguinami
Feel free to open issues, fork it, or just play around in the terminal.
Any feedback is super welcome! 🚀
