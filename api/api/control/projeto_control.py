# -*- coding: utf-8 -*-
from flask import request, jsonify
import traceback
from api.service.projeto_service import ProjetoService
from api.utils.error_response import ErrorResponse
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
"""
Classe responsável por controlar os endpoints da API REST para a entidade Projeto.

Implementa métodos de CRUD, utilizando injeção de dependência
para receber a instância de ProjetoService, desacoplando a lógica de negócio
da camada de controle.
"""
class ProjetoControl:
    def __init__(self, projeto_service: ProjetoService):
        """
        Construtor da classe ProjetoControl
        :param projeto_service: Instância do ProjetoService (injeção de dependência)
        """
        print("⬆️  ProjetoControl.constructor()")
        self.__projeto_service = projeto_service

    def store(self):
        """Cria um novo projeto"""
        print("🔵 ProjetoControl.store()")
        try:
            json_projeto = request.json.get("projeto")
            newIdProjeto = self.__projeto_service.createProjeto(json_projeto)
            return jsonify({
                "success": True,
                "message": "Projeto criado com sucesso",
                "data": {
                    "projeto": {
                        "id": newIdProjeto,
                        "nome": json_projeto.get("nome"),
                        "descricao": json_projeto.get("descricao"),
                        "data_inicio": json_projeto.get("data_inicio"),
                        "status": json_projeto.get("status", "Pendente"),
                        "usuario_id": json_projeto.get("usuario_id")
                    }
                }
            }), 201
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em store: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def index(self):
        """Lista todos os projetos cadastrados"""
        print("🔵 ProjetoControl.index()")
        try:
            lista_projetos = self.__projeto_service.findAll()
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"projetos": lista_projetos}
            }), 200
        except Exception as e:
            print(f"❌ Erro inesperado em index: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def show(self, id):
        """Busca um projeto pelo ID"""
        print("🔵 ProjetoControl.show()")
        try:
            projeto = self.__projeto_service.findById(id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": projeto
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em show: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def update(self, id):
        """Atualiza os dados de um projeto existente"""
        print("🔵 ProjetoControl.update()")
        try:
            projeto_atualizado = self.__projeto_service.updateProjeto(id, request.json)

            return jsonify({
                "success": True,
                "message": "Projeto atualizado com sucesso",
                "data": {
                    "projeto": {
                        "id": int(id),
                        "nome": request.json.get("projeto", {}).get("nome"),
                        "status": request.json.get("projeto", {}).get("status")
                    }
                }
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em update: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def destroy(self, id):
        """Remove um projeto pelo ID"""
        print("🔵 ProjetoControl.destroy()")
        try:
            excluiu = self.__projeto_service.deleteProjeto(id)
            return jsonify({
                "success": True,
                "message": "Projeto excluído com sucesso"
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em destroy: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def show_by_usuario(self, usuario_id):
        """Lista todos os projetos de um usuário específico"""
        print("🔵 ProjetoControl.show_by_usuario()")
        try:
            projetos = self.__projeto_service.findByUsuarioId(usuario_id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"projetos": projetos}
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em show_by_usuario: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500