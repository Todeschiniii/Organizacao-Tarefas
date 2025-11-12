# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class UsuarioMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Usuario.

    Objetivos:
    - Garantir que os campos obrigatórios existam antes de chamar os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição para criação de um novo usuário.

        Verifica apenas a existência:
        - O objeto 'usuario' existe
        - Campos obrigatórios: nome, email, senha_hash
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 UsuarioMiddleware.validate_body()")
            body = request.get_json()
            
            if not body or 'usuario' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'usuario' é obrigatório!"})

            usuario = body['usuario']

            # Apenas verificar existência dos campos obrigatórios
            campos_obrigatorios = ["nome", "email", "senha_hash"]
            for campo in campos_obrigatorios:
                if campo not in usuario:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_body_update(self, f):
        """
        Decorator para validar o corpo da requisição para atualização de usuário.

        Verifica apenas a existência:
        - O objeto 'usuario' existe
        - Campos obrigatórios: nome, email
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 UsuarioMiddleware.validate_body_update()")
            body = request.get_json()
            
            if not body or 'usuario' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'usuario' é obrigatório!"})

            usuario = body['usuario']

            # Campos obrigatórios para atualização
            campos_obrigatorios = ["nome", "email"]
            for campo in campos_obrigatorios:
                if campo not in usuario:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_login_body(self, f):
        """
        Decorator para validar o corpo da requisição para login de um usuário.

        Verifica apenas a existência:
        - O objeto 'usuario' existe
        - Campos obrigatórios: email, senha
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 UsuarioMiddleware.validate_login_body()")
            body = request.get_json()

            if not body or 'usuario' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'usuario' é obrigatório!"})

            usuario = body['usuario']

            # ✅ CORREÇÃO CRÍTICA: Mudar de "senha_hash" para "senha"
            campos_obrigatorios = ["email", "senha"]
            for campo in campos_obrigatorios:
                if campo not in usuario:
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
            print("🔷 UsuarioMiddleware.validate_id_param()")
            if 'id' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'id' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function