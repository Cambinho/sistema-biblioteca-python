from models.livro import Livro
from utils import validadores


class LivroController:
    def __init__(self):
        self.model = Livro()

    def cadastrar(self, titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel):
        resultado = validadores.teste_campos_vazios(titulo, autor, isbn, quantidade_total, quantidade_disponivel)
        if resultado:
            self.model.inserir_livro(titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel)
            return True, "Livro cadastrado!"
        return False, "Preencha todos os campos!"

    def listar(self):
        return self.model.listar_livros()
    

    def buscar(self, parametro, nome_coluna = "titulo"):
        return self.model.buscar_livro(parametro, nome_coluna)
    

    def atualizar(self, id, titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel):
        resultado = validadores.teste_campos_vazios(titulo, autor, isbn, quantidade_total, quantidade_disponivel)
        if resultado:
            self.model.atualizar_livro(id, titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel)
            return True, "Livro atualizado!"
        return False, "Todos os campos precisam estar preenchidos!"

    def excluir(self, id):
        return self.model.excluir_livro(id)
    
    def livros_emprestados(self, id):
        return self.model.livros_emprestados(id)
    
    def estatisticas(self):
        return self.model.quantidade_livros()
    
    def buscar_id(self, id):
        return self.model.busca_id(id)
