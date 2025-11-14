import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from views.tela_extrair_balancetes import abrir_tela_comandos
from views.tela_treeview_balancetes import abrir_tela_rel_balancete
from views.tela_importar_previdenciario import abrir_tela_importar_previdenciario
from views.tela_importar_integracao_contabil import abrir_tela_importar_integracao_contabil
from views.tela_importar_plan_mercer import abrir_tela_importar_plan_mercer
from controls.secoes.caminho_relativo import caminho_relativo


def abrir_tela_principal():
    janela = tk.Tk()
    janela.title("Postalis - GCO/CCN")
    janela.geometry("600x500")
    janela.iconbitmap(caminho_relativo("images/icon_postalis.ico"))
    janela.resizable(False, False)

    menubar = tk.Menu(janela)
    menu_principal = tk.Menu(menubar, tearoff=0)
    menu_principal.add_command(label="Parâmetros", command=...)
    menu_principal.add_separator()
    menu_principal.add_command(label="Sair", command=janela.destroy)

    menubar.add_cascade(label="Menu", menu=menu_principal)

    menu_importar_arquivos = tk.Menu(menubar, tearoff=0)
    menu_importar_arquivos.add_command(label="Importar Folhas GBE", command=abrir_tela_importar_previdenciario)
    menu_importar_arquivos.add_command(label="Importar Integração Contábil", command=abrir_tela_importar_integracao_contabil)
    menu_importar_arquivos.add_command(label="Importar Planilha Mercer", command=abrir_tela_importar_plan_mercer)
    
    menu_importar_arquivos.add_separator()
    menu_relatorio_prev = tk.Menu(menu_importar_arquivos, tearoff=0)
    menu_importar_arquivos.add_cascade(label="Relatórios", menu=menu_relatorio_prev)
    menubar.add_cascade(label="Importar Arquivos", menu=menu_importar_arquivos)

     
    menu_contabil = tk.Menu(menubar, tearoff=0)
    menu_contabil.add_command(label="Extrair Movimento", command=abrir_tela_comandos)
    menu_contabil.add_separator()

    #sub-menu relatórios
    menu_relatorios = tk.Menu(menu_contabil, tearoff=0)
    menu_relatorios.add_command(label="Rel. Balancete", command=abrir_tela_rel_balancete)
    menu_relatorios.add_command(label="Rel. Razão", command=...)

    menu_contabil.add_cascade(label="Relatórios", menu=menu_relatorios)
    menubar.add_cascade(label="Movimento Contábil", menu=menu_contabil)

    janela.config(menu=menubar)

    # Frame principal
    frame = tk.Frame(janela, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # === Carregar a imagem da logo ===
    caminho_logo = caminho_relativo("images/logo_postalis.jpg")
    imagem_original = Image.open(caminho_logo)
    imagem_redimensionada = imagem_original.resize((400, 80))  # ajuste o tamanho conforme necessário
    logo_img = ImageTk.PhotoImage(imagem_redimensionada)

    # === Label da logo ===
    lbl_logo = tk.Label(frame, image=logo_img)
    lbl_logo.image = logo_img  # mantém uma referência para não ser coletado pelo garbage collector
    lbl_logo.grid(row=0, column=0, pady=(0, 10))

    # Título
    lbl_titulo = tk.Label(frame, text="Sistema Coordenação de Contabilidade", font=("Arial", 16, "bold"))
    lbl_titulo.grid(row=1, column=0, pady=(0, 15))

    janela.mainloop()