from models.conexao import ConexaoDB
from psycopg2 import sql


class Livro:
    def __init__(self):
        self.db = ConexaoDB()

    def inserir_livro(self, titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel):
        query = sql.SQL("""
            INSERT INTO {tabela} (titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel)
            VALUES (%s, %s, %s, %s, %s, %s)
        """).format(
            tabela=sql.Identifier("livros")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel))
            conexao.commit()

        except Exception as erro:
            print("Erro ao inserir livro:", erro)
            conexao.rollback()
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def listar_livros(self):
 
        query = sql.SQL("""
            SELECT id, titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel
            FROM {tabela} ORDER BY id ASC
        """).format(
            tabela=sql.Identifier("livros")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query)
            dados = cursor.fetchall()

            return dados

        except Exception as erro:
            print("Erro ao listar livro:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()
    
    def atualizar_livro(self, id, titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel):
        query = sql.SQL("""
            UPDATE {tabela} SET titulo = %s, autor = %s, isbn = %s, ano_publicacao = %s, quantidade_total = %s, quantidade_disponivel = %s
            WHERE id = %s
        """).format(
            tabela=sql.Identifier("livros")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel, id))
            conexao.commit()

        except Exception as erro:
            print("Erro ao atualizar livro:", erro)
            conexao.rollback()
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def atualizar_quantidade_disponivel(self, id, valor):
        query = sql.SQL("""
            UPDATE {tabela} SET quantidade_disponivel = quantidade_disponivel + %s
            WHERE id = %s
        """).format(
            tabela=sql.Identifier("livros")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (valor, id,))
            conexao.commit()

        except Exception as erro:
            print("Erro ao atualizar quantidade disponível do livro:", erro)
            conexao.rollback()
        finally:
            if conexao:
                cursor.close()
                conexao.close()


    def buscar_livro(self, parametro, nome_coluna):
        query = sql.SQL("""
             SELECT id, titulo, autor, isbn, ano_publicacao, quantidade_total, quantidade_disponivel FROM {tabela} WHERE {coluna} ILIKE %s ORDER BY id ASC
        """).format(
            tabela=sql.Identifier("livros"),
            coluna = sql.Identifier(nome_coluna)
        )
        parametro_formatado = f"%{parametro}%"
        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (parametro_formatado,))
            dados = cursor.fetchall()

            return dados

        except Exception as erro:
            print("Erro ao encontrar livro:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def excluir_livro(self, id):
        query = sql.SQL("""
             Delete FROM {tabela} WHERE id = %s
        """).format(
            tabela=sql.Identifier("livros")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (id,))
            conexao.commit()

            return True

        except Exception as erro:
            conexao.rollback()
            print("Erro ao deletar livro:", erro)
            return False
        finally:
            if conexao:
                cursor.close()
                conexao.close()
           
    def livros_emprestados(self, id_livro):
        query = sql.SQL("""
            SELECT id FROM {tabela} WHERE livro_id = %s and status = %s
        """).format(
            tabela=sql.Identifier("emprestimos")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (id_livro, "ativo"))
            dados = cursor.fetchall()
            return dados

        except Exception as erro:
            print("Erro ao listar livro:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def quantidade_livros(self):
        query = sql.SQL("""
             SELECT SUM(quantidade_total) FROM {tabela}
        """).format(
            tabela=sql.Identifier("livros")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query)
            dados = cursor.fetchall()
            return dados

        except Exception as erro:
            print("Erro ao somar livros:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def busca_id(self, id):
        query = sql.SQL("""
                SELECT titulo FROM {tabela} WHERE id = %s
            """).format(
                tabela=sql.Identifier("livros")
            )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (id,))
            dados = cursor.fetchall()
            return dados

        except Exception as erro:
            print("Erro ao encontrar livro:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()