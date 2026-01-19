# 🌌 GuinaOS: Web-Based Encrypted Virtual Machine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=for-the-badge&logo=fastapi)
![Architecture](https://img.shields.io/badge/Architecture-Von_Neumann-orange?style=for-the-badge)

> **A conceptual Operating System and Virtual Machine implemented in Python, featuring a proprietary Instruction Set Architecture (ISA), encrypted Virtual File System (VFS), and a reactive WebCLI via WebSockets.**

---

## 🏗️ Architecture

The system is built on a structured 4-Layer Architecture to ensure isolation between hardware emulation and user interface.

```mermaid
graph TD
    User([User Browser]) -- WebSocket --- Server[Layer 4: Web Bridge]
    Server --- Kernel[Layer 3: Kernel Shell]
    Kernel --- CPU[Layer 2: Virtual CPU]
    Kernel --- VFS[Layer 1: Virtual File System]
    CPU --- Security[Layer 0: Crypto Core]
    VFS --- Security
    
    style User fill:#00f3ff,stroke:#333,color:#000
    style Security fill:#bc13fe,stroke:#333,color:#fff

Layer Breakdown
Layer 0 (Security): Handles XOR encryption/decryption using a deterministic seed (2026) and a shuffled 95-character ASCII table.

Layer 1 (VFS): Manages the guina_hd_proprietary.json disk, handling sector creation (directories) and binary storage.

Layer 2 (CPU): The logic brain. Reads encrypted bytes, decrypts opcodes on-the-fly, and executes instructions.

Layer 3 (Kernel): The command interpreter (importar, executar, sonar).

Layer 4 (Interface): The FastAPI adapter that streams stdout to the HTML frontend.

🛠️ Installation & Usage
Prerequisites
Python 3.8+

pip

1. Clone & Install

git clone https://github.com/jonasguinami/GuinaOS.git
cd GuinaOS
pip install fastapi uvicorn

2. Run the System
Start the WebSocket Server:

python -m uvicorn server:app --reload

Open index.html in your browser or navigate to http://localhost:8000.

💻 The "Ghinamys" Language
GuinaOS runs Ghinamys, a proprietary language designed for this VM.

Workflow
Write Code: Create a .ghina file.

Compile: Generate an encrypted binary (.es).

python CompilerGhina_v4.py logic.ghina

Import & Execute: In the Web Terminal:

jonas.architect:~ $ importar binario_seguro.es
jonas.architect:~ $ executar binario_seguro.es

Instruction Set Reference (v1.1 Stable)

Mnemonic,Hex,Description,Modern Equivalence
materializar,0x10,Loads value into REG_A,"MOV EAX, val"
duplicar,0x11,Copies REG_A to REG_B,"MOV EBX, EAX"
fundir,0x20,Adds REG_B to REG_A,"ADD EAX, EBX"
drenar,0x21,Subtracts REG_B from REG_A,"SUB EAX, EBX"
captar,0x50,Reads input from sensor,STDIN / SCANF
projetar,0x60,Prints REG_A to console,STDOUT / PRINT
encerrar,0xFF,Halts the CPU cycle,HALT / EXIT

🔮 Roadmap

[x] Core Kernel & VFS

[x] Virtual CPU Integration

[x] WebSocket WebCLI

[ ] Multi-threading support

[ ] Graphical Mode (Canvas API integration)

[ ] Network Module (Peer-to-Peer encrypted chat)


Author: Jonas Guinami

Architect & AI Researcher

