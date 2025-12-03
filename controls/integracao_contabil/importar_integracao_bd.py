import os
import pdfplumber
import pandas as pd
import re

def import_integracao_contabil_bd(pasta):
    """
    Extrair dados dos PDFs de integração contábil do Plano BD
    """
    try:
        dados_folha = []

        # regex explicação:
        # ^\s*                 -> início da linha (com optional espaços)
        # (\d{2,6})            -> código numérico (ex: 1460)
        # \s+(.+?)\s+          -> descrição (lazy) seguida por espaços
        # ([\d\.]+)            -> conta (ex: 2.0.1.0.10.10.10.00000)
        # \s+([0-9\.]{2,})     -> auxiliar (ex: 00.00.00.00.00)
        # \s+([CD])\s+         -> D ou C
        # ([\d\.,]+)           -> valor com '.' como separador de milhares e ',' decimal
        padrao_rubrica = re.compile(
            r'^\s*(\d{2,6})\s+(.+?)\s+([\d\.]+)\s+([0-9\.]{2,})\s+([CD])\s+([\d\.,]+)\s*$',
            flags=re.MULTILINE | re.UNICODE
        )

        # regex para espécie e CD
        padrao_especie = re.compile(
            r'ESPÉCIE:\s*(.+?)\s*CD:\s*(\d+)', flags=re.IGNORECASE
        )

        especie_atual = None
        cd_atual = None

        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith('.pdf')]
        if not arquivos:
            print("⚠️ Nenhum PDF encontrado na pasta informada.")
            return pd.DataFrame()

        for nome_arquivo in arquivos:
            caminho_pdf = os.path.join(pasta, nome_arquivo)
            print(f"\n📄 Lendo: {nome_arquivo}")

            with pdfplumber.open(caminho_pdf) as pdf:
                for i, pagina in enumerate(pdf.pages, start=1):
                    texto = pagina.extract_text()
                    if not texto:
                        continue

                    for linha in texto.splitlines():
                        linha = linha.strip()
                        if not linha:
                            continue

                        # Detecta nova ESPÉCIE + CD
                        m_especie = padrao_especie.search(linha)
                        if m_especie:
                            especie_atual = m_especie.group(1).strip()
                            cd_atual = m_especie.group(2).strip()
                            continue

                        # Detecta rubrica
                        m = padrao_rubrica.search(linha)
                        if m:
                            codigo = m.group(1)
                            descricao = m.group(2).strip()
                            conta = m.group(3)
                            auxiliar = m.group(4)
                            dc = m.group(5).upper()
                            valor_text = m.group(6)

                            # normalizar valor
                            valor_num = float(
                                valor_text.replace(".", "").replace(",", ".")
                            )
                            if dc == "D":
                                valor_num = -abs(valor_num)

                            dados_folha.append({
                                "arquivo": nome_arquivo,
                                "pagina": i,
                                "especie": especie_atual,
                                "cd": cd_atual,
                                "codigo": codigo,
                                "descricao": descricao,
                                "conta": conta,
                                "auxiliar": auxiliar,
                                "dc": dc,
                                "valor": valor_num
                            })

        df = pd.DataFrame(dados_folha)

        if df.empty:
            print("\n⚠️ Nenhum dado foi extraído.")
        else:
            print(f"\n✅ Total de linhas extraídas: {len(df)}")
            print(df.head())

        if not df.empty:
            df.to_excel("Integração_Contábil_BD.xlsx", index=False)
            print("📁 Arquivo salvo como 'Integração_Contábil_BD.xlsx'")

        return df

    except Exception as e:
        print(f"[DEBUG] Erro na importação dos arquivos: {e}")
        return pd.DataFrame()
