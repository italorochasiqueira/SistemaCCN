import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from controls.secoes.caminho_relativo import caminho_relativo
# from controls.integracao_contabil.importar_integracao_bd import importar_arquivos_integracao_bd
# from controls.integracao_contabil.importar_integracao_bps import importar_arquivos_integracao_bps
# from controls.integracao_contabil.importar_integracao_pp import importar_arquivos_integracao_postalprev


def abrir_tela_importar_integracao_contabil():
    janela = tk.Toplevel()
    janela.title("Postalis - GCO/CCN")
    janela.geometry("500x350")
    janela.iconbitmap(caminho_relativo("images/icon_postalis.ico"))
    janela.resizable(False, False)

    # Frame principal centralizado
    frame_principal = tk.Frame(janela, padx=20, pady=20)
    frame_principal.grid(row=0, column=0, sticky="nsew")

    # Configurações para expandir corretamente
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    # ======== Frame Título ========
    frame_titulo = tk.Frame(frame_principal, pady=10)
    frame_titulo.grid(row=0, column=0, sticky="ew")

    lbl_titulo = tk.Label(frame_titulo, text="Importar arquivos de Integração", font=("Arial", 14, "bold"))
    lbl_titulo.grid(row=0, column=0, columnspan=4, sticky="n", pady=5)

    # ======== Frame Tipo de Plano ========
    frame_plano = tk.LabelFrame(frame_principal, text="Selecionar Plano", padx=10, pady=10)
    frame_plano.grid(row=1, column=0, pady=5, sticky="ew")

    plano_var = tk.StringVar(value="BD")  # valor inicial

    rdb_bd = tk.Radiobutton(frame_plano, text="Plano BD", variable=plano_var, value="BD")
    rdb_bd.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    rdb_bps = tk.Radiobutton(frame_plano, text="Plano BPS", variable=plano_var, value="BPS")
    rdb_bps.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    rdb_postalprev = tk.Radiobutton(frame_plano, text="PostalPrev", variable=plano_var, value="PostalPrev")
    rdb_postalprev.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # ======== Frame Pasta ========
    frame_pasta = tk.LabelFrame(frame_principal, text="Selecionar pasta", padx=10, pady=10)
    frame_pasta.grid(row=2, column=0, pady=5, sticky="ew")

    # Ícone da pasta
    imagem_original = Image.open(caminho_relativo("images/pasta.png"))
    imagem_redimensionada = imagem_original.resize((25, 25), Image.Resampling.LANCZOS)
    imagem_pasta = ImageTk.PhotoImage(imagem_redimensionada)

    lbl_pasta = tk.Label(frame_pasta, image=imagem_pasta)
    lbl_pasta.image = imagem_pasta
    lbl_pasta.grid(row=0, column=0, padx=5, sticky="e")

    entrada_pasta = tk.Entry(frame_pasta, width=50)
    entrada_pasta.grid(row=0, column=1, padx=5, sticky="ew")

    def selecionar_pasta():
        pasta = filedialog.askdirectory()
        if pasta:
            entrada_pasta.delete(0, tk.END)
            entrada_pasta.insert(0, pasta)

    btn_pasta = tk.Button(frame_pasta, text="...", width=3, command=selecionar_pasta)
    btn_pasta.grid(row=0, column=2, padx=5, sticky="w")

    # Ajusta expansão horizontal
    frame_pasta.grid_columnconfigure(1, weight=1)

    # ======== Frame Botões ========
    frame_botoes = tk.Frame(frame_principal, pady=20)
    frame_botoes.grid(row=3, column=0, pady=5)

    def importar_arquivos():
        pasta = entrada_pasta.get()
        plano = plano_var.get()

        if not pasta:
            messagebox.showwarning("Aviso", "Selecione uma pasta de arquivos para importar.")
            return

        # try:
            # if plano == "BD":
            #     df = importar_arquivos_integracao_bd(pasta)
            # elif plano == "BPS":
            #     df = importar_arquivos_integracao_bps(pasta)
            # elif plano == "PostalPrev":
            #     df = importar_arquivos_integracao_postalprev(pasta)
            # else:
            #     df = None

            # if df is not None and not df.empty:
            #     messagebox.showinfo("Sucesso", f"Arquivos do plano {plano} importados da pasta:\n{pasta}")
            # elif df is not None and df.empty:
            #     messagebox.showwarning("Aviso", f"Nenhum dado foi encontrado para o plano {plano}.")

        # except Exception as e:
        #     messagebox.showerror("Erro", f"Ocorreu um erro na importação: {e}")

    #Frame dos Botões
    frame_botoes = tk.LabelFrame(frame_principal, pady=20)
    frame_botoes.grid(row=3, column=0, pady=5, sticky="ew")

    #Centralizar botões no Label
    frame_botoes.grid_columnconfigure(0, weight=1)
    frame_botoes.grid_columnconfigure(1, weight=1)

    btn_importar = tk.Button(frame_botoes,
                             text="Importar", 
                             width=15, 
                             command=importar_arquivos,
                             activebackground="#54E478", 
                             activeforeground="white")
    btn_importar.grid(row=0, column=0, padx=10)

    btn_sair = tk.Button(frame_botoes, 
                         text="Sair", 
                         width=15, 
                         command=janela.destroy,
                         activebackground="#AD5E62",
                         activeforeground="white")
    btn_sair.grid(row=0, column=1, padx=10)

    janela.mainloop()
