from tkinter import messagebox
from views.tela_escolher_data import abrir_tela_data
from views.tela_login import abrir_tela_login

def chamar_login_e_extrair_sentinela(funcao_extracao, titulo="Sistema Sentinela"):
    periodo = abrir_tela_data()

    if not periodo or not all(periodo.values()):
        return

    def valores_ao_logar(usuario, senha):    
        if usuario and senha:
            print("Período selecionado:")
            print(f"{periodo['mes_ini']}/{periodo['ano_ini']} até {periodo['mes_fim']}/{periodo['ano_fim']}")
            funcao_extracao(
                usuario, senha,
                periodo["mes_ini"], periodo["ano_ini"],
                periodo["mes_fim"], periodo["ano_fim"]
            )
        
    messagebox.showinfo("Bem-Vindo", "Favor inserir Usuário e Senha de acesso ao Sistema Sentinela.")
    abrir_tela_login(callback=valores_ao_logar)

def chamar_login_e_extrair(funcao_extracao, titulo="Sistema Atena"):
    periodo = abrir_tela_data()

    if not periodo or not all(periodo.values()):
        return

    def valores_ao_logar(usuario, senha):    
        if usuario and senha:
            print("Período selecionado:")
            print(f"{periodo['mes_ini']}/{periodo['ano_ini']} até {periodo['mes_fim']}/{periodo['ano_fim']}")
            funcao_extracao(
                usuario, senha,
                periodo["mes_ini"], periodo["ano_ini"],
                periodo["mes_fim"], periodo["ano_fim"]
            )
    
    messagebox.showinfo("Bem-Vindo", f"Favor inserir Usuário e Senha de acesso ao {titulo}!")
    abrir_tela_login(callback=valores_ao_logar)

def chamar_extrair_pp_atena():
    from controls.analisar_pps.extrair_pp_atena import extrair_pp_atena
    chamar_login_e_extrair(extrair_pp_atena, titulo="Sistema Atena - PPs Realizadas")

def chamar_extrair_orcamento_atena():
    from controls.conciliacao.extrair_orcamento_atena import extrair_orcamento_atena
    chamar_login_e_extrair(extrair_orcamento_atena, titulo="Sistema Atena - Orçamento")

def chamar_extrair_remanejamento():
    from controls.relatorio_operacional.extrair_remanejamentos import extrair_remanejamento_atena
    chamar_login_e_extrair(extrair_remanejamento_atena, titulo="Sistema Atena - Orçamento")

def chamar_extair_pp_sentinela():
    from controls.analisar_pps.extrair_pp_sentinela import extrair_pp_sentinela
    chamar_login_e_extrair_sentinela(extrair_pp_sentinela, titulo="Sistema Sentinela - PPs Realizadas")

def chamar_extrair_orcamento_sentinela():
    from controls.conciliacao.extrair_orcamento_sentinela import extrair_orcamento_sentinela
    chamar_login_e_extrair_sentinela(extrair_orcamento_sentinela, titulo="Sistema Sentinela -Orçamento")


