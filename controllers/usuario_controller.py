from models.usuario import Usuario
from utils import validadores

class UsuarioController:
    def __init__(self):
        self.model = Usuario()
    
    def cadastrar(self, nome, email, telefone, data_cadastro):
        resultado = validadores.teste_campos_vazios(nome, email, data_cadastro)
        if resultado:
            self.model.inserir_usuario(nome, email, telefone, data_cadastro)
            return True, "Usuário cadastrado!"
        return resultado, "Preencha todos os campos"

    def listar(self):
        return self.model.listar_usuarios()
    
    def atualizar(self, id, nome, email, telefone):
        resultado = validadores.teste_campos_vazios(id, nome, email)
        if resultado:
            self.model.atualizar_usuario(id, nome, email, telefone)
            return resultado, "Usuário atualizado!"
        return resultado, "Todos os campos precisam estar preenchidos."

    def buscar(self, parametro):
        return self.model.buscar_usuario(parametro)

    def excluir(self, id):
        return self.model.excluir_usuario(id)
    
    def quantidade_usuarios(self, filtro):
        return self.model.quantidade_usuarios(filtro)