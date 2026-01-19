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

@app.websocket("/neuro-link")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Conexão Neural Estabelecida...\nBem-vindo ao GuinaOS v2.0 (Web Edition)")
    
    while True:
        try:
            # Espera o comando do Front-end
            data = await websocket.receive_text()
            
            # Processa no Python
            resposta = sistema.processar_comando_web(data)
            
            # Devolve a resposta pro Front-end
            await websocket.send_text(resposta)
        except:
            break