# GuinaOS

# 🌌 GuinaOS: Web-Based Encrypted Virtual Machine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?style=for-the-badge&logo=fastapi)
![Architecture](https://img.shields.io/badge/Architecture-Von_Neumann-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **A conceptual Operating System and Virtual Machine implemented in Python, featuring a proprietary Instruction Set Architecture (ISA), encrypted Virtual File System (VFS), and a reactive WebCLI via WebSockets.**

---

## 🧠 Project Overview

**GuinaOS** is an engineering exploration into low-level computing concepts within a high-level environment. It simulates a complete computer architecture—from the CPU cycle (Fetch-Decode-Execute) to memory management—encapsulated within a modern Glassmorphism Web Interface.

Unlike standard terminals, GuinaOS operates on **Encrypted Bytecode**. Programs must be written in the proprietary assembly language (**Ghinamys**), compiled into an encrypted binary format (`.es`), and executed by the virtual CPU, which performs runtime decryption.

### 🚀 Key Features

* **Virtual CPU Core:** Implements a custom ALU (Arithmetic Logic Unit) with registers (`REG_A`, `REG_B`, `IP`) and a simulated clock cycle.
* **Proprietary ISA (Ghinamys):** A custom assembly language designed for this architecture (e.g., `moldar`, `fundir`, `projetar`).
* **Encrypted VFS:** A JSON-based file system where all data is obfuscated using a seed-based XOR cipher. The host machine cannot read the files without the Kernel.
* **Web-Based Kernel Shell:** A real-time terminal interface built with **FastAPI** and **WebSockets**, featuring a responsive Cyberpunk/Glassmorphism UI.
* **Hardware Simulation:** Simulates sensor inputs and processing latency.

---

## 🏗️ Architecture

The system is built on a 4-Layer Architecture:

```mermaid
graph TD
    A[User (Browser)] <-->|WebSocket| B[Layer 4: Web Bridge (Server.py)];
    B <--> C[Layer 3: Kernel Shell];
    C <--> D[Layer 2: Virtual CPU];
    C <--> E[Layer 1: Virtual File System (VFS)];
    D <--> F[Layer 0: Security & Crypto Core];
    E <--> F;
Layer 0 (Security): Handles XOR encryption/decryption using a deterministic seed (2026) and a shuffled 95-character ASCII table.Layer 1 (VFS): Manages the guina_hd_proprietary.json disk, handling sector creation (directories) and binary storage.Layer 2 (CPU): The logic brain. Reads encrypted bytes, decrypts opcodes on-the-fly, and executes instructions.Layer 3 (Kernel): The command interpreter (import, executar, sonar).Layer 4 (Interface): The FastAPI adapter that streams stdout to the HTML frontend.🛠️ Installation & UsagePrerequisitesPython 3.8+pip1. Clone & InstallBashgit clone [https://github.com/jonasguinami/GuinaOS.git](https://github.com/jonasguinami/GuinaOS.git)
cd GuinaOS
pip install fastapi uvicorn
2. Run the SystemStart the WebSocket Server:Bashpython -m uvicorn server:app --reload
Open index.html in your browser or navigate to http://localhost:8000.💻 The "Ghinamys" LanguageGuinaOS cannot run Python or C. It runs Ghinamys, a language designed for this VM.WorkflowWrite Code: Create a .ghina file (e.g., logic.ghina).Compile: Use the compiler to generate an encrypted binary (.es).Bashpython CompilerGhina_v4.py logic.ghina
Import: In the Web Terminal, import the binary from the host.Bashjonas.architect:~ $ importar binario_seguro.es
Execute: Run it on the Virtual CPU.Bashjonas.architect:~ $ executar binario_seguro.es
Instruction Set Reference (v1.1 Stable)MnemonicHexDescriptionModern Equivalencematerializar <val>0x10Loads value into REG_AMOV EAX, valduplicar0x11Copies REG_A to REG_BMOV EBX, EAXfundir0x20Adds REG_B to REG_AADD EAX, EBXdrenar0x21Subtracts REG_B from REG_ASUB EAX, EBXcaptar0x50Reads input from sensorSTDIN / SCANFprojetar0x60Prints REG_A to consoleSTDOUT / PRINTencerrar0xFFHalts the CPU cycleHALT / EXIT📸 Screenshots(Add a screenshot of your Glassmorphism terminal here)🔮 Roadmap[x] Core Kernel & VFS[x] Virtual CPU Integration[x] WebSocket WebCLI[ ] Multi-threading support[ ] Graphical Mode (Canvas API integration)[ ] Network Module (Peer-to-Peer encrypted chat)Author: Jonas GuinamiArchitect & AI Researcher
---

### Dica para a Imagem (Screenshot):
Tire um print da sua tela com o terminal rodando o comando `executar binario_seguro.es` e o output colorido. Salve como `screenshot.png` na pasta do projeto e o GitHub vai renderizar automaticamente onde coloquei o placeholder.

**Esse README transforma seu projeto de "um script python" para "uma arquitetura d
