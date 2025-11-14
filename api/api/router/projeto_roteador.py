# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.projeto_middleware import ProjetoMiddleware
from api.control.projeto_control import ProjetoControl

class ProjetoRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Projeto no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Projeto.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, projeto_middleware: ProjetoMiddleware, projeto_control: ProjetoControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param projeto_middleware: Middleware com validações específicas para Projeto.
        :param projeto_control: Controlador que implementa a lógica de negócio.
        """
        print("⬆️  ProjetoRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__projeto_middleware = projeto_middleware
        self.__projeto_control = projeto_control

        self.__blueprint = Blueprint('projeto', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Projeto.

        Rotas implementadas:
        - POST /        -> Cria um novo projeto PARA O USUÁRIO
        - GET /         -> Lista todos os projetos DO USUÁRIO
        - GET /<id>     -> Retorna um projeto por ID (só se for do usuário)
        - PUT /<id>     -> Atualiza um projeto por ID (só se for do usuário)
        - DELETE /<id>  -> Remove um projeto por ID (só se for do usuário)
        - GET /usuario/<usuario_id> -> Lista projetos por usuário (só admin)
        - GET /meus-projetos -> Lista projetos do usuário autenticado
        """

        # POST / -> cria um projeto PARA O USUÁRIO
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_body
        def store():
            """
            Rota responsável por criar um novo projeto.
            Requer autenticação JWT.
            O projeto será criado para o usuário autenticado.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__projeto_control.store(user_id)

        # GET / -> lista todos os projetos DO USUÁRIO
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def index():
            """
            Rota responsável por listar todos os projetos do usuário autenticado.
            Requer autenticação JWT.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__projeto_control.index(user_id)

        # GET /<id> -> retorna um projeto específico (só se for do usuário)
        @self.__blueprint.route('/<int:id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_id_param
        def show(id):
            """
            Rota que retorna um projeto específico pelo seu ID.
            Requer autenticação JWT.
            Só retorna se o projeto pertencer ao usuário.

            :param id: int - ID do projeto vindo da URI.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__projeto_control.show(id, user_id)

        # PUT /<id> -> atualiza um projeto (só se for do usuário)
        @self.__blueprint.route('/<int:id>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_id_param
        @self.__projeto_middleware.validate_body_update
        def update(id):
            """
            Rota que atualiza um projeto existente.
            Requer autenticação JWT.
            Só atualiza se o projeto pertencer ao usuário.

            :param id: int - ID do projeto a ser atualizado.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__projeto_control.update(id, user_id)

        # DELETE /<id> -> remove um projeto (só se for do usuário)
        @self.__blueprint.route('/<int:id>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_id_param
        def destroy(id):
            """
            Rota que remove um projeto pelo seu ID.
            Requer autenticação JWT.
            Só remove se o projeto pertencer ao usuário.

            :param id: int - ID do projeto a ser removido.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__projeto_control.destroy(id, user_id)

        # GET /usuario/<usuario_id> -> lista projetos por usuário (só admin)
        @self.__blueprint.route('/usuario/<int:usuario_id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_usuario_id_param
        def show_by_usuario(usuario_id):
            """
            Rota que retorna todos os projetos de um usuário específico.
            Requer autenticação JWT.
            (Normalmente só admin pode ver projetos de outros usuários)
            """
            return self.__projeto_control.show_by_usuario(usuario_id)

        # GET /meus-projetos -> lista projetos do usuário autenticado
        @self.__blueprint.route('/meus-projetos', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def show_meus_projetos():
            """
            Rota que retorna todos os projetos do usuário autenticado.
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
            
            # ✅ CORREÇÃO: Usa o método index que agora filtra por usuário
            return self.__projeto_control.index(user_id)

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint