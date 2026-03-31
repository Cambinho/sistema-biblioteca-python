from models.conexao import ConexaoDB
from psycopg2 import sql

class Usuario:
    def __init__(self):
        self.db = ConexaoDB()

    def inserir_usuario(self, nome, email, telefone, data_cadastro):
        query = sql.SQL("""
            INSERT INTO {tabela} (nome, email, telefone, data_cadastro)
            VALUES (%s, %s, %s, %s)
        """).format(
            tabela=sql.Identifier("usuarios")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (nome, email, telefone, data_cadastro))
            conexao.commit()

        except Exception as erro:
            print("Erro ao inserir usuário:", erro)
            conexao.rollback()
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def listar_usuarios(self):
 
        query = sql.SQL("""
             SELECT id, nome, email, telefone, data_cadastro FROM {tabela} ORDER BY id ASC
        """).format(
            tabela=sql.Identifier("usuarios")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query)
            dados = cursor.fetchall()
            return dados

        except Exception as erro:
            print("Erro ao listar usuário:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()
    
    def atualizar_usuario(self, id, nome, email, telefone):
        query = sql.SQL("""
            UPDATE {tabela} SET nome = %s, email = %s, telefone = %s
            WHERE id = %s
        """).format(
            tabela=sql.Identifier("usuarios")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (nome, email, telefone, id))
            conexao.commit()

        except Exception as erro:
            print("Erro ao atualizar usuário:", erro)
            conexao.rollback()
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def buscar_usuario(self, parametro):
        query = sql.SQL("""
             SELECT id, nome, email, telefone, data_cadastro FROM {tabela} WHERE nome ILIKE %s ORDER BY id ASC
        """).format(
            tabela=sql.Identifier("usuarios")
        )
        parametro_formatado = f"%{parametro}%"
        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (parametro_formatado,))
            dados = cursor.fetchall()

            return dados

        except Exception as erro:
            print("Erro ao encontrar usuário:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def excluir_usuario(self, id):
        query = sql.SQL("""
             Delete FROM {tabela} WHERE id = %s
        """).format(
            tabela=sql.Identifier("usuarios")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (id,))
            conexao.commit()
            return True

        except Exception as erro:
            conexao.rollback()
            print("Erro ao deletar usuário:", erro)
            return False
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def quantidade_usuarios(self, filtro):
        query = sql.SQL("""
            SELECT id FROM {tabela} WHERE data_cadastro >= CURRENT_DATE - INTERVAL %s
        """).format(
            tabela=sql.Identifier("usuarios")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (filtro,))
            dados = cursor.fetchall()
            return dados

        except Exception as erro:
            print("Erro ao encontrar os dados:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()