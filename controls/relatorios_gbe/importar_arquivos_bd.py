import os
import pdfplumber
import pandas as pd
import re
from pathlib import Path

# compile no topo do arquivo
PADRAO_TIPO_FOLHA = re.compile(r'TIPO\s*DE\s*FOLHA\s*:\s*([^\n:]+)', re.I)
PADRAO_REFERENCIA = re.compile(r'REFER[ÊE]NCIA\s*:\s*([^\n:]+)', re.I)

def importar_arquivos_folha_bd(pasta):
    try:
        dados_folha = []
        padrao_rubrica = re.compile(
            r'^\s*(\d{3,6})\s+(.*?)\s+(\d{1,3}(?:\.\d{3})*,\d{2})(?:\s+\d+)?\s*$'
        )

        for nome_arquivo in os.listdir(pasta):
            if not nome_arquivo.lower().endswith('.pdf'):
                continue

            caminho_pdf = os.path.join(pasta, nome_arquivo)
            print(f"\n📄 Lendo: {nome_arquivo}")

            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if not texto:
                        continue

                    if "RESUMO DA FOLHA DE PAGAMENTO" not in texto.upper():
                        continue

                    # --- NOVO: extrair cabeçalho por regex no texto inteiro ---
                    tipo_folha = None
                    competencia = None
                    t = texto.replace('\xa0', ' ')

                    m_tipo = PADRAO_TIPO_FOLHA.search(t)
                    if m_tipo:
                        tipo_folha = m_tipo.group(1).strip()

                    m_ref = PADRAO_REFERENCIA.search(t)
                    if m_ref:
                        competencia = m_ref.group(1).strip()

                    # --- resto igual: varrer blocos e rubricas ---
                    bloco_atual = None
                    for linha in texto.splitlines():
                        linha = linha.strip()

                        if linha.startswith("PROVENTOS"):
                            bloco_atual = "PROVENTO"; continue
                        elif linha.startswith("DESCONTOS"):
                            bloco_atual = "DESCONTO"; continue
                        elif linha.startswith("TOTAL") or not linha:
                            bloco_atual = None; continue

                        if bloco_atual:
                            match = padrao_rubrica.match(linha)
                            if match:
                                cod, descricao, valor = match.groups()
                                dados_folha.append({
                                    "tipo": bloco_atual,
                                    "cod_rubrica": cod,
                                    "descricao_rubrica": descricao,
                                    "valor": float(valor.replace(".", "").replace(",", ".")),
                                    "competencia": competencia,
                                    "tipo_folha": tipo_folha,
                                    "arquivo": nome_arquivo
                                })

        df = pd.DataFrame(dados_folha)
        
        if df.empty:
            print("\n⚠️ Nenhum dado foi extraído.")
        else:
            print(f"\n✅ Total de linhas extraídas: {len(df)}")
            print(df.head())

        if not df.empty:
            df.to_excel("resumo_extraido_plano_BD.xlsx", index=False)

        #Salvar arquivo em json
        base_diretorio = Path(__file__).resolve().parents[2]
        caminho_json = base_diretorio / "models" / "base_folha" / "tb_folha_bd.json"
        df_json = df.to_json(caminho_json, orient="records", force_ascii=False, indent=4)

        print(f"[DEBUG] Arquivo JSON salvo no diretorio:{caminho_json}")


        return df

    except Exception as e:
        print(f"[DEBUG] Erro na importação dos arquivos: {e}")
        return pd.DataFrame()

