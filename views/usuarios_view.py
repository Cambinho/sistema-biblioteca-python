from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from datetime import datetime
from controllers.usuario_controller import UsuarioController
from utils import validadores


class UsuariosView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.controller = UsuarioController()


        layout = QVBoxLayout()

        self.nome_usuario = QLineEdit()
        self.nome_usuario.setPlaceholderText("Seu Nome")
        self.email_usuario = QLineEdit()
        self.email_usuario.setPlaceholderText("exemplo@exemplo.com")
        self.telefone_usuario = QLineEdit()
        self.telefone_usuario.setInputMask("(99)99999-9999")

        layout_botoes = QHBoxLayout()
        layout_intermediario = QHBoxLayout()

        self.botao_buscar = QPushButton("Buscar")
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_editar = QPushButton("Editar")
        self.botao_atualizar = QPushButton("Atualizar Usuário")
        self.botao_atualizar.setVisible(False)
        self.botao_excluir = QPushButton("Excluir")
        self.botao_voltar = QPushButton("Voltar")

        layout_botoes.addWidget(self.botao_adicionar)
        layout_botoes.addWidget(self.botao_editar)
        layout_botoes.addWidget(self.botao_excluir)
        layout_botoes.addWidget(self.botao_voltar)

        layout_intermediario.addWidget(QLabel("Nome:"))
        layout_intermediario.addWidget(self.nome_usuario)
        layout_intermediario.addWidget(self.botao_buscar)

        self.tabela_usuarios = QTableWidget()

        layout.addLayout(layout_intermediario)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_usuario)
        layout.addWidget(QLabel("Telefone:"))
        layout.addWidget(self.telefone_usuario)
        layout.addWidget(self.botao_atualizar)
        layout.addWidget(self.tabela_usuarios)
        layout.addLayout(layout_botoes)

        self.setLayout(layout)
        self.carregar()
        self.conectar_botoes()


    def conectar_botoes(self):
        self.botao_adicionar.clicked.connect(self.cadastrar_usuario)
        self.botao_buscar.clicked.connect(self.buscar_usuario)
        self.botao_editar.clicked.connect(self.editar_usuario)
        self.botao_atualizar.clicked.connect(self.atualizar_usuario)
        self.botao_excluir.clicked.connect(self.excluir_usuario)
        self.botao_voltar.clicked.connect(self.voltar_janela)

        self.tabela_usuarios.itemSelectionChanged.connect(self.atualizar_botoes)
        self.nome_usuario.textChanged.connect(self.habilitar_busca)
        self.atualizar_botoes()
        self.habilitar_busca()

    def atualizar_botoes(self):
        tem_selecao = self.tabela_usuarios.currentRow() >= 0
        self.botao_editar.setEnabled(tem_selecao)
        self.botao_excluir.setEnabled(tem_selecao)

    def habilitar_busca(self):
        habilitador = self.nome_usuario.text()
        if habilitador != "":
            self.botao_buscar.setEnabled(True)
        else:
            self.botao_buscar.setEnabled(False)
            self.carregar()

    def carregar(self, dados = 1):
        if dados == 1:
            dados = self.controller.listar()

        self.tabela_usuarios.setRowCount(len(dados))
        self.tabela_usuarios.setColumnCount(5)
        self.tabela_usuarios.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_usuarios.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabela_usuarios.setSortingEnabled(True)
        self.tabela_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabela_usuarios.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabela_usuarios.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela_usuarios.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.tabela_usuarios.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.tabela_usuarios.setHorizontalHeaderLabels(
            ["ID", "Nome", "Email", "Telefone", "Data de Cadastro"]
        )

        for linha, registro in enumerate(dados):
            for col, valor in enumerate(registro):
                self.tabela_usuarios.setItem(linha, col, QTableWidgetItem(str(valor)))

    def cadastrar_usuario(self):
        nome = self.nome_usuario.text()
        email = self.email_usuario.text()
        telefone_campo = self.telefone_usuario.text()
        data_atual = datetime.now()
        data_cadastro = data_atual.strftime("%Y-%m-%d %H:%M:%S")

        resultado = validadores.validar_email(email)
        if resultado:
            ok, msg = self.controller.cadastrar(nome, email, telefone_campo, data_cadastro)
        else:
            QMessageBox.warning(self, "Email inválido", "Confira seu endereço de email. Formato inválido.")
            return

        if ok:
            QMessageBox.information(self, "Sucesso", msg)
            self.limpar_campos()
            self.carregar()
        else:
            QMessageBox.warning(self, "Erro", msg)
    
    def editar_usuario(self):
        linha_atual = self.tabela_usuarios.currentRow()
        if linha_atual < 0:
            return
        
        self.nome_usuario.setText(self.tabela_usuarios.item(linha_atual, 1).text())
        self.email_usuario.setText(self.tabela_usuarios.item(linha_atual, 2).text())
        self.telefone_usuario.setText(self.tabela_usuarios.item(linha_atual, 3).text())

        self.botao_atualizar.setVisible(True)
        self.botao_editar.setEnabled(False)
        self.botao_excluir.setEnabled(False)
   
    def atualizar_usuario(self):
        linha_atual = self.tabela_usuarios.currentRow()
        id = self.tabela_usuarios.item(linha_atual, 0).text()
        nome = self.nome_usuario.text()
        email = self.email_usuario.text()
        telefone_campo = self.telefone_usuario.text()

        resultado = validadores.validar_email(email)
        if resultado:
            ok, msg = self.controller.atualizar(int(id), nome, email, telefone_campo)
        else:
            QMessageBox.warning(self, "Email inválido", "Confira seu endereço de email. Formato inválido.")
            return
        
        if ok:
            QMessageBox.information(self, "Sucesso", msg)
        else:
            QMessageBox.warning(self, "Erro", msg)
            return


        self.tabela_usuarios.clearSelection()
        self.botao_editar.setEnabled(False)
        self.botao_excluir.setEnabled(False)
        self.botao_atualizar.setVisible(False)
        self.limpar_campos()
        self.carregar()

    def excluir_usuario(self):
        linha_atual = self.tabela_usuarios.currentRow()
        if linha_atual < 0:
            return
        
        id = self.tabela_usuarios.item(linha_atual, 0).text()
        nome = self.tabela_usuarios.item(linha_atual, 1).text()
        
        # Pede confirmação
        resposta = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja excluir o usuário '{nome}' (ID: {id})?",
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
                QMessageBox.information(self, "Sucesso", "Usuário excluído!")
            else:
                QMessageBox.critical(self, "Erro", "Falha ao excluir usuário no banco de dados.")
    
    def buscar_usuario(self):
        parametro = self.nome_usuario.text()
        dados = self.controller.buscar(parametro)
        self.carregar(dados)

    def limpar_campos(self):
        self.nome_usuario.clear()
        self.email_usuario.clear()
        self.telefone_usuario.clear()

    def voltar_janela(self):
        self.limpar_campos()
        self.carregar()
        self.tabela_usuarios.clearSelection()
        self.botao_editar.setEnabled(False)
        self.botao_excluir.setEnabled(False)
        self.botao_atualizar.setVisible(False)
        self.stacked_widget.setCurrentIndex(0) # Muda para a janela principal