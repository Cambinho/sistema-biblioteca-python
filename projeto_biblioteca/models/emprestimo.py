from models.conexao import ConexaoDB
from psycopg2 import sql


class Emprestimo:
    def __init__(self):
        self.db = ConexaoDB()

    def realizar_emprestimo(self, usuario_id, livro_id, data_emprestimo,
            data_devolucao_prevista, data_devolucao_real, status):
        query = sql.SQL("""
            INSERT INTO {tabela} (usuario_id, livro_id, data_emprestimo,
            data_devolucao_prevista, data_devolucao_real, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """).format(
            tabela=sql.Identifier("emprestimos")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (usuario_id, livro_id, data_emprestimo,
            data_devolucao_prevista, data_devolucao_real, status,))
            conexao.commit()

        except Exception as erro:
            print("Erro ao emprestar livro:", erro)
            conexao.rollback()
        finally:
            if conexao:
                cursor.close()
                conexao.close()
    
    def registrar_devolucao(self, id, data_devolucao):
        query = sql.SQL("""
            UPDATE {tabela} SET data_devolucao_real = %s, status = %s
            WHERE id = %s
        """).format(
            tabela=sql.Identifier("emprestimos")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (data_devolucao, "devolvido", id))
            conexao.commit()

        except Exception as erro:
            print("Erro ao alterar status:", erro)
            conexao.rollback()
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def listar_emprestimos(self):
        query = sql.SQL("""
            SELECT 
                e.id, u.nome, l.titulo, e.data_emprestimo, e.data_devolucao_prevista,
                e.data_devolucao_real, e.status
            FROM {emprestimos} AS e
            INNER JOIN {usuarios} AS u ON u.id = e.usuario_id
            INNER JOIN {livros} AS l ON l.id = e.livro_id
            ORDER BY e.id
        """).format(
            emprestimos=sql.Identifier("emprestimos"),
            usuarios=sql.Identifier("usuarios"),
            livros=sql.Identifier("livros")
        )

        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query)
            dados = cursor.fetchall()

            return dados

        except Exception as erro:
            print("Erro ao listar alunos:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def listar_historico_ou_emprestimos_ativos(self, parametro, nome_coluna):
        query = sql.SQL("""
            SELECT 
                e.id, u.nome, l.titulo, e.data_emprestimo, e.data_devolucao_prevista,
                e.data_devolucao_real, e.status
            FROM {emprestimos} AS e
            INNER JOIN {usuarios} AS u ON u.id = e.usuario_id
            INNER JOIN {livros} AS l ON l.id = e.livro_id
            WHERE {coluna} = %s
            ORDER BY e.id
        """).format(
            emprestimos=sql.Identifier("emprestimos"),
            usuarios=sql.Identifier("usuarios"),
            livros=sql.Identifier("livros"),
            coluna=sql.Identifier(nome_coluna)
        )
        try:
            conexao = self.db.conectar()
            cursor = conexao.cursor()

            cursor.execute(query, (parametro,))
            dados = cursor.fetchall()

            return dados

        except Exception as erro:
            print("Erro ao listar histórico:", erro)
            return []
        finally:
            if conexao:
                cursor.close()
                conexao.close()

    def estatistica_emprestimos_ativos(self, filtro):
        query = sql.SQL("""
            SELECT id FROM {tabela} WHERE data_devolucao_real >=  CURRENT_DATE - INTERVAL %s
        """).format(
            tabela=sql.Identifier("emprestimos")
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

    def livros_mais_emprestados(self, filtro):
        query = sql.SQL("""
            SELECT livro_id, COUNT(*) AS total
            FROM {tabela} 
            WHERE data_emprestimo >= CURRENT_DATE - INTERVAL %s
            GROUP BY livro_id
            ORDER BY total DESC
        """).format(
            tabela=sql.Identifier("emprestimos")
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