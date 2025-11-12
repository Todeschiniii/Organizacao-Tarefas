# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.tarefa_middleware import TarefaMiddleware
from api.control.tarefa_control import TarefaControl

class TarefaRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Tarefa no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Tarefa.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, tarefa_middleware: TarefaMiddleware, tarefa_control: TarefaControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param tarefa_middleware: Middleware com validações específicas para Tarefa.
        :param tarefa_control: Controlador que implementa a lógica de negócio.
        """
        print("⬆️  TarefaRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__tarefa_middleware = tarefa_middleware
        self.__tarefa_control = tarefa_control

        # ✅ CORREÇÃO: Blueprint com nome no singular
        self.__blueprint = Blueprint('tarefa', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Tarefa.

        Rotas implementadas:
        - POST /        -> Cria uma nova tarefa
        - GET /         -> Lista todas as tarefas
        - GET /<id>     -> Retorna uma tarefa por ID
        - PUT /<id>     -> Atualiza uma tarefa por ID
        - DELETE /<id>  -> Remove uma tarefa por ID
        - GET /projeto/<projeto_id> -> Lista tarefas por projeto
        - PUT /<id>/concluir -> Marca tarefa como concluída
        - GET /minhas-tarefas -> Lista tarefas do usuário autenticado
        """

        # POST / -> cria uma tarefa
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_body
        def store():
            """
            Rota responsável por criar uma nova tarefa.
            Requer autenticação JWT.
            """
            return self.__tarefa_control.store()

        # GET / -> lista todas as tarefas
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def index():
            """
            Rota responsável por listar todas as tarefas cadastradas no sistema.
            Requer autenticação JWT.
            """
            return self.__tarefa_control.index()

        # GET /<id> -> retorna uma tarefa específica
        @self.__blueprint.route('/<int:id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        def show(id):
            """
            Rota que retorna uma tarefa específica pelo seu ID.
            Requer autenticação JWT.

            :param id: int - ID da tarefa vindo da URI.
            """
            return self.__tarefa_control.show(id)

        # PUT /<id> -> atualiza uma tarefa
        @self.__blueprint.route('/<int:id>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        @self.__tarefa_middleware.validate_body_update
        def update(id):
            """
            Rota que atualiza uma tarefa existente.
            Requer autenticação JWT.

            :param id: int - ID da tarefa a ser atualizada.
            """
            return self.__tarefa_control.update(id)

        # DELETE /<id> -> remove uma tarefa
        @self.__blueprint.route('/<int:id>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        def destroy(id):
            """
            Rota que remove uma tarefa pelo seu ID.
            Requer autenticação JWT.

            :param id: int - ID da tarefa a ser removida.
            """
            return self.__tarefa_control.destroy(id)

        # GET /projeto/<projeto_id> -> lista tarefas por projeto
        @self.__blueprint.route('/projeto/<int:projeto_id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_projeto_id_param
        def show_by_projeto(projeto_id):
            """
            Rota que retorna todas as tarefas de um projeto específico.
            Requer autenticação JWT.

            :param projeto_id: int - ID do projeto.
            """
            return self.__tarefa_control.show_by_projeto(projeto_id)

        # PUT /<id>/concluir -> marca tarefa como concluída
        @self.__blueprint.route('/<int:id>/concluir', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        def marcar_concluida(id):
            """
            Rota que marca uma tarefa como concluída.
            Requer autenticação JWT.

            :param id: int - ID da tarefa a ser marcada como concluída.
            """
            return self.__tarefa_control.marcar_concluida(id)

        # GET /minhas-tarefas -> lista tarefas do usuário autenticado
        @self.__blueprint.route('/minhas-tarefas', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def show_minhas_tarefas():
            """
            Rota que retorna todas as tarefas dos projetos do usuário autenticado.
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
            
            # Esta rota precisaria de um método específico no service/control
            # que busca tarefas por usuário (não apenas por projeto)
            # Por enquanto, vamos usar uma implementação básica
            return jsonify({
                "success": True,
                "message": "Rota em desenvolvimento - minhas-tarefas",
                "data": {"user_id": user_id}
            }), 200

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint