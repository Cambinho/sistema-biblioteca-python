from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow,
    QStackedWidget, QHBoxLayout
)
from PySide6.QtCore import Qt
from views.usuarios_view import UsuariosView
from views.livros_view import LivrosView
from views.emprestimos_view import EmprestimosView
from views.dashboard_view import DashboardView




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Projeto - Gerenciamento de Biblioteca")
        
        # 1. Criar o QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.resize(500, 500)
        cor = "#6BBD44"

        estizacao ="""
            QLineEdit {
            background-color: yellow;
            color: blue;
            }
            QTableWidget {
            background-color: lightgrey;
            }
            QTableWidget::item:hover {
            background-color: lightblue;
            }
            QTableWidget::item:selected {
                background-color: #d9fffb;  
                color: #000000;             
            }
            QPushButton {
            background-color: #DD3000;                   
            }
            QPushButton:hover {
            background-color: #FFD700;
            border: 1px solid orange;
            }
            QPushButton:pressed {
            background-color: #C0270F;
            }"""
        
        estizacao_pagina_inicial = """
            QPushButton {
            background-color: #DD3000;
            min-width: 200px;
            max-width: 200px;
            min-height: 200px;
            max-height: 200px;
            border-radius: 100px;
            font-size: 30px;
            }
            QPushButton:hover {
            background-color: #FFD700;
            border: 1px solid orange;
            }
            QPushButton:pressed {
            background-color: #C0270F;
            }"""

        self.setStyleSheet(f"""
            background-color: {cor};
            """)
        
        # Criando a página inicial e as telas, estilizando todas
        self.pagina_inicial = QWidget()
        self.pagina_inicial.setStyleSheet(estizacao_pagina_inicial)
        self.tela_usuario = UsuariosView(self.stacked_widget)
        self.tela_usuario.setStyleSheet(estizacao)
        self.tela_livros = LivrosView(self.stacked_widget)
        self.tela_livros.setStyleSheet(estizacao)
        self.tela_emprestimos = EmprestimosView(self.stacked_widget)
        self.tela_emprestimos.setStyleSheet(estizacao)
        self.tela_dashboard = DashboardView(self.stacked_widget)
        self.tela_dashboard.setStyleSheet(estizacao)

        layout_inicial = QVBoxLayout()

        label = QLabel("""Biblioteca 
Natalina
""")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            font-family: Helvetica;
            font-size: 48pt; color: #FFC500;  
            padding-bottom: 150px;
            """)


        # Criando os botões para direcionar o usuário
        self.botao_usuario = QPushButton("Usuários")
        self.botao_usuario.clicked.connect(lambda: self.tela_selecionada(1))
        self.botao_livros = QPushButton("Livros")
        self.botao_livros.clicked.connect(lambda: self.tela_selecionada(2))
        self.botao_emprestimos = QPushButton("Empréstimos")
        self.botao_emprestimos.clicked.connect(lambda: self.tela_selecionada(3))
        self.botao_dashboard = QPushButton("Dashboard")
        self.botao_dashboard.clicked.connect(lambda: self.tela_selecionada(4))

        # Adicionando os botões ao layout_botoes
        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.botao_usuario)
        layout_botoes.addWidget(self.botao_livros)
        layout_botoes.addWidget(self.botao_emprestimos)
        layout_botoes.addWidget(self.botao_dashboard)
        # Montando o layout da página e setando ele a página inicial
        layout_inicial.addWidget(label)
        layout_inicial.addLayout(layout_botoes)
        self.pagina_inicial.setLayout(layout_inicial)
        # Adicionando as telas para navegação no stacked_widget
        self.stacked_widget.addWidget(self.pagina_inicial)
        self.stacked_widget.addWidget(self.tela_usuario)
        self.stacked_widget.addWidget(self.tela_livros)
        self.stacked_widget.addWidget(self.tela_emprestimos)
        self.stacked_widget.addWidget(self.tela_dashboard)


    def tela_selecionada(self, a):
        self.stacked_widget.setCurrentIndex(a) # Muda para a tela de acordo com o botão apertado

    

 