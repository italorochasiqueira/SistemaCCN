import tkinter as tk
import calendar
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
# from controls.contabil.extrair_balancete import extrair_balancete
# from controls.contabil.extrair_razao import extrair_razao
from controls.secoes.caminho_relativo import caminho_relativo
from views.tela_login import abrir_tela_login

def abrir_tela_comandos():
    janela = tk.Toplevel()
    janela.title("Postalis - GCO/CCN")
    janela.geometry("600x500")
    janela.iconbitmap(caminho_relativo("images/icon_postalis.ico"))
    janela.resizable(False, False)

    # Frame principal
    frame = tk.Frame(janela, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título
    lbl_titulo = tk.Label(frame, text="Extrair Movimento Contábil", font=("Arial", 14, "bold"))
    lbl_titulo.grid(row=0, column=0, pady=(0, 15))

    # Frame Período (dentro do frame principal)
    frame_periodo = tk.LabelFrame(frame, padx=10, pady=10)
    frame_periodo.grid(row=1, column=0, pady=(0, 15))

    lbl_mes = tk.Label(frame_periodo, text="Mês:")
    lbl_mes.grid(row=0, column=0, sticky="e", padx=5)
    entrada_mes = tk.Entry(frame_periodo, width=10)
    entrada_mes.grid(row=0, column=1, padx=5)

    lbl_ano = tk.Label(frame_periodo, text="Ano:")
    lbl_ano.grid(row=0, column=2, sticky="e", padx=5)
    entrada_ano = tk.Entry(frame_periodo, width=10)
    entrada_ano.grid(row=0, column=3, padx=5)

    # Quadro de Flags (também dentro do frame principal)
    quadro_flags = tk.LabelFrame(frame, text="Exportar arquivos", padx=10, pady=10)
    quadro_flags.grid(row=2, column=0, pady=10, sticky="ew")

    var_bd = tk.IntVar()
    var_postal = tk.IntVar()
    var_pga = tk.IntVar()

    chk_bd = tk.Checkbutton(quadro_flags, text="1 - Plano BD", variable=var_bd) #valor 1
    chk_postal = tk.Checkbutton(quadro_flags, text="2 - Plano Postal Prev", variable=var_postal) # valor 3
    chk_pga = tk.Checkbutton(quadro_flags, text="3 - PGA", variable=var_pga) #Tem que apresentar valor 5
    
    chk_bd.grid(row=0, column=0, sticky="w", pady=2)
    chk_postal.grid(row=1, column=0, sticky="w", pady=2)
    chk_pga.grid(row=2, column=0, sticky="w", pady=2)

    ###Quadro para escolher o tipo de relatório (Balancete/Razão)
    quadro_tipos = tk.LabelFrame(quadro_flags, text="Tipo Documento", padx=10, pady=10)
    quadro_tipos.grid(row=0, column=1, rowspan=4, padx=(220, 0), sticky="n")

    var_balancete = tk.IntVar()
    var_razao = tk.IntVar()

    chk_balancete = tk.Checkbutton(quadro_tipos, text="Balancete", variable=var_balancete)
    chk_razao = tk.Checkbutton(quadro_tipos, text="Razão", variable=var_razao)

    chk_balancete.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    chk_razao.grid(row=1, column=0, padx=5, pady=5, sticky="w")

  
    #Frame para caminho pasta
    frame_pasta = tk.LabelFrame(frame, text='Caminho do arquivo', bd=2, relief='groove', pady=25)
    frame_pasta.grid(row=3, column=0)

    # Carrega e redimensiona a imagem
    imagem_original = Image.open(caminho_relativo("images/pasta.png"))
    imagem_redimensionada = imagem_original.resize((25, 25), Image.Resampling.LANCZOS)  #parte para ajuste do tamanho da imagem pasta
    imagem_pasta = ImageTk.PhotoImage(imagem_redimensionada)

    # Label com imagem
    lbl_pasta = tk.Label(frame_pasta, image=imagem_pasta, compound="left")
    lbl_pasta.image = imagem_pasta  # manter a referência
    lbl_pasta.grid(row=0, column=0, sticky="e", pady=(10, 0))
    entrada_pasta = tk.Entry(frame_pasta, width=60)
    entrada_pasta.grid(row=0, column=1, pady=(10, 0), sticky="w")

    def selecionar_pasta():
        pasta = filedialog.askdirectory()
        if pasta:
            entrada_pasta.delete(0, tk.END)
            entrada_pasta.insert(0, pasta)

    btn_pasta = tk.Button(frame_pasta, text="...", command=selecionar_pasta)
    btn_pasta.grid(row=0, column=2, padx=10, pady=10)

    #Função para  extrair informações para o botão gerar
    def gerar_documentos(usuario, senha):
        mes = entrada_mes.get().zfill(2)
        ano = entrada_ano.get()
        if not mes.isdigit() or not ano.isdigit():
            messagebox.showerror("Erro", "Mês e ano devem ser numéricos.")
        
        periodo_balancete = f"{mes}/{ano}"

        ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
        periodo_inicio_razao = f"01/{mes}/{ano}"
        periodo_fim_razao = f"{ultimo_dia:02}/{mes}/{ano}"

        
        planos_selecionados = []
        if var_bd.get():
            planos_selecionados.append(1)
        if var_postal.get():
            planos_selecionados.append(3)
        if var_pga.get():
            planos_selecionados.append(5)

        if not planos_selecionados:
            messagebox.showwarning("Aviso", "Selecione ao menos um plano para extrair o documento desejado.")
            return
        
        pasta_destino = entrada_pasta.get()
        if not pasta_destino:
            messagebox.showwarning("Aviso", "Selecione uma pasta de destino.")
            return
        
        if var_balancete.get():
            try:
                messagebox.showinfo("Olá", "Utilizar 'Usuário' e 'Senha' do Módulo Atena.")
                # extrair_balancete(
                #     planos=planos_selecionados,
                #     usuario=usuario,
                #     senha=senha,
                #     periodo=periodo_balancete,
                #     pasta_destino=pasta_destino
                # )
                
                messagebox.showinfo("Sucesso", "Balancete extraído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro durante a extração do balancete:\n{e}")
        
        if var_razao.get():
            messagebox.showinfo("Olá", "Utilizar 'Usuário' e 'Senha' do Módulo Atena.")
            # extrair_razao(
            #     planos=planos_selecionados,
            #     usuario=usuario,
            #     senha=senha,
            #     data_inicio=periodo_inicio_razao,
            #     data_fim=periodo_fim_razao,
            #     pasta_destino=pasta_destino
            # )
            try:
                messagebox.showinfo("Sucesso", "Razão extraído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro durante a extração do razão:\n{e}")

     # Frame Botões
    frame_botoes = tk.Frame(frame, pady=20)
    frame_botoes.grid(row=4, column=0)

    btn_exportar = tk.Button(frame_botoes, text="Extrair", width=15, command=lambda: abrir_tela_login(gerar_documentos))
    btn_exportar.grid(row=0, column=0, padx=10)

    btn_sair = tk.Button(frame_botoes, text="Sair", width=15, command=janela.destroy)
    btn_sair.grid(row=0, column=2, padx=10)

    janela.mainloop()



