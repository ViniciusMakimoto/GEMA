
import tkinter as tk
from tkinter import ttk

from services.equipamentosService import EquipamentosService

MAIN_BACKGROUND_COLOR = "#252F60"
LATERAL_MENU_COLOR = "#353F6E"

class AbaEquipamentos:
    def __init__(self, areaPrincipal):

        self.mainFrame = tk.Frame(areaPrincipal, bg=MAIN_BACKGROUND_COLOR)
        
        self.filtroFrame = tk.Frame(self.mainFrame, height=125, bg=MAIN_BACKGROUND_COLOR)
        self.filtroFrame.pack(side="top", fill="x")
        self.criarFiltros()
        
        self.tabelaFrame = tk.Frame(self.mainFrame, bg=MAIN_BACKGROUND_COLOR)
        self.tabelaFrame.pack(side="bottom", expand=True, fill="both")
        
        self.criarTabela()

        self.equipamentosService = EquipamentosService()
        self.atualizarTabela(self.equipamentosService.obterTodosEquipamentos())

    def criarFiltros(self):

        self.statusLabel = tk.Label(self.filtroFrame, text="Status:",  height=7, bg=MAIN_BACKGROUND_COLOR, fg="white")
        self.statusLabel.pack(side="left", padx=10, pady=10)

        self.statusComboBox = ttk.Combobox(self.filtroFrame, state= "readonly", values=["Todos", "Disponível", "Manutenção"])
        self.statusComboBox.current(0)
        self.statusComboBox.pack(side="left", padx=10, pady=10)

        self.pesquisaLabel = tk.Label(self.filtroFrame, text="Pesquisar (id):", bg=MAIN_BACKGROUND_COLOR, fg="white")
        self.pesquisaLabel.pack(side="left", padx=10, pady=10)

        self.pesquisaEntry = tk.Entry(self.filtroFrame)
        self.pesquisaEntry.pack(side="left", padx=10, pady=10)

        self.aplicarFiltroButton = tk.Button(self.filtroFrame, text="Aplicar Filtro", command=self.onAplicarFiltro)
        self.aplicarFiltroButton.pack(side="left", padx=10, pady=10)

    def onAplicarFiltro(self):
        todosEquipamentos = self.equipamentosService.obterTodosEquipamentos()
        statusSelecionado = self.statusComboBox.get()
        pesquisaTexto = self.pesquisaEntry.get().strip()

        if statusSelecionado == "Todos":
            filtroStatus = todosEquipamentos
        else:
            filtroStatus = [equip for equip in todosEquipamentos if equip[5] == statusSelecionado]
        
        if pesquisaTexto == "":
            filtroPesquisa = filtroStatus
        else:
            filtroPesquisa = [equip for equip in filtroStatus if pesquisaTexto.lower() in str(equip[0]).lower()]

        self.atualizarTabela(filtroPesquisa)

    def criarTabela(self):
        # Exemplo de criação de tabela usando Treeview
        self.tabela = ttk.Treeview(self.tabelaFrame, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")
        self.tabela.heading("col1", text="ID")
        self.tabela.heading("col2", text="Serial Number")
        self.tabela.heading("col3", text="Marca")
        self.tabela.heading("col4", text="Modelo")
        self.tabela.heading("col5", text="Observações")
        self.tabela.heading("col6", text="Status")
        self.tabela.pack(expand=True, fill='both')

    def atualizarTabela(self, dados):

        # Limpa a tabela existente
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        # Adiciona novos dados à tabela
        for linha in dados:
            self.tabela.insert("", tk.END, values=linha)