# dao/usuario_dao.py
from datetime import datetime
from api.model.usuario import Usuario

class UsuarioDAO:
    def __init__(self, database_dependency):
        print("⬆️  UsuarioDAO.__init__()")
        self.__database = database_dependency
        self._create_tables()

    def _create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        print("🟢 UsuarioDAO._create_tables()")
        try:
            # ✅ CORREÇÃO: Sintaxe MySQL para criar tabela
            SQL = '''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    senha_hash VARCHAR(255) NOT NULL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
            self.__database.execute_query(SQL)
            print("✅ Tabela 'usuarios' criada/verificada com sucesso!")
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO._create_tables(): {e}")
            # Não levanta exceção para evitar que a aplicação pare
            # A tabela pode já existir

    def create(self, usuario: Usuario) -> int:
        """
        Cria um novo usuário no banco de dados
        :param usuario: Objeto Usuario
        :return: ID do usuário criado
        """
        print("🟢 UsuarioDAO.create()")
        try:
            SQL = '''
                INSERT INTO usuarios (nome, email, senha_hash, data_criacao)
                VALUES (%s, %s, %s, %s)
            '''
            params = (
                usuario.nome, 
                usuario.email, 
                usuario.senha_hash, 
                usuario.data_criacao.strftime('%Y-%m-%d %H:%M:%S')
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir usuário")
            return insert_id

        except Exception as e:
            if "Duplicate entry" in str(e) or "UNIQUE constraint" in str(e):
                raise ValueError("Email já cadastrado")
            print(f"❌ Erro em UsuarioDAO.create(): {e}")
            raise

    def find_by_id(self, usuario_id: int) -> Usuario | None:
        """
        Busca usuário por ID
        :param usuario_id: ID do usuário
        :return: Objeto Usuario ou None
        """
        print("✅ UsuarioDAO.find_by_id()")
        try:
            SQL = '''
                SELECT id, nome, email, senha_hash, data_criacao 
                FROM usuarios WHERE id = %s
            '''
            rows = self.__database.execute_query(SQL, (usuario_id,), fetch=True)

            if not rows:
                return None

            row = rows[0]
            usuario = Usuario()
            usuario.id = row["id"]
            usuario.nome = row["nome"]
            usuario.email = row["email"]
            usuario.senha_hash = row["senha_hash"]
            
            # Converter string para datetime
            if row["data_criacao"]:
                if hasattr(row["data_criacao"], 'isoformat'):
                    usuario.data_criacao = row["data_criacao"]
                else:
                    usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S')
            
            return usuario

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.find_by_id(): {e}")
            raise

    def find_by_email(self, email: str) -> Usuario | None:
        """
        Busca usuário por email
        :param email: Email do usuário
        :return: Objeto Usuario ou None
        """
        print("🟢 UsuarioDAO.find_by_email()")
        try:
            SQL = '''
                SELECT id, nome, email, senha_hash, data_criacao 
                FROM usuarios WHERE email = %s
            '''
            rows = self.__database.execute_query(SQL, (email,), fetch=True)

            if not rows:
                return None

            row = rows[0]
            usuario = Usuario()
            usuario.id = row["id"]
            usuario.nome = row["nome"]
            usuario.email = row["email"]
            usuario.senha_hash = row["senha_hash"]
            
            # Converter string para datetime
            if row["data_criacao"]:
                if hasattr(row["data_criacao"], 'isoformat'):
                    usuario.data_criacao = row["data_criacao"]
                else:
                    usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S')
            
            return usuario

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.find_by_email(): {e}")
            raise

    def find_all(self) -> list[Usuario]:
        """
        Retorna todos os usuários
        :return: Lista de objetos Usuario
        """
        print("🟢 UsuarioDAO.find_all()")
        try:
            SQL = '''
                SELECT id, nome, email, senha_hash, data_criacao 
                FROM usuarios ORDER BY id
            '''
            rows = self.__database.execute_query(SQL, fetch=True)

            usuarios = []
            for row in rows:
                usuario = Usuario()
                usuario.id = row["id"]
                usuario.nome = row["nome"]
                usuario.email = row["email"]
                usuario.senha_hash = row["senha_hash"]
                
                # Converter string para datetime
                if row["data_criacao"]:
                    if hasattr(row["data_criacao"], 'isoformat'):
                        usuario.data_criacao = row["data_criacao"]
                    else:
                        usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S')
                
                usuarios.append(usuario)

            return usuarios

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.find_all(): {e}")
            raise

    def update(self, usuario: Usuario) -> bool:
        """
        Atualiza usuário
        :param usuario: Objeto Usuario
        :return: Boolean indicando sucesso
        """
        print("🟢 UsuarioDAO.update()")
        try:
            SQL = '''
                UPDATE usuarios 
                SET nome = %s, email = %s, senha_hash = %s
                WHERE id = %s
            '''
            params = (
                usuario.nome, 
                usuario.email, 
                usuario.senha_hash, 
                usuario.id
            )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0

        except Exception as e:
            if "Duplicate entry" in str(e) or "UNIQUE constraint" in str(e):
                raise ValueError("Email já cadastrado")
            print(f"❌ Erro em UsuarioDAO.update(): {e}")
            raise

    def delete(self, usuario_id: int) -> bool:
        """
        Exclui usuário por ID
        :param usuario_id: ID do usuário
        :return: Boolean indicando sucesso
        """
        print("🟢 UsuarioDAO.delete()")
        try:
            SQL = 'DELETE FROM usuarios WHERE id = %s'
            affected = self.__database.execute_query(SQL, (usuario_id,))
            return affected > 0

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.delete(): {e}")
            raise

    def find_by_field(self, campo: str, valor) -> list[Usuario]:
        """
        Busca usuários por campo específico
        :param campo: Campo para busca
        :param valor: Valor do campo
        :return: Lista de objetos Usuario
        """
        print(f"🟢 UsuarioDAO.find_by_field() - Campo: {campo}, Valor: {valor}")
        try:
            allowed_fields = ["id", "nome", "email"]
            if campo not in allowed_fields:
                raise ValueError("Campo inválido para busca")

            SQL = f'''
                SELECT id, nome, email, senha_hash, data_criacao 
                FROM usuarios WHERE {campo} = %s
            '''
            rows = self.__database.execute_query(SQL, (valor,), fetch=True)

            usuarios = []
            for row in rows:
                usuario = Usuario()
                usuario.id = row["id"]
                usuario.nome = row["nome"]
                usuario.email = row["email"]
                usuario.senha_hash = row["senha_hash"]
                
                # Converter string para datetime
                if row["data_criacao"]:
                    if hasattr(row["data_criacao"], 'isoformat'):
                        usuario.data_criacao = row["data_criacao"]
                    else:
                        usuario.data_criacao = datetime.strptime(str(row["data_criacao"]), '%Y-%m-%d %H:%M:%S')
                
                usuarios.append(usuario)

            return usuarios

        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.find_by_field(): {e}")
            raise