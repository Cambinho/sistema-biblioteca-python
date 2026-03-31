from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCompleter,
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from datetime import date, timedelta
from controllers.usuario_controller import UsuarioController
from controllers.livro_controller import LivroController
from controllers.emprestimo_controller import EmprestimoController


class EmprestimosView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.usuario_controller = UsuarioController()
        self.livro_controller = LivroController()
        self.emprestimo_controler = EmprestimoController()

        layout = QVBoxLayout()
        layout_botoes = QHBoxLayout()
        self.tabela_emprestimos = QTableWidget()

        # Campos ComboBox
        self.selecao_usuario = QComboBox()
        self.selecao_usuario.setEditable(True)
        self.selecao_usuario.lineEdit().setPlaceholderText("Selecione um usuário")
        self.selecao_usuario.setInsertPolicy(QComboBox.NoInsert)
        self.selecao_usuario.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.carregar_usuarios()
        self.selecao_usuario.setCurrentIndex(-1)

        self.selecao_livro = QComboBox()
        self.selecao_livro.setEditable(True)
        self.selecao_livro.lineEdit().setPlaceholderText("Selecione um livro")
        self.selecao_livro.setInsertPolicy(QComboBox.NoInsert)
        self.selecao_livro.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.carregar_livros()
        self.selecao_livro.setCurrentIndex(-1)

        # Botões
        self.botao_emprestar = QPushButton("Emprestar")
        self.botao_historico = QPushButton("Histórico")
        self.botao_devolver = QPushButton("Devolver")
        self.botao_devolver.setEnabled(False)
        self.botao_ver_disponibilidade = QPushButton("Ver Disponibilidade")
        self.botao_emprestimos_ativos = QPushButton("Empréstimos Ativos")
        self.botao_atualizar_tabela = QPushButton("Atualizar Tabela")
        self.botao_voltar = QPushButton("Voltar")

        # Adicionar botões ao layout dos botões
        layout_botoes.addWidget(self.botao_emprestar)
        layout_botoes.addWidget(self.botao_historico)
        layout_botoes.addWidget(self.botao_devolver)
        layout_botoes.addWidget(self.botao_ver_disponibilidade)
        layout_botoes.addWidget(self.botao_emprestimos_ativos)
        layout_botoes.addWidget(self.botao_atualizar_tabela)
        layout_botoes.addWidget(self.botao_voltar)

        # Adicionar layouts ao layout principal
        layout.addWidget(self.selecao_usuario)
        layout.addWidget(self.selecao_livro)
        layout.addWidget(self.tabela_emprestimos)
        layout.addLayout(layout_botoes)

        # Passando o layout para a instância
        self.setLayout(layout)
        self.carregar()
        self.conectar_botoes()
        self.selecao_usuario.currentTextChanged.connect(self.recarregar_tabela)
        self.selecao_livro.currentTextChanged.connect(self.recarregar_tabela)

    def conectar_botoes(self):
        self.botao_emprestar.clicked.connect(self.emprestar)
        self.botao_historico.clicked.connect(self.listar_historico)
        self.botao_devolver.clicked.connect(self.devolver)
        self.botao_ver_disponibilidade.clicked.connect(self.verificar_disponibilidade)
        self.botao_emprestimos_ativos.clicked.connect(self.listar_emprestimos_ativos)
        self.botao_atualizar_tabela.clicked.connect(self.recarregar)
        self.botao_voltar.clicked.connect(self.voltar_janela)

        self.tabela_emprestimos.itemSelectionChanged.connect(self.habilitar_devolucao)
        self.selecao_usuario.activated.connect(self.atualizar_botoes)
        self.selecao_livro.activated.connect(self.atualizar_botoes)
        
        self.atualizar_botoes()

    def atualizar_botoes(self):
        usuario = self.selecao_usuario.currentText()
        livro = self.selecao_livro.currentText()
        if usuario != "" and livro != "":
            self.botao_emprestar.setEnabled(True)
        else:
            self.botao_emprestar.setEnabled(False)

        if usuario != "" and livro == "" or usuario == "" and livro != "":
            self.botao_historico.setEnabled(True)
        else:
            self.botao_historico.setEnabled(False)
        
        if livro != "" and usuario == "":
            self.botao_ver_disponibilidade.setEnabled(True)
        else:
            self.botao_ver_disponibilidade.setEnabled(False)

    def habilitar_devolucao(self):
        linha_atual = self.tabela_emprestimos.currentRow()
        status = self.tabela_emprestimos.item(linha_atual, 6).text()
        if status == "ativo":
            self.botao_devolver.setEnabled(True)
        else:
            self.botao_devolver.setEnabled(False)

    def recarregar_tabela(self):
        usuario = self.selecao_usuario.currentText()
        livro = self.selecao_livro.currentText()
        self.botao_emprestar.setEnabled(False)
        self.botao_historico.setEnabled(False)
        self.botao_ver_disponibilidade.setEnabled(False)
        
        if usuario == "" and livro == "":
            self.carregar()
    
    def recarregar(self):
        self.carregar()

    def carregar(self, dados = 1):
        if dados == 1:
            dados = self.emprestimo_controler.listar()

        self.tabela_emprestimos.setRowCount(len(dados))
        self.tabela_emprestimos.setColumnCount(7)
        self.tabela_emprestimos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_emprestimos.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabela_emprestimos.setSortingEnabled(True)
        self.tabela_emprestimos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabela_emprestimos.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabela_emprestimos.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela_emprestimos.setHorizontalHeaderLabels(
            ["ID", "Usuário", "Livro", "Data de Empréstimo", "Devolução Prevista", "Data de Devolução", "Status"]
        )

        for linha, registro in enumerate(dados):
            for col, valor in enumerate(registro):
                self.tabela_emprestimos.setItem(linha, col, QTableWidgetItem(str(valor)))
    
    def carregar_usuarios(self):
        """Carrega lista de usuários no ComboBox"""
        dados = self.usuario_controller.listar()

        self.selecao_usuario.clear()
        for usuario in dados:
            id_usuario = usuario[0]
            nome = usuario[1]
            self.selecao_usuario.addItem(nome, id_usuario)

    def carregar_livros(self):
        """Carrega lista de livros no ComboBox"""
        dados = self.livro_controller.listar()

        self.selecao_livro.clear()
        for livro in dados:
            id_livro = livro[0]
            nome = livro[1]
            self.selecao_livro.addItem(nome, id_livro)

    def emprestar(self):
        disponibilidade = self.verificar_disponibilidade()
        if disponibilidade:
            nome_usuario = self.selecao_usuario.currentText()
            informacoes_usuario = self.usuario_controller.buscar(nome_usuario)
            id_usuario = informacoes_usuario[0][0]

            nome_livro = self.selecao_livro.currentText()
            informacoes_livro = self.livro_controller.buscar(nome_livro, "titulo")
            id_livro = informacoes_livro[0][0]
            
            data_emprestimo = date.today()
            data_devolucao_prevista = data_emprestimo + timedelta(days=7)
            data_devolucao_real = None
            status = "ativo"

            ok, msg = self.emprestimo_controler.realizar_emprestimo(id_usuario, id_livro, data_emprestimo,
                data_devolucao_prevista, data_devolucao_real, status)
            
            if ok:
                QMessageBox.information(self, "Sucesso", msg)
                self.livro_controller.atualizar(id_livro, informacoes_livro[0][1], informacoes_livro[0][2],
                informacoes_livro[0][3], informacoes_livro[0][4], informacoes_livro[0][5], informacoes_livro[0][6]-1)
                self.carregar()
                self.limpar_campos()
                self.atualizar_botoes()
            else:
                QMessageBox.warning(self, "Erro", msg)

    def devolver(self):
        linha_atual = self.tabela_emprestimos.currentRow()
        id = self.tabela_emprestimos.item(linha_atual, 0).text()
        nome_livro = self.tabela_emprestimos.item(linha_atual, 2).text()
        informacoes_livro = self.livro_controller.buscar(nome_livro, "titulo")
        data_devolucao = date.today()
        
        ok, msg = self.emprestimo_controler.registrar_devolucao(id, data_devolucao)

        if ok:
            QMessageBox.information(self, "Sucesso", msg)
            self.livro_controller.atualizar(informacoes_livro[0][0], informacoes_livro[0][1], informacoes_livro[0][2],
            informacoes_livro[0][3], informacoes_livro[0][4], informacoes_livro[0][5], informacoes_livro[0][6]+1)
            self.carregar()
            self.limpar_campos()
            self.atualizar_botoes()
            self.botao_devolver.setEnabled(False)
        else:
            QMessageBox.warning(self, "Erro", msg)

    def listar_historico(self):
        usuario = self.selecao_usuario.currentText()
        livro = self.selecao_livro.currentText()

        if usuario != "" and livro == "":
            informacoes_usuario = self.usuario_controller.buscar(usuario)
            id_usuario = informacoes_usuario[0][0]
            coluna = "usuario_id"
            dados = self.emprestimo_controler.listar_historico_ou_emprestimos_ativos(id_usuario, coluna)
            self.carregar(dados)

        elif usuario == "" and livro != "":
            informacoes_livro = self.livro_controller.buscar(livro)
            id_livro = informacoes_livro[0][0]
            coluna = "livro_id"
            dados = self.emprestimo_controler.listar_historico_ou_emprestimos_ativos(id_livro, coluna)
            self.carregar(dados)
        self.atualizar_botoes()
    
    def verificar_disponibilidade(self):
        livro = self.selecao_livro.currentText()
        informacoes_livro = self.livro_controller.buscar(livro)
        quantidade = informacoes_livro[0][6]
        if quantidade > 0:
            QMessageBox.information(self, "Disponível", f"O livro {livro} está disponível! {quantidade} unidades disponíveis.")
            return True
        else:
            QMessageBox.information(self, "Indisponível", f"O livro {livro} está indisponível.")

    def limpar_campos(self):
        self.selecao_usuario.setCurrentIndex(-1)
        self.selecao_livro.setCurrentIndex(-1)
        
    def listar_emprestimos_ativos(self):
        parametro = "ativo"
        coluna = "status"
        dados = self.emprestimo_controler.listar_historico_ou_emprestimos_ativos(parametro, coluna)

        self.carregar(dados)

    def voltar_janela(self):
        self.limpar_campos()
        self.tabela_emprestimos.clearSelection()
        self.carregar()
        self.atualizar_botoes()
        self.botao_devolver.setEnabled(False)
        self.stacked_widget.setCurrentIndex(0) # Muda para a janela principal