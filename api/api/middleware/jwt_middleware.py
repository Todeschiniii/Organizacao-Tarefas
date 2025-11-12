# -*- coding: utf-8 -*-
from flask import request, jsonify
from functools import wraps
from api.http.meu_token_jwt import MeuTokenJWT


class JwtMiddleware:
    """
    Middleware Flask para validação de tokens JWT.
    
    Implementa validação de token JWT para proteger endpoints da API.
    Utiliza injeção de dependência para receber a instância de MeuTokenJWT.
    """

    def __init__(self, jwt_instance: MeuTokenJWT = None):
        """
        Construtor do JwtMiddleware.
        
        :param jwt_instance: Instância de MeuTokenJWT (opcional)
        """
        print("⬆️  JwtMiddleware.__init__()")
        self.__jwt_instance = jwt_instance or MeuTokenJWT()

    def validate_token(self, f):
        """
        Decorator para validar token JWT em endpoints protegidos.
        
        Verifica:
        - Presença do header Authorization
        - Validade do token JWT
        - Expiração do token
        
        :param f: Função a ser decorada
        :return: Função decorada ou resposta de erro 401
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 JwtMiddleware.validate_token()")
            
            # Obtém o header Authorization
            authorization_header = request.headers.get("Authorization")
            
            if not authorization_header:
                print("❌ Header Authorization não encontrado")
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Token de autenticação não fornecido",
                        "code": 401
                    }
                }), 401

            # Valida o token
            if self.__jwt_instance.validarToken(authorization_header):
                print(f"✅ Token válido para: {self.__jwt_instance.payload.get('email', 'Unknown')}")
                return f(*args, **kwargs)
            else:
                print("❌ Token inválido ou expirado")
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Token inválido ou expirado",
                        "code": 401
                    }
                }), 401

        return decorated_function

    def obter_dados_usuario(self):
        """
        Retorna os dados do usuário a partir do token validado.
        
        :return: dict com dados do usuário ou None se não houver token válido
        """
        if not self.__jwt_instance.payload:
            return None
        
        return {
            "id": self.__jwt_instance.payload.get("idFuncionario"),
            "email": self.__jwt_instance.payload.get("email"),
            "name": self.__jwt_instance.payload.get("name"),
            "role": self.__jwt_instance.payload.get("role")
        }

    def validate_token_and_role(self, allowed_roles: list):
        """
        Decorator para validar token JWT e papel do usuário.
        
        :param allowed_roles: Lista de roles permitidos
        :return: Função decorada
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                print(f"🔷 JwtMiddleware.validate_token_and_role() - Roles: {allowed_roles}")
                
                # Primeiro valida o token
                authorization_header = request.headers.get("Authorization")
                
                if not authorization_header:
                    return jsonify({
                        "success": False,
                        "error": {
                            "message": "Token de autenticação não fornecido",
                            "code": 401
                        }
                    }), 401

                if not self.__jwt_instance.validarToken(authorization_header):
                    return jsonify({
                        "success": False,
                        "error": {
                            "message": "Token inválido ou expirado",
                            "code": 401
                        }
                    }), 401

                # Verifica se o role do usuário está permitido
                user_role = self.__jwt_instance.payload.get("role")
                if user_role not in allowed_roles:
                    print(f"❌ Acesso negado. Role: {user_role}, Permitidos: {allowed_roles}")
                    return jsonify({
                        "success": False,
                        "error": {
                            "message": "Acesso não autorizado para este recurso",
                            "code": 403
                        }
                    }), 403

                print(f"✅ Acesso permitido para role: {user_role}")
                return f(*args, **kwargs)

            return decorated_function
        return decorator

    def get_user_id(self):
        """
        Retorna o ID do usuário a partir do token validado.
        
        :return: int ID do usuário ou None
        """
        if not self.__jwt_instance.payload:
            return None
        return self.__jwt_instance.payload.get("idFuncionario")

    def get_user_email(self):
        """
        Retorna o email do usuário a partir do token validado.
        
        :return: str Email do usuário ou None
        """
        if not self.__jwt_instance.payload:
            return None
        return self.__jwt_instance.payload.get("email")


# Exemplo de uso
if __name__ == "__main__":
    # Teste do middleware
    from flask import Flask
    
    app = Flask(__name__)
    jwt_middleware = JwtMiddleware()
    
    @app.route('/api/protegido')
    @jwt_middleware.validate_token
    def rota_protegida():
        return jsonify({
            "success": True,
            "message": "Acesso permitido!",
            "data": {
                "user": jwt_middleware.obter_dados_usuario()
            }
        })
    
    @app.route('/api/admin')
    @jwt_middleware.validate_token_and_role(["admin", "gerente"])
    def rota_admin():
        return jsonify({
            "success": True,
            "message": "Acesso admin permitido!"
        })
    
    print("✅ JwtMiddleware configurado com sucesso!")