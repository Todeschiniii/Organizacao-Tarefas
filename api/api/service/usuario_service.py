# api/service/usuario_service.py
from api.model.usuario import Usuario  # ✅ CORREÇÃO: models NO PLURAL
from api.utils.error_response import ErrorResponse
import bcrypt
from datetime import datetime
import traceback

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
        print("🟢 UsuarioService.createUsuario()")
        print(f"📝 Dados recebidos: {usuario_data}")
        
        try:
            # Validações iniciais
            if not usuario_data:
                raise ErrorResponse("Dados do usuário não fornecidos", 400)
                
            email = usuario_data.get('email')
            nome = usuario_data.get('nome')
            senha = usuario_data.get('senha', '')

            # Valida campos obrigatórios
            if not email:
                raise ErrorResponse("Email é obrigatório", 400)
            if not nome:
                raise ErrorResponse("Nome é obrigatório", 400)
            if not senha:
                raise ErrorResponse("Senha é obrigatória", 400)

            # Verifica se email já existe
            print(f"🔍 Verificando se email existe: {email}")
            if self.__usuario_dao.email_exists(email):
                raise ErrorResponse("Email já cadastrado", 400)

            # Cria objeto Usuario
            print("👤 Criando objeto Usuario...")
            usuario = Usuario()
            usuario.nome = nome
            usuario.email = email
            
            # Hash da senha
            print("🔐 Gerando hash da senha...")
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            usuario.senha_hash = senha_hash
            usuario.data_criacao = datetime.now()

            print(f"💾 Salvando usuário no banco: {usuario.nome}, {usuario.email}")
            # Salva no banco
            new_id = self.__usuario_dao.create(usuario)
            print(f"✅ Usuário criado com ID: {new_id}")
            
            return new_id

        except ValueError as e:
            print(f"❌ Erro de validação em createUsuario: {e}")
            raise ErrorResponse(str(e), 400)
        except ErrorResponse:
            raise  # Re-lança erros que já são ErrorResponse
        except Exception as e:
            print(f"❌ Erro inesperado em createUsuario: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(f"Erro interno ao criar usuário: {str(e)}", 500)

    def loginUsuario(self, login_data):
        """
        Autentica usuário e retorna token JWT
        """
        print("🟢 UsuarioService.loginUsuario()")
        try:
            email = login_data.get('email')
            senha = login_data.get('senha')

            if not email or not senha:
                raise ErrorResponse("Email e senha são obrigatórios", 400)

            print(f"🔍 Buscando usuário por email: {email}")
            # Busca usuário
            usuario_db = self.__usuario_dao.find_by_email(email)
            if not usuario_db:
                raise ErrorResponse("Email ou senha incorretos", 401)

            print("🔐 Verificando senha...")
            # Verifica senha
            if not bcrypt.checkpw(senha.encode('utf-8'), usuario_db.senha_hash.encode('utf-8')):
                raise ErrorResponse("Email ou senha incorretos", 401)

            print(f"✅ Login bem-sucedido para: {usuario_db.nome}")
            
            # ✅ CORREÇÃO: GERAR TOKEN JWT
            from api.http.meu_token_jwt import MeuTokenJWT  # Import aqui para evitar circular imports
            
            token_jwt = MeuTokenJWT()
            
            # Claims para o token (ajuste conforme seus campos)
            claims = {
                "email": usuario_db.email,
                "name": usuario_db.nome,
                "idFuncionario": usuario_db.id,  # Ou "idUsuario" se preferir
                "role": "user"  # Defina o role conforme sua lógica
            }
            
            token = token_jwt.gerarToken(claims)
            
            # Retorna dados do usuário E o token
            return {
                'usuario': {
                    'id': usuario_db.id,
                    'nome': usuario_db.nome,
                    'email': usuario_db.email
                },
                'token': token  # ✅ TOKEN ADICIONADO AQUI
            }

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em loginUsuario: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao fazer login", 500)
    def findById(self, id):
        """
        Busca usuário por ID
        """
        print(f"🟢 UsuarioService.findById() - ID: {id}")
        try:
            usuario_db = self.__usuario_dao.find_by_id(id)
            if not usuario_db:
                raise ErrorResponse("Usuário não encontrado", 404)

            return {
                'usuario': {
                    'id': usuario_db.id,
                    'nome': usuario_db.nome,
                    'email': usuario_db.email,
                    'data_criacao': usuario_db.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if usuario_db.data_criacao else None
                }
            }

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em findById: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao buscar usuário", 500)

    def findAll(self):
        """
        Busca todos os usuários
        """
        print("🟢 UsuarioService.findAll()")
        try:
            usuarios_db = self.__usuario_dao.find_all()
            
            usuarios = []
            for usuario_db in usuarios_db:
                usuarios.append({
                    'id': usuario_db.id,
                    'nome': usuario_db.nome,
                    'email': usuario_db.email,
                    'data_criacao': usuario_db.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if usuario_db.data_criacao else None
                })

            print(f"✅ Encontrados {len(usuarios)} usuários")
            return usuarios

        except Exception as e:
            print(f"❌ Erro inesperado em findAll: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao buscar usuários", 500)

    def updateUsuario(self, id, usuario_data):
        """
        Atualiza usuário
        """
        print(f"🟢 UsuarioService.updateUsuario() - ID: {id}")
        try:
            usuario_db = self.__usuario_dao.find_by_id(id)
            if not usuario_db:
                raise ErrorResponse("Usuário não encontrado", 404)

            update_data = usuario_data.get('usuario', {})
            
            print(f"📝 Dados para atualização: {update_data}")
            # Atualiza dados
            if 'nome' in update_data:
                usuario_db.nome = update_data['nome']
            if 'email' in update_data:
                # Verifica se o novo email já existe (para outro usuário)
                if update_data['email'] != usuario_db.email:
                    if self.__usuario_dao.email_exists(update_data['email']):
                        raise ErrorResponse("Email já está em uso por outro usuário", 400)
                usuario_db.email = update_data['email']
            if 'senha' in update_data and update_data['senha']:
                senha_hash = bcrypt.hashpw(update_data['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                usuario_db.senha_hash = senha_hash

            self.__usuario_dao.update(usuario_db)
            print(f"✅ Usuário {id} atualizado com sucesso")
            return True

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em updateUsuario: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao atualizar usuário", 500)

    def deleteUsuario(self, id):
        """
        Remove usuário
        """
        print(f"🟢 UsuarioService.deleteUsuario() - ID: {id}")
        try:
            usuario_db = self.__usuario_dao.find_by_id(id)
            if not usuario_db:
                raise ErrorResponse("Usuário não encontrado", 404)

            self.__usuario_dao.delete(id)
            print(f"✅ Usuário {id} excluído com sucesso")
            return True

        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em deleteUsuario: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao excluir usuário", 500)

    def verificarEmail(self, email):
        """
        Verifica se email existe
        """
        print(f"🟢 UsuarioService.verificarEmail() - Email: {email}")
        try:
            existe = self.__usuario_dao.email_exists(email)
            print(f"📧 Email {email} existe: {existe}")
            return {
                'email_existe': existe
            }

        except Exception as e:
            print(f"❌ Erro inesperado em verificarEmail: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao verificar email", 500)