import os
import pdfplumber
import pandas as pd
import re

def importar_arquivos_folha_pp(pasta):
    try:
        dados_folha = []

        # Regex atualizado: código | descrição | valor | [opcionalmente código final]
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

                    # Extrair cabeçalho
                    tipo_folha = None
                    competencia = None
                    for linha in texto.splitlines():
                        if "TIPO FOLHA" in linha.upper():   # <<< Ajuste aqui
                            partes = linha.split(":")
                            if len(partes) > 1:
                                tipo_folha = partes[1].strip()
                        if "REFERÊNCIA" in linha.upper():
                            partes = linha.split(":")
                            if len(partes) > 1:
                                competencia = partes[1].strip()

                    # Extrair dados de PROVENTO e DESCONTO
                    bloco_atual = None
                    for linha in texto.splitlines():
                        linha = linha.strip()

                        if linha.startswith("PROVENTO"):
                            bloco_atual = "PROVENTO"
                            continue
                        elif linha.startswith("DESCONTO"):
                            bloco_atual = "DESCONTO"
                            continue
                        elif linha.startswith("TOTAL") or not linha:
                            bloco_atual = None
                            continue

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

        # Criar DataFrame
        df = pd.DataFrame(dados_folha)

        if df.empty:
            print("\n⚠️ Nenhum dado foi extraído.")
        else:
            print(f"\n✅ Total de linhas extraídas: {len(df)}")
            print(df.head())

        # (Opcional) Salvar em Excel
        if not df.empty:
            df.to_excel("resumo_extraido_plano_PostalPrev.xlsx", index=False)

        return df

    except Exception as e:
        print(f"[DEBUG] Erro na importação dos arquivos: {e}")
        return pd.DataFrame()
