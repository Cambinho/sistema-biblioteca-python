from models.emprestimo import Emprestimo
from utils import validadores

class EmprestimoController:
    def __init__(self):
        self.model = Emprestimo()

    def realizar_emprestimo(self, id_usuario, id_livro, data_emprestimo,
            data_devolucao_prevista, data_devolucao_real, status):
        resultado = validadores.teste_campos_vazios(id_usuario, id_livro, data_emprestimo,
            data_devolucao_prevista, status)
        if resultado:
            self.model.realizar_emprestimo(id_usuario, id_livro, data_emprestimo,
                data_devolucao_prevista, data_devolucao_real, status)
            return True, "Empréstimo cadastrado!"
        return False, "Falha ao registrar o empréstimo."
    
    def registrar_devolucao(self, id, data_devolucao):
        resultado = validadores.teste_campos_vazios(id, data_devolucao)
        if resultado:
            self.model.registrar_devolucao(id, data_devolucao)
            return True, "Devolução registrada!"
        else:
            return False, "Falha em registrar devolução."

    def listar(self):
        return self.model.listar_emprestimos()
    
    def listar_historico_ou_emprestimos_ativos(self, parametro, nome_coluna):
        return self.model.listar_historico_ou_emprestimos_ativos(parametro, nome_coluna)
    
    def estatistica_emprestimos_ativos(self, filtro):
        return self.model.estatistica_emprestimos_ativos(filtro)
    
    def livros_mais_emprestados(self, filtro):
        return self.model.livros_mais_emprestados(filtro)
    
