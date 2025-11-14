import tkinter as tk
from tkinter import ttk, messagebox
from controls.secoes.caminho_relativo import caminho_relativo

def abrir_tela_data():
    janela = tk.Toplevel()
    janela.title("Período de Consulta")
    janela.geometry("400x250")
    janela.iconbitmap(caminho_relativo("images/icon_postalis.ico"))
    janela.resizable(False, False)

    #Função para bloquear a chamada de outra tela
    janela.grab_set()

    resultado = {"mes_ini": None, "ano_ini": None, "mes_fim": None, "ano_fim": None}

    # === Frame do título ===
    frame_titulo = tk.Frame(janela, pady=10)
    frame_titulo.pack()
    lbl_titulo = tk.Label(frame_titulo, text="Informar o Período da Consulta", font=("Arial", 14, "bold"))
    lbl_titulo.pack()

    # === Frame das datas ===
    frame_datas = tk.Frame(janela, padx=20, pady=10)
    frame_datas.pack()

    # Dados para os combos
    meses = [f"{i:02}" for i in range(1, 13)]
    anos = [str(i) for i in range(2020, 2036)]

    # === Data Inicial ===
    tk.Label(frame_datas, text="Data Inicial:").grid(row=0, column=0, sticky="e", pady=5)
    combo_mes_ini = ttk.Combobox(frame_datas, values=meses, width=6, state="readonly")
    combo_mes_ini.grid(row=0, column=1, pady=5, padx=10)
    combo_mes_ini.set("01")

    #tk.Label(frame_datas, text="Ano Inicial:").grid(row=1, column=0, sticky="e", pady=5)
    combo_ano_ini = ttk.Combobox(frame_datas, values=anos, width=6, state="readonly")
    combo_ano_ini.grid(row=0, column=2, pady=5, padx=10)
    combo_ano_ini.set("2025")

    # === Data Final ===
    tk.Label(frame_datas, text="Data Final:").grid(row=2, column=0, sticky="e", pady=5)
    combo_mes_fim = ttk.Combobox(frame_datas, values=meses, width=6, state="readonly")
    combo_mes_fim.grid(row=2, column=1, pady=5, padx=10)
    combo_mes_fim.set("01")

    #tk.Label(frame_datas, text="Ano Final:").grid(row=3, column=0, sticky="e", pady=5)
    combo_ano_fim = ttk.Combobox(frame_datas, values=anos, width=6, state="readonly")
    combo_ano_fim.grid(row=2, column=2, pady=5, padx=10)
    combo_ano_fim.set("2025")

    # === Frame dos botões ===
    frame_botoes = tk.Frame(janela, pady=20, padx=30, bd=2, relief="ridge")
    frame_botoes.pack()

    def pesquisar():
        resultado["mes_ini"] = combo_mes_ini.get()
        resultado["ano_ini"] = combo_ano_ini.get()
        resultado["mes_fim"] = combo_mes_fim.get()
        resultado["ano_fim"] = combo_ano_fim.get()
        janela.destroy()

    def sair():
        resultado.clear()
        janela.destroy()

    btn_pesquisar = tk.Button(frame_botoes, text="Pesquisar", width=12, command=pesquisar)
    btn_pesquisar.grid(row=0, column=0, padx=10)

    btn_sair = tk.Button(frame_botoes, text="Sair", width=12, command=sair)
    btn_sair.grid(row=0, column=1, padx=10)

    janela.wait_window()
    return resultado