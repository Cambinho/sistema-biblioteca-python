from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFormLayout,
    QHBoxLayout, QLineEdit
)
from controllers.livro_controller import LivroController
from controllers.usuario_controller import UsuarioController
from controllers.emprestimo_controller import EmprestimoController

class DashboardView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.usuario_controller = UsuarioController()
        self.emprestimo_controller = EmprestimoController()
        self.livro_controller = LivroController()

        layout = QVBoxLayout()
        layout_dados = QFormLayout()
        layout_botoes = QHBoxLayout()



        label_filtro = QLabel("Filtro de dados:")
        self.selecao_data = QComboBox()
        self.selecao_data.setPlaceholderText("Selecione um intervalo de tempo")
        self.carregar_filtro()
        self.selecao_data.setCurrentIndex(-1)
        self.selecao_data.activated.connect(self.atualizar_estatisticas)

        self.total_livros = QLineEdit()
        self.total_livros.setReadOnly(True)
        self.total_usuarios = QLineEdit()
        self.total_usuarios = QLineEdit()
        self.total_usuarios.setReadOnly(True)
        self.emprestimos_ativos = QLineEdit()
        self.emprestimos_ativos.setReadOnly(True)
        self.livro_mais_emprestado = QLineEdit()
        self.livro_mais_emprestado.setReadOnly(True)
        self.quantidade_livro_mais_emprestado = QLineEdit()
        self.quantidade_livro_mais_emprestado.setReadOnly(True)

        layout_dados.addRow("Total de livros cadastrados:", self.total_livros)
        layout_dados.addRow("Total de usuários cadastrados:", self.total_usuarios)
        layout_dados.addRow("Total de empréstimos ativos:", self.emprestimos_ativos)
        layout_dados.addRow("Livro mais emprestado:", self.livro_mais_emprestado)
        layout_dados.addRow("Total de empréstimos do livro mais emprestado:", self.quantidade_livro_mais_emprestado)

        self.botao_importar = QPushButton("Importar Dados")
        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.clicked.connect(self.voltar_janela)

        layout_botoes.addWidget(self.botao_importar)
        layout_botoes.addWidget(self.botao_voltar)


        layout.addWidget(label_filtro)
        layout.addWidget(self.selecao_data)
        layout.addLayout(layout_dados)
        layout.addLayout(layout_botoes)

        self.setLayout(layout)


    def carregar_filtro(self):
        filtros = ["Sem Filtro", "3 dias", "7 dias", "1 mês", "3 meses", "6 meses", "1 ano"]
        self.selecao_data.clear()
        self.selecao_data.addItems(filtros)
        
    def atualizar_estatisticas(self):
        filtros = ["1000 years", "3 days", "7 days", "1 month", "3 months", "6 months", "1 year"]

        indice = self.selecao_data.currentIndex()
        livros = self.livro_controller.estatisticas()
        qtd_livros  = livros[0][0]
        self.total_livros.setText(str(qtd_livros))

        lista_usuario = self.usuario_controller.quantidade_usuarios(filtros[indice])
        qtd_usuarios = len(lista_usuario)
        self.total_usuarios.setText(str(qtd_usuarios))

        devolvidos = self.emprestimo_controller.estatistica_emprestimos_ativos(filtros[indice])
        emprestimos_ativos = self.emprestimo_controller.listar_historico_ou_emprestimos_ativos("ativo", "status")
        emprestimos_ativos_filtrado = len(devolvidos) + len(emprestimos_ativos)
        self.emprestimos_ativos.setText(str(emprestimos_ativos_filtrado))

        livro_mais_emprestado = self.emprestimo_controller.livros_mais_emprestados(filtros[indice])
        id_livro = livro_mais_emprestado[0][0]
        lista_nome_livro = self.livro_controller.buscar_id(id_livro)
        nome_livro = lista_nome_livro[0][0]
        self.livro_mais_emprestado.setText(nome_livro)

        qtd_emprestimos = livro_mais_emprestado[0][1]
        self.quantidade_livro_mais_emprestado.setText(str(qtd_emprestimos))
        
    def voltar_janela(self):
        self.stacked_widget.setCurrentIndex(0) # Muda para a janela principal
