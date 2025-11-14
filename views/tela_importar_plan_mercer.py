#Tela para importação das folhas previdenciárias

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from controls.secoes.caminho_relativo import caminho_relativo


def abrir_tela_importar_plan_mercer():
    janela = tk.Toplevel()
    janela.title("Postalis - GCO/CCN")
    janela.geometry("500x350")
    janela.iconbitmap(caminho_relativo("images/icon_postalis.ico"))
    janela.resizable(False, False)

    # Frame principal centralizado
    frame_principal = tk.Frame(janela, padx=20, pady=20)
    frame_principal.place(relx=0.5, rely=0.5, anchor="center")

    # Configurações para expandir corretamente
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    # ======== Frame Título ========
    frame_titulo = tk.Frame(frame_principal, pady=5)
    frame_titulo.grid(row=0, column=0, sticky="ew")

    lbl_titulo = tk.Label(frame_titulo, text="Importar Planilha Mercer", font=("Arial", 14, "bold"))
    lbl_titulo.grid(row=0, column=0, columnspan=4, pady=5)

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
    frame_botoes = tk.LabelFrame(frame_principal, pady=20)
    frame_botoes.grid(row=3, column=0, pady=5, sticky="ew")

    #Centralizar botões no Label
    frame_botoes.grid_columnconfigure(0, weight=1)
    frame_botoes.grid_columnconfigure(1, weight=1)

    btn_importar = tk.Button(frame_botoes,
                             text="Importar", 
                             width=15, 
                             command=...,
                             #height=2,
                             activebackground="#54E478", 
                             activeforeground="white")
    btn_importar.grid(row=0, column=0, padx=10)

    btn_sair = tk.Button(frame_botoes, 
                         text="Sair", 
                         width=15, 
                         command=janela.destroy,
                         #height=2,
                         activebackground="#AD5E62",
                         activeforeground="white")
    btn_sair.grid(row=0, column=1, padx=10)

    janela.mainloop()
