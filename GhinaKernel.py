import json
import os
import sys
import string
import random
import time

# ==========================================
# CAMADA 0: CRIPTOGRAFIA (SEED 2026)
# ==========================================
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

# ==========================================
# CAMADA 1: VFS (SISTEMA DE ARQUIVOS)
# ==========================================
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
        else: print("[ERRO] setor inválido.")

    def gravar(self, nome, conteudo):
        if not nome.endswith(".es"): return "[ERRO] use .es"
        self._get_alvo()[nome] = {"tipo": "binario", "conteudo": self.sec.encriptar_texto(conteudo)}
        self.sync()
        return f"[MEMORIA] '{nome}' gravado."

    # Gravar Binário Puro (Vindo do Compilador)
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

# ==========================================
# CAMADA 2: CPU VIRTUAL (PROCESSADOR)
# ==========================================
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

# ==========================================
# CAMADA 3: KERNEL (SHELL)
# ==========================================
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

        if acao == "help":
            # Formatação limpa para o terminal
            print("\n=== GUINA PROTOCOL v3.1 (MANUAL) ===")
            print(" moldar [nome]      :: Cria setor (pasta)")
            print(" orbitar [nome]     :: Entra no setor")
            print(" orbitar voltar     :: Retorna um nível")
            print(" sonar              :: Escaneia setor atual")
            print(" gravar [nome.es]   :: Cria arquivo de texto seguro")
            print(" extrair [nome.es]  :: Lê arquivo de texto")
            print(" importar [arq.es]  :: Importa binário do Host")
            print(" executar [arq.es]  :: Processa binário na CPU")
            print(" pulverizar [alvo]  :: Deleta setor/arquivo")
            print(" computar           :: Inicia módulo matemático")
            print(" limpeza            :: Limpa o terminal")
            print(" derrubar           :: Desliga o sistema")
            print("========================================")

        elif acao == "sonar": self.vfs.sonar()
        
        elif acao == "moldar": 
            if param: 
                msg = self.vfs.moldar(param)
                if msg: print(msg)
            else: print("[ERRO] nome do setor ausente.")

        elif acao == "importar":
            if param and os.path.exists(param):
                try:
                    with open(param, 'r') as f:
                        dados = json.load(f)
                    self.vfs.importar_binario(param, dados)
                    print(f"[IO] binário '{param}' importado com sucesso.")
                except:
                    print("[ERRO] falha ao ler binário do host.")
            else:
                print("[ERRO] arquivo não encontrado no pc host.")

        elif acao == "executar":
            if param:
                bytecode = self.vfs.ler_binario(param)
                if bytecode:
                    self.cpu.executar(bytecode)
                else:
                    print("[ERRO] arquivo não é executável ou não existe.")
            else: print("[ERRO] qual arquivo?")

        # Comandos simples de deleção e navegação
        elif acao == "orbitar":
            if param: self.vfs.orbitar(param)
        
        elif acao == "pulverizar":
            if param: self.vfs.pulverizar(param)

        elif acao == "gravar":
            if param:
                print(f"[INPUT] Texto para '{param}':")
                conteudo = input("    > ")
                self.vfs.gravar(param, conteudo)

        elif acao == "extrair":
            if param:
                txt = self.vfs.extrair(param)
                if txt: print(f"\n>> CONTEÚDO: {txt}")

        elif acao == "limpeza":
             os.system('cls' if os.name == 'nt' else 'clear')
             
        elif acao == "derrubar":
            print("[SHUTDOWN] Desconectando...")
            sys.exit()

        else: print("[ERRO] comando desconhecido.")

# Permite rodar o Kernel sozinho sem o WebServer se quiser testar rápido
if __name__ == "__main__":
    k = GuinaKernel()
    print("--- GUINA OS TERMINAL MODE ---")
    while True:
        try:
            cmd = input("jonas.architect $ ")
            k.interpretar(cmd)
        except KeyboardInterrupt:
            break