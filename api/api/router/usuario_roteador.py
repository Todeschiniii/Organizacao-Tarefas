# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.usuario_middleware import UsuarioMiddleware
from api.control.usuario_control import UsuarioControl

class UsuarioRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Usuario no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Usuario.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, usuario_middleware: UsuarioMiddleware, usuario_control: UsuarioControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param usuario_middleware: Middleware com validações específicas para Usuario.
        :param usuario_control: Controlador que implementa a lógica de negócio.
        """
        print("⬆️  UsuarioRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__usuario_middleware = usuario_middleware
        self.__usuario_control = usuario_control

        # ✅ CORREÇÃO: Blueprint com nome no singular
        self.__blueprint = Blueprint('usuario', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Usuario.

        Rotas implementadas:
        - POST /login    -> Autentica usuário e retorna token JWT
        - POST /         -> Cria um novo usuário (cadastro)
        - GET /          -> Lista todos os usuários (público para login)
        - GET /<id>      -> Retorna um usuário por ID
        - PUT /<id>      -> Atualiza um usuário por ID
        - DELETE /<id>   -> Remove um usuário por ID
        - GET /me        -> Retorna dados do usuário autenticado
        - GET /email/<email> -> Busca usuário por email
        """

        # POST /login -> autentica usuário e retorna token JWT
        @self.__blueprint.route('/login', methods=['POST'])
        @self.__usuario_middleware.validate_login_body
        def login():
            """
            Rota responsável por autenticar um usuário.
            Não requer autenticação JWT.
            
            Body esperado:
            {
                "usuario": {
                    "email": "email@exemplo.com",
                    "senha": "senha123"
                }
            }
            """
            return self.__usuario_control.login()

        # POST / -> cria um usuário (cadastro)
        @self.__blueprint.route('/', methods=['POST'])
        @self.__usuario_middleware.validate_body
        def store():
            """
            Rota responsável por criar um novo usuário.
            Não requer autenticação JWT para permitir cadastro.
            
            Body esperado:
            {
                "usuario": {
                    "nome": "Nome Completo",
                    "email": "email@exemplo.com", 
                    "senha": "senha123"
                }
            }
            """
            return self.__usuario_control.store()

        # GET / -> lista todos os usuários
        @self.__blueprint.route('/', methods=['GET'])
        def index():
            """
            Rota responsável por listar todos os usuários cadastrados no sistema.
            NÃO requer autenticação JWT para permitir seleção na tela de login.
            """
            return self.__usuario_control.index()

        # GET /<id> -> retorna um usuário específico
        @self.__blueprint.route('/<int:id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__usuario_middleware.validate_id_param
        def show(id):
            """
            Rota que retorna um usuário específico pelo seu ID.
            Requer autenticação JWT.

            :param id: int - ID do usuário vindo da URI.
            """
            return self.__usuario_control.show(id)

        # PUT /<id> -> atualiza um usuário
        @self.__blueprint.route('/<int:id>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__usuario_middleware.validate_id_param
        @self.__usuario_middleware.validate_body_update
        def update(id):
            """
            Rota que atualiza um usuário existente.
            Requer autenticação JWT.

            :param id: int - ID do usuário a ser atualizado.
            """
            return self.__usuario_control.update(id)

        # DELETE /<id> -> remove um usuário
        @self.__blueprint.route('/<int:id>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__usuario_middleware.validate_id_param
        def destroy(id):
            """
            Rota que remove um usuário pelo seu ID.
            Requer autenticação JWT.

            :param id: int - ID do usuário a ser removido.
            """
            return self.__usuario_control.destroy(id)

        # GET /me -> retorna dados do usuário autenticado
        @self.__blueprint.route('/me', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def show_me():
            """
            Rota que retorna os dados do usuário autenticado.
            Requer autenticação JWT.
            """
            # Obtém o ID do usuário do token JWT
            user_id = self.__jwt_middleware.get_user_id()
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Não foi possível identificar o usuário",
                        "code": 401
                    }
                }), 401
            
            return self.__usuario_control.show(user_id)

        # GET /email/<email> -> busca usuário por email
        @self.__blueprint.route('/email/<string:email>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def show_by_email(email):
            """
            Rota que retorna um usuário pelo seu email.
            Requer autenticação JWT.

            :param email: string - Email do usuário.
            """
            return self.__usuario_control.show_by_email(email)

        # GET /verificar-email/<email> -> verifica se email existe (público)
        @self.__blueprint.route('/verificar-email/<string:email>', methods=['GET'])
        def verificar_email(email):
            """
            Rota que verifica se um email já está cadastrado.
            Não requer autenticação JWT.
            
            :param email: string - Email a ser verificado.
            """
            return self.__usuario_control.verificar_email(email)

        # POST /logout -> invalida token (opcional)
        @self.__blueprint.route('/logout', methods=['POST'])
        @self.__jwt_middleware.validate_token
        def logout():
            """
            Rota para logout do usuário.
            Requer autenticação JWT.
            Em uma implementação real, invalidaria o token no servidor.
            """
            return jsonify({
                "success": True,
                "message": "Logout realizado com sucesso",
                "data": None
            }), 200

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint