import json
import os
import sys
import string
import random
import time
import psutil

# CAMADA 0: CRIPTOGRAFIA 

class GuinaSecurity:
    def __init__(self):
        self.CHAVE_MESTRA = 0xB7
        self.charset_padrao = string.printable[:95] 
        random.seed(2026) 
        vals = list(range(10, 10 + len(self.charset_padrao)))
        random.shuffle(vals)
        self.char_map = dict(zip(self.charset_padrao, vals))
        self.reverse_map = {v: k for k, v in self.char_map.items()}

    def encriptar_texto(self, texto):
        buffer = []
        for char in texto:
            val = self.char_map.get(char, 63) # 63 = '?'
            buffer.append(val ^ self.CHAVE_MESTRA)
        return buffer

    def decriptar_texto(self, buffer_bytes):
        texto = ""
        for b in buffer_bytes:
            val_base = b ^ self.CHAVE_MESTRA
            texto += self.reverse_map.get(val_base, '?')
        return texto

    # Criptografia de Bytes Brutos (CPU)
    def encriptar_byte(self, val):
        return (val % 256) ^ self.CHAVE_MESTRA

    def decriptar_byte(self, val_encriptado):
        return (val_encriptado ^ self.CHAVE_MESTRA)


# CAMADA 1: VFS (SISTEMA DE ARQUIVOS)


class GuinaVFS:
    def __init__(self, sec):
        self.disk_file = "guina_hd_proprietary.json"
        self.sec = sec
        self.current_path = [] 
        self.file_system = self.mount()

    def mount(self):
        if os.path.exists(self.disk_file):
            try:
                with open(self.disk_file, 'r') as f: return json.load(f)
            except: pass
        return {"NUCLEO": {"tipo": "setor", "dados": {}}}

    def sync(self):
        with open(self.disk_file, 'w') as f: json.dump(self.file_system, f, indent=4)

    def _get_alvo(self):
        nav = self.file_system["NUCLEO"]["dados"]
        for p in self.current_path: nav = nav[p]["dados"]
        return nav

    def moldar(self, nome): 
        alvo = self._get_alvo()
        if nome not in alvo:
            alvo[nome] = {"tipo": "setor", "dados": {}}
            self.sync()
            return f"[ESTRUTURA] setor '{nome}' moldado."
        return "[ERRO] setor já existe."

    def orbitar(self, nome):
        if nome == "voltar":
            if self.current_path: self.current_path.pop()
            return
        alvo = self._get_alvo()
        if nome in alvo and alvo[nome]["tipo"] == "setor":
            self.current_path.append(nome)
        else: print(f"[ERRO] '{nome}' não é um setor válido.")

    def pulverizar(self, nome):
        alvo = self._get_alvo()
        if nome in alvo:
            del alvo[nome]
            self.sync()
            print(f"[DESTRUIÇÃO] '{nome}' foi pulverizado.")
        else: print(f"[ERRO] alvo '{nome}' não encontrado.")

    def gravar(self, nome, conteudo):
        if not nome.endswith(".es"): return "[ERRO] use .es"
        # Grava como BINARIO (Texto criptografado)
        self._get_alvo()[nome] = {"tipo": "binario", "conteudo": self.sec.encriptar_texto(conteudo)}
        self.sync()
        return f"[MEMORIA] '{nome}' gravado."

    def extrair(self, nome):
        alvo = self._get_alvo()
        if nome in alvo:
            if alvo[nome]["tipo"] == "binario":
                return self.sec.decriptar_texto(alvo[nome]["conteudo"])
            else:
                return "[ERRO] este arquivo é um executável ou setor, não pode ser extraído como texto."
        return "[ERRO] arquivo não encontrado."

    def importar_binario(self, nome, lista_bytes):
        self._get_alvo()[nome] = {"tipo": "executavel", "conteudo": lista_bytes}
        self.sync()

    def ler_binario(self, nome):
        alvo = self._get_alvo()
        if nome in alvo and alvo[nome]["tipo"] == "executavel":
            return alvo[nome]["conteudo"]
        return None

    def sonar(self):
        alvo = self._get_alvo()
        path_str = " / ".join(self.current_path) if self.current_path else "RAIZ"
        print(f"\n--- SONAR ATIVO: [{path_str}] ---")
        if not alvo: print("   (vazio)")
        for k, v in alvo.items():
            t = "[SETOR]" if v["tipo"] == "setor" else f"[{v['tipo'].upper()}]"
            print(f"   {t:<12} {k}")

# CAMADA 2: CPU VIRTUAL (PROCESSADOR)

class GuinaCPU:
    def __init__(self, security):
        self.sec = security
        self.reg = {"a": 0, "b": 0, "ip": 0}
        self.running_process = False

    def executar(self, bytecode_encriptado):
        self.reg = {"a": 0, "b": 0, "ip": 0} 
        self.running_process = True
        
        print(f"[CPU] Processo iniciado. {len(bytecode_encriptado)} bytes carregados.")
        
        while self.running_process and self.reg["ip"] < len(bytecode_encriptado):
            # 1. FETCH
            byte_sujo = bytecode_encriptado[self.reg["ip"]]
            opcode = self.sec.decriptar_byte(byte_sujo)
            self.reg["ip"] += 1

            # 2. DECODE & EXECUTE
            if opcode == 0x10: # materializar
                val_sujo = bytecode_encriptado[self.reg["ip"]]
                val = self.sec.decriptar_byte(val_sujo)
                self.reg["ip"] += 1
                self.reg["a"] = val

            elif opcode == 0x11: # duplicar
                self.reg["b"] = self.reg["a"]

            elif opcode == 0x20: # fundir
                self.reg["a"] += self.reg["b"]

            elif opcode == 0x21: # drenar
                self.reg["a"] -= self.reg["b"]

            elif opcode == 0x50: # captar
                # Simula sensor para não travar WebSocket
                sensor_val = random.randint(1, 100)
                print(f">> [SENSOR] dado captado do ambiente: {sensor_val}")
                self.reg["a"] = sensor_val

            elif opcode == 0x60: # projetar
                print(f">> [PROJEÇÃO HOLOGRÁFICA] VALOR FINAL :: {self.reg['a']}")

            elif opcode == 0xFF: # encerrar
                self.running_process = False
                print("[CPU] Ciclo encerrado com sucesso.")
            
            else:
                print(f"[CPU PANIC] Instrução corrompida: {hex(opcode)}")
                self.running_process = False

# CAMADA 3: KERNEL (SHELL)

class GuinaKernel:
    def __init__(self):
        self.sec = GuinaSecurity()
        self.vfs = GuinaVFS(self.sec)
        self.cpu = GuinaCPU(self.sec)
        self.user = "jonas.architect"

    def interpretar(self, cmd_str):
        partes = cmd_str.split(" ", 1)
        acao = partes[0].lower()
        param = partes[1] if len(partes) > 1 else None

        # SISTEMA E AJUDA 
        
        if acao == "help":
            print("\n=== GUINA PROTOCOL v3.3 (OFFICIAL MANUAL) ===")
            print(" [ESTRUTURA] ")
            print("  moldar [nome]      :: Cria setor (pasta)")
            print("  orbitar [nome]     :: Entra no setor (use 'voltar' para subir)")
            print("  sonar              :: Escaneia o setor atual")
            print("  pulverizar [alvo]  :: Deleta permanentemente o alvo")
            print("")
            print(" [DADOS & ARQUIVOS] ")
            print("  gravar [nome.es]   :: Inicia fluxo de escrita (envie o texto após o comando)")
            print("  extrair [nome.es]  :: Decripta e lê conteúdo de texto")
            print("  importar [arq.es]  :: Traz binário do Host para o VFS")
            print("  executar [arq.es]  :: Roda binário na CPU Virtual")
            print("")
            print(" [SISTEMA & UTILITÁRIOS] ")
            print("  computar           :: Ativa Math Core (digite 'fim' para sair)")
            print("  status             :: Monitora CPU/RAM real do Host")
            print("  limpeza            :: Limpa o buffer do terminal")
            print("  derrubar           :: Encerra o Kernel")
            print("==============================================")

        elif acao == "limpeza":
            os.system('cls' if os.name == 'nt' else 'clear')

        elif acao == "derrubar":
            print("[SHUTDOWN] Desconectando...")
            sys.exit()

        if acao == "status":
            cpu_uso = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            disco = psutil.disk_usage('/')
            
            print("\n=== MONITORAMENTO DE HARDWARE (HOST) ===")
            print(f" CPU CORE      :: [{cpu_uso}%] " + ("█" * int(cpu_uso/10)))
            print(f" MEMÓRIA RAM   :: {ram.percent}% ({ram.used // 1024**2}MB / {ram.total // 1024**2}MB)")
            print(f" DISCO VFS     :: {disco.percent}% ocupado")
            print(f" STATUS NÚCLEO :: OPERACIONAL (ESTÁVEL)")
            print("========================================\n")

        # MANUTENÇÃO DO EXTRAIR
        elif acao == "extrair":
            if param:
                txt = self.vfs.extrair(param)
                if txt: 
                    # Se for erro, o VFS retorna uma string começando com [ERRO]
                    print(f"\n>> CONTEÚDO EXTRAÍDO:\n{txt}\n")
            else: 
                print("[ERRO] informe o nome do arquivo para extração.")

        # NAVEGAÇÃO E EXPLORAÇÃO
        elif acao == "sonar": 
            self.vfs.sonar()

        elif acao == "moldar": 
            if param: print(self.vfs.moldar(param))
            else: print("[ERRO] nome do setor ausente.")

        elif acao == "orbitar":
            if param: self.vfs.orbitar(param)
            else: print("[ERRO] setor alvo necessário.")

        # MANIPULAÇÃO DE DADOS
        elif acao == "gravar":
            # Apenas avisa o server.py
            if param:
                pass # O servidor intercepta 
            else: 
                print("[ERRO] informe o nome do arquivo.")

        elif acao == "extrair":
            if param:
                txt = self.vfs.extrair(param)
                if txt: print(f"\n>> CONTEÚDO EXTRAÍDO:\n{txt}")
            else: 
                print("[ERRO] qual arquivo deseja extrair?")

        elif acao == "pulverizar":
            if param: self.vfs.pulverizar(param)
            else: print("[ERRO] o que você deseja pulverizar?")

        # EXECUÇÃO E BINÁRIOS
        elif acao == "importar":
            if param and os.path.exists(param):
                with open(param, 'r') as f:
                    dados = json.load(f)
                self.vfs.importar_binario(param, dados)
                print(f"[IO] binário '{param}' importado.")
            else: print("[ERRO] arquivo host não encontrado.")

        elif acao == "executar":
            if param:
                bytecode = self.vfs.ler_binario(param)
                if bytecode: self.cpu.executar(bytecode)
                else: print("[ERRO] executável não encontrado.")
            else: print("[ERRO] qual arquivo?")

        elif acao == "computar":
            # O servidor intercepta esse comando e entra no modo matemático
            print("[SISTEMA] Alternando para modo de processamento matemático...")

        else: 
            print(f"[ERRO] comando '{acao}' desconhecido. digite 'help'.")

# Roda o Kernel sozinho sem o WebServer
if __name__ == "__main__":
    k = GuinaKernel()
    print("--- GUINA OS TERMINAL MODE ---")
    while True:
        try:
            cmd = input("jonas.architect $ ")
            k.interpretar(cmd)
        except KeyboardInterrupt:

            break
