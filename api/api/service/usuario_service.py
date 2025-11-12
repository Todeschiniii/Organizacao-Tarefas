# api/service/usuario_service.py
from api.model.usuario import Usuario
from api.utils.error_response import ErrorResponse
import bcrypt
from datetime import datetime

class UsuarioService:
    def __init__(self, usuario_dao_dependency):
        """
        Service para regras de negócio do Usuario
        """
        print("⬆️  UsuarioService.__init__()")
        self.__usuario_dao = usuario_dao_dependency

    def createUsuario(self, usuario_data):
        """
        Cria um novo usuário com validações
        """
        try:
            # Verifica se email já existe
            if self.__usuario_dao.email_exists(usuario_data.get('email')):
                raise ErrorResponse("Email já cadastrado", 400)

            # Cria objeto Usuario
            usuario = Usuario()
            usuario.nome = usuario_data.get('nome')
            usuario.email = usuario_data.get('email')
            
            # Hash da senha
            senha = usuario_data.get('senha', '')
            if not senha:
                raise ErrorResponse("Senha é obrigatória", 400)
                
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            usuario.senha_hash = senha_hash
            usuario.data_criacao = datetime.now()

            # Salva no banco
            new_id = self.__usuario_dao.create(usuario)
            return new_id

        except ValueError as e:
            raise ErrorResponse(str(e), 400)
        except Exception as e:
            print(f"❌ Erro em createUsuario: {e}")
            raise ErrorResponse("Erro ao criar usuário", 500)

    def loginUsuario(self, login_data):
        """
        Autentica usuário
        """
        try:
            email = login_data.get('email')
            senha = login_data.get('senha')

            if not email or not senha:
                raise ErrorResponse("Email e senha são obrigatórios", 400)

            # Busca usuário
            usuario_db = self.__usuario_dao.find_by_email(email)
            if not usuario_db:
                raise ErrorResponse("Email ou senha incorretos", 401)

            # Verifica senha
            if not bcrypt.checkpw(senha.encode('utf-8'), usuario_db['senha_hash'].encode('utf-8')):
                raise ErrorResponse("Email ou senha incorretos", 401)

            # Retorna dados do usuário (sem senha)
            return {
                'usuario': {
                    'id': usuario_db['id'],
                    'nome': usuario_db['nome'],
                    'email': usuario_db['email']
                }
            }

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro em loginUsuario: {e}")
            raise ErrorResponse("Erro ao fazer login", 500)

    def findById(self, id):
        """
        Busca usuário por ID
        """
        try:
            usuario_db = self.__usuario_dao.find_by_id(id)
            if not usuario_db:
                raise ErrorResponse("Usuário não encontrado", 404)

            return {
                'usuario': {
                    'id': usuario_db['id'],
                    'nome': usuario_db['nome'],
                    'email': usuario_db['email'],
                    'data_criacao': usuario_db['data_criacao']
                }
            }

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro em findById: {e}")
            raise ErrorResponse("Erro ao buscar usuário", 500)

    def findAll(self):
        """
        Busca todos os usuários
        """
        try:
            usuarios_db = self.__usuario_dao.find_all()
            
            usuarios = []
            for usuario_db in usuarios_db:
                usuarios.append({
                    'id': usuario_db['id'],
                    'nome': usuario_db['nome'],
                    'email': usuario_db['email'],
                    'data_criacao': usuario_db['data_criacao']
                })

            return usuarios

        except Exception as e:
            print(f"❌ Erro em findAll: {e}")
            raise ErrorResponse("Erro ao buscar usuários", 500)

    def updateUsuario(self, id, usuario_data):
        """
        Atualiza usuário
        """
        try:
            usuario_db = self.__usuario_dao.find_by_id(id)
            if not usuario_db:
                raise ErrorResponse("Usuário não encontrado", 404)

            update_data = usuario_data.get('usuario', {})
            
            # Atualiza dados
            if 'nome' in update_data:
                usuario_db['nome'] = update_data['nome']
            if 'email' in update_data:
                usuario_db['email'] = update_data['email']
            if 'senha' in update_data:
                senha_hash = bcrypt.hashpw(update_data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                usuario_db['senha_hash'] = senha_hash

            self.__usuario_dao.update(id, usuario_db)
            return True

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro em updateUsuario: {e}")
            raise ErrorResponse("Erro ao atualizar usuário", 500)

    def deleteUsuario(self, id):
        """
        Remove usuário
        """
        try:
            usuario_db = self.__usuario_dao.find_by_id(id)
            if not usuario_db:
                raise ErrorResponse("Usuário não encontrado", 404)

            self.__usuario_dao.delete(id)
            return True

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro em deleteUsuario: {e}")
            raise ErrorResponse("Erro ao excluir usuário", 500)

    def verificarEmail(self, email):
        """
        Verifica se email existe
        """
        try:
            existe = self.__usuario_dao.email_exists(email)
            return {
                'email_existe': existe
            }

        except Exception as e:
            print(f"❌ Erro em verificarEmail: {e}")
            raise ErrorResponse("Erro ao verificar email", 500)