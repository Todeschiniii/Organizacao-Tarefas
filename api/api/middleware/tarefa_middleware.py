# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class TarefaMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Tarefa.

    Objetivos:
    - Garantir que os campos obrigatórios existam antes de chamar os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição para criação de uma nova tarefa.

        Verifica apenas a existência:
        - O objeto 'tarefa' existe
        - Campos obrigatórios: titulo, projeto_id
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 TarefaMiddleware.validate_body()")
            body = request.get_json()
            
            if not body or 'tarefa' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'tarefa' é obrigatório!"})

            tarefa = body['tarefa']

            # Apenas verificar existência dos campos obrigatórios
            campos_obrigatorios = ["titulo", "projeto_id"]
            for campo in campos_obrigatorios:
                if campo not in tarefa:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_body_update(self, f):
        """
        Decorator para validar o corpo da requisição para atualização de tarefa.

        Verifica apenas a existência:
        - O objeto 'tarefa' existe
        - Campos obrigatórios: titulo, concluida
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 TarefaMiddleware.validate_body_update()")
            body = request.get_json()
            
            if not body or 'tarefa' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'tarefa' é obrigatório!"})

            tarefa = body['tarefa']

            # Campos obrigatórios para atualização
            campos_obrigatorios = ["titulo", "concluida"]
            for campo in campos_obrigatorios:
                if campo not in tarefa:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'id'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 TarefaMiddleware.validate_id_param()")
            if 'id' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'id' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function

    def validate_projeto_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'projeto_id'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 TarefaMiddleware.validate_projeto_id_param()")
            if 'projeto_id' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'projeto_id' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function