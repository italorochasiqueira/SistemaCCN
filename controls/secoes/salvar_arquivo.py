from pathlib import Path
import time
import os
import shutil
import zipfile

# Função para esperar o download terminar e mover o arquivo
def mover_arquivo_baixado(plano, periodo, destino_path=None):
    '''
    Função para arquivar download do balancete/razão
    
    '''
    downloads_path = str(Path.home() / "Downloads")
    if not destino_path:
        destino_path = os.getcwd()

    # Aguarda o arquivo aparecer (até 30 segundos)
    timeout = 30
    tempo_inicial = time.time()
    arquivo_baixado = None

    while time.time() - tempo_inicial < timeout:
        arquivos = os.listdir(downloads_path)
        arquivos_xls = [f for f in arquivos if f.endswith(".xls") or f.endswith(".xlsx")]
        if arquivos_xls:
            # Pega o mais recente
            arquivo_baixado = max(
                [os.path.join(downloads_path, f) for f in arquivos_xls],
                key=os.path.getctime
            )
            break
        time.sleep(1)

    if not arquivo_baixado:
        print("[Erro] Arquivo não encontrado na pasta de downloads.")
        return

    # Define novo nome com base no plano e período
    nome_arquivo = f"Plano_{plano}_{periodo.replace('/', '_')}.xlsx"
    caminho_destino = os.path.join(destino_path, nome_arquivo)

    # Move e renomeia
    try:
        shutil.move(arquivo_baixado, caminho_destino)
        print(f"[OK] Arquivo movido para: {caminho_destino}")
    except Exception as e:
        print(f"[Erro] ao mover o arquivo: {e}")

def mover_pasta_baixada(plano, periodo, destino_path=None):
    downloads_path = str(Path.home() / "Downloads")
    if not destino_path:
        destino_path = os.getcwd()

    timeout = 30
    tempo_inicial = time.time()
    arquivo_zip = None

    # Espera o .zip aparecer
    while time.time() - tempo_inicial < timeout:
        arquivos = os.listdir(downloads_path)
        arquivos_zip = [f for f in arquivos if f.endswith(".zip")]
        if arquivos_zip:
            arquivo_zip = max(
                [os.path.join(downloads_path, f) for f in arquivos_zip],
                key=os.path.getctime
            )
            break
        time.sleep(1)

    if not arquivo_zip:
        print("[Erro] Arquivo .zip não encontrado na pasta de downloads.")
        return

    # Define o nome final do .zip
    nome_zip = f"Plano_{plano}_{periodo.replace('/', '_')}.zip"
    caminho_zip_destino = os.path.join(destino_path, nome_zip)

    # Evita sobrescrita
    if os.path.exists(caminho_zip_destino):
        base, ext = os.path.splitext(nome_zip)
        contador = 1
        while os.path.exists(os.path.join(destino_path, f"{base}_{contador}{ext}")):
            contador += 1
        nome_zip = f"{base}_{contador}{ext}"
        caminho_zip_destino = os.path.join(destino_path, nome_zip)

    # Move o .zip
    try:
        shutil.move(arquivo_zip, caminho_zip_destino)
        print(f"[OK] Arquivo .zip movido para: {caminho_zip_destino}")
    except Exception as e:
        print(f"[Erro] ao mover o arquivo .zip: {e}")
        return

    # Extrai o conteúdo do .zip (apenas arquivos .xls ou .xlsx)
    try:
        with zipfile.ZipFile(caminho_zip_destino, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith('.xls') or file.endswith('.xlsx'):
                    zip_ref.extract(file, destino_path)
                    print(f"[OK] Arquivo Excel extraído: {file}")
    except Exception as e:
        print(f"[Erro] ao extrair o arquivo Excel do .zip: {e}")