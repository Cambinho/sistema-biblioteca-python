from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QHeaderView,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QFormLayout
)
from controllers.livro_controller import LivroController


class LivrosView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.controller = LivroController()

        layout = QVBoxLayout()
        layout_cadastro = QFormLayout()
        layout_botoes = QHBoxLayout()
        self.tabela_livros = QTableWidget()

        # Campos do formulário
        self.titulo = QLineEdit()
        self.titulo.setPlaceholderText("Título do livro")
        self.autor = QLineEdit()
        self.autor.setPlaceholderText("Autor do livro")
        self.isbn = QLineEdit()
        self.isbn.setPlaceholderText("Código ISBN")
        self.ano_publicacao = QLineEdit()
        self.ano_publicacao.setPlaceholderText("Ex: 2025")
        self.quantidade = QLineEdit()
        self.quantidade.setPlaceholderText("Quantidade total no acervo")

        # Adicionar campos ao layout do formulário
        layout_cadastro.addRow("Título:", self.titulo)
        layout_cadastro.addRow("Autor:", self.autor)
        layout_cadastro.addRow("ISBN:", self.isbn)
        layout_cadastro.addRow("Ano de Publicação:", self.ano_publicacao)
        layout_cadastro.addRow("Quantidade:", self.quantidade)

        # Botões
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_editar = QPushButton("Editar")
        self.botao_atualizar = QPushButton("Atualizar Livro")
        self.botao_atualizar.setVisible(False)
        self.botao_excluir = QPushButton("Excluir")
        self.botao_buscar = QPushButton("Buscar")
        self.botao_atualizar_tabela = QPushButton("Atualizar Tabela")
        self.botao_voltar = QPushButton("Voltar")

        # Adicionar botões ao layout dos botões
        layout_botoes.addWidget(self.botao_adicionar)
        layout_botoes.addWidget(self.botao_editar)
        layout_botoes.addWidget(self.botao_excluir)
        layout_botoes.addWidget(self.botao_buscar)
        layout_botoes.addWidget(self.botao_atualizar_tabela)
        layout_botoes.addWidget(self.botao_voltar)

        # Adicionar layouts ao layout principal
        layout.addLayout(layout_cadastro)
        layout.addWidget(self.botao_atualizar)
        layout.addWidget(self.tabela_livros)
        layout.addLayout(layout_botoes)

        # Passando o layout para a instância
        self.setLayout(layout)
        self.carregar()
        self.conectar_botoes()

    def conectar_botoes(self):
        self.botao_adicionar.clicked.connect(self.cadastrar_livro)
        self.botao_buscar.clicked.connect(self.buscar_livro)
        self.botao_editar.clicked.connect(self.editar_livro)
        self.botao_atualizar.clicked.connect(self.atualizar_livro)
        self.botao_excluir.clicked.connect(self.excluir_livro)
        self.botao_atualizar_tabela.clicked.connect(self.recarregar)
        self.botao_voltar.clicked.connect(self.voltar_janela)

        self.tabela_livros.itemSelectionChanged.connect(self.atualizar_botoes)
        self.titulo.textChanged.connect(self.habilitar_busca)
        self.atualizar_botoes()
        self.habilitar_busca()

    def atualizar_botoes(self):
        tem_selecao = self.tabela_livros.currentRow() >= 0
        self.botao_editar.setEnabled(tem_selecao)
        self.botao_excluir.setEnabled(tem_selecao)

    def habilitar_busca(self):
        habilitador = self.titulo.text()
        if habilitador != "":
            self.botao_buscar.setEnabled(True)
        else:
            self.botao_buscar.setEnabled(False)
            self.carregar()

    def carregar(self, dados = 1):
        if dados == 1 or False:
            dados = self.controller.listar()

        self.tabela_livros.setRowCount(len(dados))
        self.tabela_livros.setColumnCount(7)
        self.tabela_livros.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_livros.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabela_livros.setSortingEnabled(True)
        self.tabela_livros.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabela_livros.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabela_livros.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela_livros.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.tabela_livros.setHorizontalHeaderLabels(
            ["ID", "Título", "Autor", "ISBN", "Ano de Publicação", "Total no Acervo", "Total Disponível"]
        )

        for linha, registro in enumerate(dados):
            for col, valor in enumerate(registro):
                self.tabela_livros.setItem(linha, col, QTableWidgetItem(str(valor)))
    
    def recarregar(self):
        self.carregar()
    
    def cadastrar_livro(self):
        titulo = self.titulo.text()
        autor = self.autor.text()
        isbn = self.isbn.text()
        ano_publicacao = self.ano_publicacao.text()
        quantidade_total = self.quantidade.text()
        quantidade_disponivel = int(quantidade_total)

        ok, msg = self.controller.cadastrar(titulo, autor, isbn, int(ano_publicacao), int(quantidade_total), quantidade_disponivel)

        if ok:
            QMessageBox.information(self, "Sucesso", msg)
            self.limpar_campos()
            self.carregar()
        else:
            QMessageBox.warning(self, "Erro", msg)
    
    def editar_livro(self):
        linha_atual = self.tabela_livros.currentRow()
        if linha_atual < 0:
            return
        
        self.titulo.setText(self.tabela_livros.item(linha_atual, 1).text())
        self.autor.setText(self.tabela_livros.item(linha_atual, 2).text())
        self.isbn.setText(self.tabela_livros.item(linha_atual, 3).text())
        self.ano_publicacao.setText(self.tabela_livros.item(linha_atual, 4).text())
        self.quantidade.setText(self.tabela_livros.item(linha_atual, 5).text())

        self.botao_atualizar.setVisible(True)
        self.botao_editar.setEnabled(False)
        self.botao_excluir.setEnabled(False)

    def atualizar_livro(self):
        linha_atual = self.tabela_livros.currentRow()
        id = self.tabela_livros.item(linha_atual, 0).text()
        titulo = self.titulo.text()
        autor = self.autor.text()
        isbn = self.isbn.text()
        ano_publicacao = self.ano_publicacao.text()
        quantidade_total = self.quantidade.text()
        livros_emprestados = self.controller.livros_emprestados(int(id))
        quantidade_disponivel = int(quantidade_total) - len(livros_emprestados)

        ok, msg = self.controller.atualizar(int(id), titulo, autor, isbn, int(ano_publicacao), int(quantidade_total), quantidade_disponivel)
        
        if ok:
            QMessageBox.information(self, "Sucesso", msg)
        else:
            QMessageBox.warning(self, "Erro", msg)
            return

        self.tabela_livros.clearSelection()
        self.botao_editar.setEnabled(False)
        self.botao_excluir.setEnabled(False)
        self.botao_atualizar.setVisible(False)
        self.limpar_campos()
        self.carregar()

    def excluir_livro(self):
        linha_atual = self.tabela_livros.currentRow()
        if linha_atual < 0:
            return
        
        id = self.tabela_livros.item(linha_atual, 0).text()
        titulo = self.tabela_livros.item(linha_atual, 1).text()
        isbn = self.tabela_livros.item(linha_atual, 3).text()
        
        # Pede confirmação
        resposta = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja excluir o livro '{titulo}' (ID: {id}, ISBN: {isbn})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            # Chama a função de exclusão no banco de dados
            sucesso = self.controller.excluir(id)
            
            if sucesso:
                # Recarrega a tabela
                self.carregar()
                self.botao_editar.setEnabled(False)
                self.botao_excluir.setEnabled(False)

                QMessageBox.information(self, "Sucesso", "Livro excluído!")
            else:
                QMessageBox.critical(self, "Erro", "Falha ao excluir livro no banco de dados.")
    
    def buscar_livro(self):
        parametro = self.titulo.text()
        coluna = "titulo"
        dados = self.controller.buscar(parametro, coluna)
        self.carregar(dados)

    def limpar_campos(self):
        self.titulo.clear()
        self.autor.clear()
        self.isbn.clear()
        self.ano_publicacao.clear()
        self.quantidade.clear()

    def voltar_janela(self):
        self.limpar_campos()
        self.carregar()
        self.tabela_livros.clearSelection()
        self.botao_editar.setEnabled(False)
        self.botao_excluir.setEnabled(False)
        self.botao_atualizar.setVisible(False)
        self.stacked_widget.setCurrentIndex(0) # Muda para a janela principal