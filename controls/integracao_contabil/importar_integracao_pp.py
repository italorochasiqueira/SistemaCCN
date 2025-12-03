import os
import pdfplumber
import pandas as pd
import re

def importar_integracao_contabil_pp(pasta, debug=True):
    """
    Extrai rubricas do PDF (adaptado ao layout enviado).
    - Primeiro tenta um regex robusto.
    - Se falhar, tenta um parser por fim de linha (fallback).
    - Salva um Excel por plano quando encontrar dados.
    """

    try:
        dados = []

        # Regex principal (mais flexível que o anterior)
        padrao_rubrica = re.compile(
            r'^\s*(?:([CDU])\s+)?'         # prefixo opcional C/U/D
            r'(\d{3,6})\s+'                # código (3-6 dígitos)
            r'(.+?)\s+'                    # descrição (lazy)
            r'(\d(?:\.\d+){3,8})\s+'       # conta: começa com dígito, 4-9 blocos
            r'([.\d\s]{0,40})\s*'          # auxiliar (pontos ou números) - opcional
            r'([CDU])\s+'                  # D/C/U final
            r'([\d\.,]+)\s*$',             # valor
            flags=re.UNICODE
        )

        padrao_especie = re.compile(r'ESP[ÉE]CIE[:]?\s*(.+)', flags=re.IGNORECASE)
        padrao_plano = re.compile(r'PLANO[: ]*\s*(\d+)', flags=re.IGNORECASE)

        # padrão para identificar D/C + valor no final (usado no fallback)
        padrao_dc_valor_final = re.compile(r'([CDU])\s+([\d\.,]+)\s*$')

        especie_atual = None
        plano_atual = None

        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith('.pdf')]
        if not arquivos:
            print("⚠️ Nenhum PDF encontrado.")
            return pd.DataFrame()

        for nome_arquivo in arquivos:
            caminho_pdf = os.path.join(pasta, nome_arquivo)
            print(f"\n📄 Lendo: {nome_arquivo}")

            with pdfplumber.open(caminho_pdf) as pdf:
                for num_pag, pagina in enumerate(pdf.pages, start=1):
                    texto = pagina.extract_text()
                    if debug:
                        print("\n" + "="*30)
                        print(f"PÁGINA {num_pag}")
                        print("="*30)
                        print(texto)
                        print("-"*30)

                    if not texto:
                        if debug:
                            print(f"Página {num_pag} sem texto.")
                        continue

                    for linha_original in texto.splitlines():
                        linha = linha_original.strip()
                        if not linha:
                            continue

                        if debug:
                            print(f"\nLinha lida: {linha}")

                        # Detecta espécie
                        m_especie = padrao_especie.search(linha)
                        if m_especie:
                            especie_atual = m_especie.group(1).strip()
                            if debug:
                                print(f"--> ESPÉCIE: {especie_atual}")
                            continue

                        # Detecta plano
                        m_plano = padrao_plano.search(linha)
                        if m_plano:
                            plano_atual = int(m_plano.group(1))
                            if debug:
                                print(f"--> PLANO: {plano_atual}")
                            continue

                        # Ignora linhas de total
                        if linha.upper().startswith("TOTAL"):
                            if debug:
                                print("--> Linha TOTAL ignorada")
                            continue

                        # 1) tenta regex principal
                        m = padrao_rubrica.search(linha)
                        if m:
                            if debug:
                                print("--> CASOU no REGEX principal")
                            dc_inicio = m.group(1)
                            codigo = m.group(2)
                            descricao = m.group(3).strip()
                            conta = m.group(4).strip()
                            auxiliar = m.group(5).strip() if m.group(5) else None
                            dc_final = m.group(6)
                            valor_texto = m.group(7)

                            dc = (dc_inicio if dc_inicio else dc_final).upper()
                            try:
                                valor = float(valor_texto.replace(".", "").replace(",", "."))
                            except Exception:
                                # tentativa extra de limpeza
                                valor = float(re.sub(r'[^\d,\.]', '', valor_texto).replace(".", "").replace(",", "."))

                            if dc == "D":
                                valor = -abs(valor)

                            dados.append({
                                "arquivo": nome_arquivo,
                                "pagina": num_pag,
                                "especie": especie_atual,
                                "plano": plano_atual,
                                "codigo": codigo,
                                "descricao": descricao,
                                "conta": conta,
                                "auxiliar": auxiliar,
                                "dc": dc,
                                "valor": valor
                            })
                            continue  # próxima linha

                        # 2) fallback: procura D/C + valor no final e tenta extrair conta como último token com pontos
                        m_end = padrao_dc_valor_final.search(linha)
                        if m_end:
                            dc_fb = m_end.group(1).upper()
                            valor_texto = m_end.group(2)
                            # remove o trecho final (dc+valor) da linha para analisar o resto
                            prefixo = linha[:m_end.start()].strip()
                            # tenta encontrar a última ocorrência de um bloco com pontos (a conta)
                            contas = re.findall(r'\d(?:\.\d+){3,8}', prefixo)
                            if contas:
                                conta = contas[-1]
                                # descrição fica entre código (primeiro número) e a conta encontrada
                                # tenta encontrar o código (primeiro grupo de 3-6 dígitos)
                                m_codigo = re.search(r'(\d{3,6})', prefixo)
                                codigo = m_codigo.group(1) if m_codigo else None

                                # descrição: tudo entre o código (após) e a conta (antes)
                                if codigo and conta:
                                    # busca posição do código e da conta no prefixo
                                    pos_codigo = prefixo.find(codigo)
                                    pos_conta = prefixo.rfind(conta)
                                    descricao = prefixo[pos_codigo + len(codigo):pos_conta].strip() if pos_conta > pos_codigo else prefixo
                                else:
                                    descricao = prefixo

                                # tenta extrair auxiliar como parte entre conta e DC (pode ser . . . . ou números)
                                # já removemos DC+valor, então auxiliar pode vir junto com prefixo: procurar seq de pontos depois da conta
                                aux_match = re.search(re.escape(conta) + r'\s+([.\d\s]{1,40})$', prefixo)
                                auxiliar = None
                                if aux_match:
                                    auxiliar = aux_match.group(1).strip()

                                # converte valor
                                try:
                                    valor = float(valor_texto.replace(".", "").replace(",", "."))
                                except Exception:
                                    valor = float(re.sub(r'[^\d,\.]', '', valor_texto).replace(".", "").replace(",", "."))

                                if dc_fb == "D":
                                    valor = -abs(valor)

                                if debug:
                                    print("--> Fallback aplicado: achou DC+VALOR no final e extraíu conta via busca de padrão")
                                    print(f"    codigo={codigo} conta={conta} dc={dc_fb} valor={valor} auxiliar={auxiliar}")

                                dados.append({
                                    "arquivo": nome_arquivo,
                                    "pagina": num_pag,
                                    "especie": especie_atual,
                                    "plano": plano_atual,
                                    "codigo": codigo,
                                    "descricao": descricao,
                                    "conta": conta,
                                    "auxiliar": auxiliar,
                                    "dc": dc_fb,
                                    "valor": valor
                                })
                                continue
                            else:
                                if debug:
                                    print("--> Fallback encontrou DC+VALOR no final, mas NÃO encontrou conta no prefixo")
                                # cairá no "não casou" abaixo

                        # se chegou aqui, não casou nem no regex nem no fallback
                        if debug:
                            print("--> ❌ NÃO CASOU (regex e fallback falharam)")

        df = pd.DataFrame(dados)

        if df.empty:
            print("\n⚠️ Nenhum dado extraído.")
            return df

        if debug:
            print("\n\n=== DataFrame extraído (preview) ===")
            print(df.head(40))

        # Salvar por plano
        for plano in sorted(df["plano"].dropna().unique()):
            df_plano = df[df["plano"] == plano]
            nome_excel = f"Integracao_Contabil_PP_Plano_{plano}.xlsx"
            df_plano.to_excel(nome_excel, index=False)
            print(f"📁 Arquivo gerado: {nome_excel} (linhas: {len(df_plano)})")

        return df

    except Exception as e:
        print(f"[ERRO] {e}")
        return pd.DataFrame()
