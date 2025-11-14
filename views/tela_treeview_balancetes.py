import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from PIL import Image, ImageTk
from controls.secoes.caminho_relativo import caminho_relativo

ARQUIVOS_JSON = {
    "BD": "tab_balancete_bd.json",
    "PP": "tab_balancete_pp.json",
    "PGA": "tab_balancete_pga.json"
}

def abrir_tela_rel_balancete():
    def format_valor(valor):
        try:
            return "{:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "0,00"

    janela = tk.Toplevel()
    janela.title("Balancetes")
    janela.geometry("1100x600")
    janela.iconbitmap(caminho_relativo("images/icon_postalis.ico"))
    janela.resizable(False, False)

    janela.grid_rowconfigure(1, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    # Frame título
    frame_titulo = tk.Frame(janela, pady=10)
    frame_titulo.grid(row=0, column=0, sticky="ew", padx=10)

    try:
        caminho_logo = caminho_relativo("images/logo_postalis.jpg")
        imagem_logo = Image.open(caminho_logo).resize((250, 60), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(imagem_logo)
        label_logo = tk.Label(frame_titulo, image=logo)
        label_logo.image = logo
        label_logo.grid(row=0, column=0, padx=10)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")

    label_titulo = tk.Label(frame_titulo, text="Balancetes Importados", font=("Arial", 16, "bold"))
    label_titulo.grid(row=0, column=1, padx=10, sticky="w")

    notebook = ttk.Notebook(janela)
    notebook.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    treeviews = {}
    colunas = ["Data", "Plano", "Conta Contábil", "Descrição", "Saldo Anterior", "Débitos", "Créditos", "Mov. Líquido", "Saldo Atual"]

    for plano, arquivo_json in ARQUIVOS_JSON.items():
        frame_aba = tk.Frame(notebook)
        frame_aba.grid_rowconfigure(0, weight=1)
        frame_aba.grid_columnconfigure(0, weight=1)
        notebook.add(frame_aba, text=plano)

        scrollbar_y = tk.Scrollbar(frame_aba, orient="vertical")
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        tree = ttk.Treeview(
            frame_aba,
            columns=colunas,
            show="headings",
            yscrollcommand=scrollbar_y.set
        )
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.config(command=tree.yview)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)

        treeviews[plano] = tree

        # Carrega JSON
        caminho_json = caminho_relativo(os.path.join("models", "balancetes", arquivo_json))
        if os.path.exists(caminho_json):
            try:
                with open(caminho_json, "r", encoding="utf-8") as f:
                    conteudo = f.read().strip()

                if not conteudo or conteudo in ["[]", "{}"]:
                    tree.insert("", "end", values=("Sem dados disponíveis",) + ("",) * (len(colunas) - 1))
                    continue

                df = pd.read_json(caminho_json)  # Não use lines=True

                if df.empty or not all(col in df.columns for col in ["Data", "Plano", "Conta Contábil", "Descrição"]):
                    tree.insert("", "end", values=("Sem dados disponíveis",) + ("",) * (len(colunas) - 1))
                else:
                    for _, row in df.iterrows():
                        tree.insert("", "end", values=(
                            row.get("Data", ""),
                            row.get("Plano", ""),
                            row.get("Conta Contábil", ""),
                            row.get("Descrição", ""),
                            format_valor(row.get("Saldo Anterior", 0)),
                            format_valor(row.get("Débitos", 0)),
                            format_valor(row.get("Créditos", 0)),
                            format_valor(row.get("Mov. Líquido", 0)),
                            format_valor(row.get("Saldo Atual", 0))
                        ))
            except Exception as e:
                print(f"Erro ao carregar {arquivo_json}: {e}")
                tree.insert("", "end", values=("Erro ao carregar",) + ("",) * (len(colunas) - 1))
        else:
            tree.insert("", "end", values=("Arquivo não encontrado",) + ("",) * (len(colunas) - 1))

    # Frame de seleção
    frame_selecao = tk.Frame(janela)
    frame_selecao.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")
    frame_selecao.grid_columnconfigure(1, weight=1)

    tk.Label(frame_selecao, text="Plano para Exportar:").grid(row=0, column=0, sticky="e", padx=5)
    plano_var = tk.StringVar()
    combo_plano = ttk.Combobox(frame_selecao, textvariable=plano_var, state="readonly", values=list(ARQUIVOS_JSON.keys()), width=20)
    combo_plano.grid(row=0, column=1, sticky="w", padx=5)

    # Frame de botões
    frame_botoes = tk.Frame(janela, pady=10, bd=2, relief="ridge")
    frame_botoes.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
    frame_botoes.grid_columnconfigure((0, 4), weight=1)

    def exportar():
        plano = plano_var.get()
        if not plano:
            messagebox.showwarning("Aviso", "Selecione o plano antes de exportar.")
            return
        messagebox.showinfo("Exportar", f"Exportando relatório do plano: {plano}")

    def encaminhar():
        plano = plano_var.get()
        if not plano:
            messagebox.showwarning("Aviso", "Selecione o plano antes de encaminhar.")
            return
        messagebox.showinfo("Encaminhar", f"Encaminhando relatório do plano: {plano}")

    btn_relatorio = tk.Button(frame_botoes, text="Gerar Relatório", width=15, command=exportar)
    btn_relatorio.grid(row=0, column=1, padx=10)

    btn_encaminhar = tk.Button(frame_botoes, text="Encaminhar", width=15, command=encaminhar)
    btn_encaminhar.grid(row=0, column=2, padx=10)

    btn_sair = tk.Button(frame_botoes, text="Sair", width=15, command=janela.destroy)
    btn_sair.grid(row=0, column=3, padx=10)

    janela.mainloop()
