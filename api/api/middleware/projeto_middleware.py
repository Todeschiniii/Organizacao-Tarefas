# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class ProjetoMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Projeto.

    Objetivos:
    - Garantir que os campos obrigatórios existam antes de chamar os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição para criação de um novo projeto.

        Verifica apenas a existência:
        - O objeto 'projeto' existe
        - Campos obrigatórios: nome, status
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ProjetoMiddleware.validate_body()")
            body = request.get_json()
            
            if not body or 'projeto' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'projeto' é obrigatório!"})

            projeto = body['projeto']

            # ✅ CORREÇÃO: Campos obrigatórios - nome e status (usuario_id é opcional)
            campos_obrigatorios = ["nome", "status"]
            for campo in campos_obrigatorios:
                if campo not in projeto:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_body_update(self, f):
        """
        Decorator para validar o corpo da requisição para atualização de projeto.

        Verifica apenas a existência:
        - O objeto 'projeto' existe
        - Campos obrigatórios: nome, status
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ProjetoMiddleware.validate_body_update()")
            body = request.get_json()
            
            if not body or 'projeto' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'projeto' é obrigatório!"})

            projeto = body['projeto']

            # ✅ CORREÇÃO: Campos obrigatórios para atualização
            campos_obrigatorios = ["nome", "status"]
            for campo in campos_obrigatorios:
                if campo not in projeto:
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
            print("🔷 ProjetoMiddleware.validate_id_param()")
            if 'id' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'id' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function

    def validate_usuario_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'usuario_id'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ProjetoMiddleware.validate_usuario_id_param()")
            if 'usuario_id' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'usuario_id' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function