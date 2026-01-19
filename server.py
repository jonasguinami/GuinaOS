from fastapi import FastAPI, WebSocket
from GhinaKernel import GuinaKernel
import sys
import io

app = FastAPI()

# --- ADAPTADOR WEB PARA O KERNEL ---
# Precisamos capturar o 'print' do Kernel e mandar pro navegador
class WebKernel(GuinaKernel):
    def __init__(self):
        super().__init__()
        self.output_buffer = []

    # Sobrescrevemos o boot para não limpar a tela do servidor real
    def boot(self):
        return "--- SISTEMA INICIADO VIA WEB-LINK ---"

    # Método personalizado para processar e capturar a resposta
    def processar_comando_web(self, comando):
        # 1. Redireciona o stdout (print) para nossa variável
        capture = io.StringIO()
        sys.stdout = capture
        
        # 2. Executa o comando do seu Kernel original
        try:
            self.interpretar(comando)
        except SystemExit:
            print("[SISTEMA] Conexão encerrada pelo usuário.")
        except Exception as e:
            print(f"[ERRO CRÍTICO] {str(e)}")

        # 3. Restaura o stdout e pega o texto
        sys.stdout = sys.__stdout__
        output = capture.getvalue()
        return output

# Instância global do Kernel
sistema = WebKernel()

# No server.py, altere o loop principal:

estado = {"escrita": False, "arquivo": "", "math": False}

@app.websocket("/neuro-link")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(">>> NEURO-LINK: ESTABELECIDO")
    
    while True:
        try:
            data = await websocket.receive_text()
            cmd = data.strip()

            # MODO ESCRITA (GRAVAR)
            if estado["escrita"]:
                sistema.vfs.gravar(estado["arquivo"], cmd)
                estado["escrita"] = False
                await websocket.send_text(f"[MEMORIA] Dados inscritos em '{estado['arquivo']}'.")
                continue

            # MODO MATEMÁTICO (COMPUTAR)
            if estado["math"]:
                if cmd.lower() == "fim":
                    estado["math"] = False
                    await websocket.send_text("[MATH] Módulo encerrado.")
                else:
                    try:
                        # O eval() faz a conta
                        resultado = eval(cmd)
                        await websocket.send_text(f"   = {resultado}")
                    except:
                        await websocket.send_text("   [ERRO] Cálculo inválido.")
                continue

            # ATIVAÇÃO DE MODOS
            if cmd.startswith("gravar "):
                estado["escrita"] = True
                estado["arquivo"] = cmd.split(" ", 1)[1]
                await websocket.send_text(f"[KERNEL] Aguardando dados para '{estado['arquivo']}'...")
                continue
            
            if cmd == "computar":
                estado["math"] = True
                await websocket.send_text("[MATH CORE] Iniciado. Digite a conta ou 'fim' para sair.")
                continue

            # COMANDOS NORMAIS (CAPTURA STDOUT)
            capture = io.StringIO()
            sys.stdout = capture
            sistema.interpretar(cmd)
            sys.stdout = sys.__stdout__
            await websocket.send_text(capture.getvalue() or f"Comando '{cmd}' executado.")

        except Exception as e:
            break