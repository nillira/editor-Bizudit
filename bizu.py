from tkinter import *
from tkinter import filedialog as FileDialog
from tkinter import messagebox as MessageBox
import tkinter.font as tkFont
import tkinter as tk
from reportlab.pdfgen import canvas
from PyQt5 import  uic,QtWidgets
import pyttsx3

caminho = ""

#Funções de arquivo
def novo_arquivo():
    global caminho #para acessar esta variável de qualquer lugar
    mensagem.set("Novo arquivo")
    caminho = ""
    texto.delete(1.0, "end")
    base.title(caminho + "- BizuDit")

#Funções de abrir arquivo
def abrir_arquivo():
    global caminho
    mensagem.set("Abrir fichero")
    caminho = FileDialog.askopenfilename(initialdir=".", filetypes=(("Arquivos de texto", "*.txt"),),title="Abrir um arquivo de texto")

    if caminho != "":
        arquivo = open(caminho,"r")
        conteudo_abrir = arquivo.read()
        texto.delete(1.0,"end")
        texto.insert("insert", conteudo_abrir)
        arquivo.close()
        base.title(caminho + " - BizuDit")

def salvar_arquivo():
    mensagem.set("Salvar Arquivo")
    if caminho != "":
        conteudo_salvar = texto.get(1.0, "end-1c")
        Arquivo = open(caminho, "w+")
        Arquivo.write(conteudo_salvar)
        Arquivo.close()
        mensagem.set("Arquivo salvo com sucesso!")
    else:
        salvar_arquivo_como()

def salvar_arquivo_como():
    global caminho
    mensagem.set("Salvar Arquivo como")
    arquivo_salvar_como = FileDialog.asksaveasfile(title="Salvar Arquivo", mode="w", defaultextension=".txt")
    if arquivo_salvar_como is not None:
        caminho = arquivo_salvar_como.name
        conteudo = texto.get(1.0, "end-1c")
        arquivo_salvar_como = open(caminho, "w")
        arquivo_salvar_como.write(conteudo)
        arquivo_salvar_como.close()
        mensagem.set("Arquivo salvo com sucesso!")
    else:
        mensagem.set("Arquivo cancelado!")
        caminho = ""

#Funções contar palavras
def Contador_de_palavras():
    root = tk.Tk()
    root.geometry("400x240")
    root.title('Contador de Palavras')
    contador_frenq = texto.get(1.0, "end-1c") #problema está nesse negocio de  "end-1c"
    

    def getTextInput():
        result=textExample.get("1.0", "end-1c")
        print(result)
        mensagem.set(str(result)+' apareceu: '+str(contador_frenq.count(str(result)))+' vezes') # usei esse comando para escrever numero lá em baixo

    textExample=tk.Text(root, height=10)
    textExample.pack()
    btnRead=tk.Button(root, height=1, width=10, text="Read",command=getTextInput)
    
    btnRead.pack()

    root.mainloop()
    
#modo escuro, bg fundo e foregraound cor da letra        
def modo_escuro():
    base.configure(bg='black')
    texto.configure(bg='black', foreground='white')

# falta ajeitar essa parte   
def gerador_pdf():
    conteudo_pdf = texto.get(1.0, "end-1c")
    nome = FileDialog.asksaveasfile(title="Salvar Arquivo", mode="w", defaultextension=".txt")
    c = canvas.Canvas("arquivo.pdf")
    c.drawString(100,750,conteudo_pdf)
    c.save()
    
def gerador_audio():
    engine = pyttsx3.init()
    conteudo_audio = texto.get(1.0, "end-1c")
    engine.say(conteudo_audio)
    engine.runAndWait()
    mensagem.set("reproduzido com sucesso!")

#Editar
def cortar():
    texto.event_generate("<<Cut>>")
def Selecionar_tudo():
    texto.event_generate("<<SelectAll>>")
def copiar():
    texto.event_generate("<<Copy>>")
def colar():
    texto.event_generate("<<Paste>>")
#Ayuda
def acercaDe():
    MessageBox.showinfo("Sobre" , "BizuDit 2.0\n---- Contato ----\n bizuteam@gmail.com")

base = Tk()

base.title("BizuDit 2.0")
base.geometry('500x500') #tamanho
base.resizable(1,1) #controle de dimensão: em boolean
base.iconbitmap("")

#Menu cima
menubar = Menu(base)
menu_pricipal = Menu(menubar, tearoff=0)
menu_ferramentas = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)
menu_export = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)
menu_leitura = Menu(menubar, tearoff=0)

#Arquivo
menu_pricipal.add_command(label="Novo",activebackground="blue",  command=novo_arquivo)
menu_pricipal.add_command(label="Abrir", activebackground="blue", command=abrir_arquivo)
menu_pricipal.add_command(label="Salvar Arquivo", activebackground="blue", command=salvar_arquivo)
menu_pricipal.add_command(label="Salvar como", activebackground="blue", command=salvar_arquivo_como)
menu_pricipal.add_separator()
menu_pricipal.add_command(label="Sair", activebackground="black", command=base.quit)
menubar.add_cascade(menu=menu_pricipal, label="Menu")

#menu ferramentas
menu_ferramentas.add_command(label="Contador de Palavras", activebackground="orange", command=Contador_de_palavras)
#menu_ferramentas.add_command(label="Trocar Palavras", activebackground="orange", command=trocar_Palavras)
menu_ferramentas.add_command(label="Modo escuro", activebackground="black", command=modo_escuro)
menubar.add_cascade(menu=menu_ferramentas, label="Ferramentas")

#Editar
editmenu.add_command(label="Copiar                      (Ctrl+C)", command=copiar)
editmenu.add_command(label="colar                       (Ctrl+V)", command=colar)
editmenu.add_command(label="Selecionar tudo       (Ctrl+shift+A)", command=Selecionar_tudo)
editmenu.add_command(label='Cortar                      (ctrl+X)', command=cortar)

menubar.add_cascade(label="Editar", menu=editmenu)

#pdf
menu_export.add_command(label="Salvar como PDF", activebackground="red", command=gerador_pdf)
menubar.add_cascade(menu=menu_export, label="Exportar para PDF")

#leitura
menu_leitura.add_command(label="Reproduzir", activebackground="red", command=gerador_audio)
menubar.add_cascade(menu=menu_leitura, label="Reproduzir texto")

#Ajuda
helpmenu.add_command(label="Help", command=acercaDe)
menubar.add_cascade(label="Sobre", menu=helpmenu)

#Caixa de texto central
texto = Text(base)
texto.pack(fill="both", expand=1)
texto.config(bd=0, padx=6, pady=4, font=("Consolas", 12))

#Monitor inferior
mensagem = StringVar()
mensagem.set("Bizu Team")
tela = Label(base, textvar=mensagem, justify="left")
tela.pack(side="left")

#Chamada de menu
base.config(menu=menubar)

saudacao = pyttsx3.init()
saudacao.say("Bem vindo ao Bizu dit 2.0  seu editor de texto.")
saudacao.runAndWait()

base.mainloop()
