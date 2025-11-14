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

        self.__blueprint = Blueprint('tarefa', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Tarefa.

        ✅ ROTAS ATUALIZADAS para nova estrutura:
        - POST /        -> Cria uma nova tarefa (com responsável e atribuidor)
        - GET /         -> Lista tarefas onde usuário é RESPONSÁVEL
        - GET /<id>     -> Retorna uma tarefa por ID (só se usuário for RESPONSÁVEL)
        - PUT /<id>     -> Atualiza uma tarefa (só se usuário for RESPONSÁVEL)
        - DELETE /<id>  -> Remove uma tarefa (só se usuário for RESPONSÁVEL)
        - GET /projeto/<projeto_id> -> Lista tarefas por projeto (só se usuário for RESPONSÁVEL)
        - PUT /<id>/concluir -> Marca tarefa como concluída (só se usuário for RESPONSÁVEL)
        - PUT /<id>/toggle-concluir -> Alterna status de conclusão
        - GET /minhas-tarefas -> Lista tarefas onde usuário é RESPONSÁVEL
        - GET /atribuidas-por-mim -> Lista tarefas que usuário ATRIBUIU para outros
        - GET /dashboard -> Estatísticas das tarefas
        """

        # POST / -> cria uma tarefa (com responsável e atribuidor)
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_body
        def store():
            """
            Rota responsável por criar uma nova tarefa.
            Requer autenticação JWT.
            O campo 'usuario_responsavel_id' é obrigatório no JSON.
            O 'usuario_atribuidor_id' será o ID do usuário autenticado.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token (será o atribuidor)
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.store(user_id)

        # GET / -> lista tarefas onde usuário é RESPONSÁVEL
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def index():
            """
            Rota responsável por listar tarefas onde o usuário é RESPONSÁVEL.
            Requer autenticação JWT.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.index(user_id)

        # GET /<id> -> retorna uma tarefa específica (só se usuário for RESPONSÁVEL)
        @self.__blueprint.route('/<int:id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        def show(id):
            """
            Rota que retorna uma tarefa específica pelo seu ID.
            Requer autenticação JWT.
            Só retorna se o usuário for RESPONSÁVEL pela tarefa.

            :param id: int - ID da tarefa vindo da URI.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.show(id, user_id)

        # PUT /<id> -> atualiza uma tarefa (só se usuário for RESPONSÁVEL)
        @self.__blueprint.route('/<int:id>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        @self.__tarefa_middleware.validate_body_update
        def update(id):
            """
            Rota que atualiza uma tarefa existente.
            Requer autenticação JWT.
            Só atualiza se o usuário for RESPONSÁVEL pela tarefa.

            :param id: int - ID da tarefa a ser atualizada.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.update(id, user_id)

        # DELETE /<id> -> remove uma tarefa (só se usuário for RESPONSÁVEL)
        @self.__blueprint.route('/<int:id>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        def destroy(id):
            """
            Rota que remove uma tarefa pelo seu ID.
            Requer autenticação JWT.
            Só remove se o usuário for RESPONSÁVEL pela tarefa.

            :param id: int - ID da tarefa a ser removida.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.destroy(id, user_id)

        # GET /projeto/<projeto_id> -> lista tarefas por projeto (só se usuário for RESPONSÁVEL)
        @self.__blueprint.route('/projeto/<int:projeto_id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_projeto_id_param
        def show_by_projeto(projeto_id):
            """
            Rota que retorna todas as tarefas de um projeto específico.
            Requer autenticação JWT.
            Só retorna se o usuário for RESPONSÁVEL pelas tarefas.

            :param projeto_id: int - ID do projeto.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.show_by_projeto(projeto_id, user_id)

        # PUT /<id>/concluir -> marca tarefa como concluída (só se usuário for RESPONSÁVEL)
        @self.__blueprint.route('/<int:id>/concluir', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        def marcar_concluida(id):
            """
            Rota que marca uma tarefa como concluída.
            Requer autenticação JWT.
            Só marca se o usuário for RESPONSÁVEL pela tarefa.

            :param id: int - ID da tarefa a ser marcada como concluída.
            """
            # ✅ CORREÇÃO: Obtém o ID do usuário do token
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.marcar_concluida(id, user_id)

        # ✅ NOVA ROTA: PUT /<id>/toggle-concluir -> alterna status de conclusão
        @self.__blueprint.route('/<int:id>/toggle-concluir', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__tarefa_middleware.validate_id_param
        def toggle_concluida(id):
            """
            Rota que alterna o status de conclusão da tarefa.
            Requer autenticação JWT.
            Só alterna se o usuário for RESPONSÁVEL pela tarefa.

            :param id: int - ID da tarefa.
            """
            user_id = self.__jwt_middleware.get_user_id()
            return self.__tarefa_control.toggle_concluida(id, user_id)

        # GET /minhas-tarefas -> lista tarefas onde usuário é RESPONSÁVEL
        @self.__blueprint.route('/minhas-tarefas', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def show_minhas_tarefas():
            """
            Rota que retorna todas as tarefas onde o usuário é RESPONSÁVEL.
            Requer autenticação JWT.
            """
            user_id = self.__jwt_middleware.get_user_id()
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Não foi possível identificar o usuário",
                        "code": 401
                    }
                }), 401
            
            # ✅ CORREÇÃO: Usa o método que busca por usuario_responsavel_id
            return self.__tarefa_control.minhas_tarefas_responsavel(user_id)

        # ✅ NOVA ROTA: GET /atribuidas-por-mim -> tarefas que usuário ATRIBUIU para outros
        @self.__blueprint.route('/atribuidas-por-mim', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def show_tarefas_atribuidas():
            """
            Rota que retorna todas as tarefas que o usuário ATRIBUIU para outros.
            Requer autenticação JWT.
            """
            user_id = self.__jwt_middleware.get_user_id()
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Não foi possível identificar o usuário",
                        "code": 401
                    }
                }), 401
            
            # ✅ CORREÇÃO: Nova rota para tarefas atribuídas para outros
            return self.__tarefa_control.tarefas_atribuidas(user_id)

        # GET /dashboard -> estatísticas das tarefas onde usuário é RESPONSÁVEL
        @self.__blueprint.route('/dashboard', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def dashboard():
            """
            Rota que retorna estatísticas das tarefas onde o usuário é RESPONSÁVEL.
            Requer autenticação JWT.
            """
            user_id = self.__jwt_middleware.get_user_id()
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Não foi possível identificar o usuário",
                        "code": 401
                    }
                }), 401
            
            # ✅ CORREÇÃO: Usa o método de estatísticas atualizado
            return self.__tarefa_control.count_tarefas(user_id)

        # ✅ NOVA ROTA: GET /todas-tarefas (apenas para desenvolvimento/admin)
        @self.__blueprint.route('/todas-tarefas', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def show_todas_tarefas():
            """
            Rota que retorna TODAS as tarefas (sem filtro por usuário).
            ⚠️ APENAS PARA DESENVOLVIMENTO/ADMIN
            Requer autenticação JWT.
            """
            user_id = self.__jwt_middleware.get_user_id()
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Não foi possível identificar o usuário",
                        "code": 401
                    }
                }), 401
            
            # ✅ CORREÇÃO: Busca todas as tarefas sem filtro (para admin/desenvolvimento)
            return self.__tarefa_control.index(None)

        # ✅ NOVA ROTA: GET /usuarios-disponiveis (para seleção de responsáveis)
        @self.__blueprint.route('/usuarios-disponiveis', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def usuarios_disponiveis():
            """
            Rota que retorna lista de usuários disponíveis para atribuição de tarefas.
            Requer autenticação JWT.
            """
            user_id = self.__jwt_middleware.get_user_id()
            if not user_id:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Não foi possível identificar o usuário",
                        "code": 401
                    }
                }), 401
            
            # ✅ CORREÇÃO: Esta rota precisaria de um serviço específico para usuários
            # Por enquanto, retorna uma lista básica
            return jsonify({
                "success": True,
                "message": "Lista de usuários disponíveis",
                "data": {
                    "usuarios": [
                        {
                            "id": 1,
                            "nome": "Ana Silva",
                            "email": "ana.silva@email.com"
                        },
                        {
                            "id": 2,
                            "nome": "Bruno Costa", 
                            "email": "bruno.costa@email.com"
                        },
                        {
                            "id": 3,
                            "nome": "Carlos Oliveira",
                            "email": "carlos.oliveira@email.com"
                        },
                        {
                            "id": 4,
                            "nome": "Davi Santos",
                            "email": "davi@email.com"
                        }
                    ],
                    "observacao": "Esta é uma lista estática para demonstração. Em produção, buscar do banco de dados."
                }
            }), 200

        # ✅ NOVA ROTA: Health check para tarefas
        @self.__blueprint.route('/health', methods=['GET'])
        def health_check():
            """
            Rota de health check para verificar se o serviço de tarefas está funcionando.
            Não requer autenticação.
            """
            return jsonify({
                "success": True,
                "message": "✅ Serviço de Tarefas está funcionando corretamente",
                "data": {
                    "service": "Tarefa API",
                    "status": "healthy",
                    "version": "1.0.0",
                    "endpoints": {
                        "criar_tarefa": "POST /api/tarefa/",
                        "listar_tarefas": "GET /api/tarefa/", 
                        "buscar_tarefa": "GET /api/tarefa/<id>",
                        "atualizar_tarefa": "PUT /api/tarefa/<id>",
                        "excluir_tarefa": "DELETE /api/tarefa/<id>",
                        "tarefas_por_projeto": "GET /api/tarefa/projeto/<projeto_id>",
                        "minhas_tarefas": "GET /api/tarefa/minhas-tarefas",
                        "tarefas_atribuidas": "GET /api/tarefa/atribuidas-por-mim",
                        "dashboard": "GET /api/tarefa/dashboard"
                    }
                }
            }), 200

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint