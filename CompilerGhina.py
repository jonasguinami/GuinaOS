import sys
import json
import string
import random

# MÓDULO DE SEGURANÇA
class GuinaSecurity:
    def __init__(self):
        self.CHAVE_MESTRA = 0xB7
        self.charset_padrao = string.printable[:95]
        random.seed(2026) 
        vals = list(range(10, 10 + len(self.charset_padrao)))
        random.shuffle(vals)
        self.char_map = dict(zip(self.charset_padrao, vals))

    def encriptar_byte(self, val):
        # [CORREÇÃO CRÍTICA]: Era % 255, agora é % 256.
        # Isso impede que o comando 0xFF (255) vire 0x00.
        return (val % 256) ^ self.CHAVE_MESTRA

INSTRUCTION_SET = {
    "materializar": 0x10,
    "duplicar":     0x11,
    "fundir":       0x20,
    "drenar":       0x21,
    "captar":       0x50,
    "projetar":     0x60,
    "encerrar":     0xFF
}

def compilar(arquivo_fonte):
    sec = GuinaSecurity()
    bytecode = []
    
    try:
        with open(arquivo_fonte, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("[ERRO] arquivo não encontrado.")
        return

    print(f"--- compilação hotfix v1.1: {arquivo_fonte} ---")
    
    for i, linha in enumerate(linhas, 1):
        parte = linha.split(';')[0].strip()
        if not parte: continue
        
        tokens = parte.split()
        cmd = tokens[0].lower()
        
        if cmd in INSTRUCTION_SET:
            op = INSTRUCTION_SET[cmd]
            bytecode.append(sec.encriptar_byte(op))
            
            if len(tokens) > 1:
                try:
                    val = int(tokens[1])
                    bytecode.append(sec.encriptar_byte(val))
                except:
                    print(f"[ERRO] valor inválido na linha {i}")
                    return
        else:
            print(f"[ERRO] comando desconhecido '{cmd}' na linha {i}")
            return

    nome_saida = "binario_seguro.es"
    with open(nome_saida, "w") as out:
        json.dump(bytecode, out)
    
    print(f"--- binário corrigido: '{nome_saida}' gerado. ---")

if __name__ == "__main__":
    if len(sys.argv) < 2: print("uso: python CompilerGhina_v4_Hotfix.py <arquivo.ghina>")
    else: compilar(sys.argv[1])