# control/usuario_control.py
from flask import request, jsonify
import traceback
from api.service.usuario_service import UsuarioService
from api.utils.error_response import ErrorResponse

class UsuarioControl:
    def __init__(self, usuario_service: UsuarioService):
        """
        Construtor da classe UsuarioControl
        :param usuario_service: Instância do UsuarioService (injeção de dependência)
        """
        print("⬆️  UsuarioControl.constructor()")
        self.__usuario_service = usuario_service

    def login(self):
        """Autentica um usuário pelo email e senha"""
        print("🔵 UsuarioControl.login()")
        try:
            json_usuario = request.json.get("usuario")
            if not json_usuario:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Dados do usuário não fornecidos",
                        "code": 400
                    }
                }), 400

            resultado = self.__usuario_service.loginUsuario(json_usuario)
            return jsonify({
                "success": True,
                "message": "Login efetuado com sucesso!",
                "data": resultado
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
            print(f"❌ Erro inesperado em login: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def store(self):
        """Cria um novo usuário"""
        print("🔵 UsuarioControl.store()")
        try:
            json_usuario = request.json.get("usuario")
            if not json_usuario:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Dados do usuário não fornecidos",
                        "code": 400
                    }
                }), 400

            newIdUsuario = self.__usuario_service.createUsuario(json_usuario)
            return jsonify({
                "success": True,
                "message": "Cadastro realizado com sucesso",
                "data": {
                    "usuario": {
                        "id": newIdUsuario,
                        "nome": json_usuario.get("nome"),
                        "email": json_usuario.get("email")
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
        """Lista todos os usuários cadastrados"""
        print("🔵 UsuarioControl.index()")
        try:
            lista_usuarios = self.__usuario_service.findAll()
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"usuarios": lista_usuarios}
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
            print(f"❌ Erro inesperado em index: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def show(self, id):
        """Busca um usuário pelo ID"""
        print("🔵 UsuarioControl.show()")
        try:
            usuario = self.__usuario_service.findById(id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": usuario
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
        """Atualiza os dados de um usuário existente"""
        print("🔵 UsuarioControl.update()")
        try:
            usuario_atualizado = self.__usuario_service.updateUsuario(id, request.json)

            return jsonify({
                "success": True,
                "message": "Atualizado com sucesso",
                "data": {
                    "usuario": {
                        "id": int(id),
                        "nome": request.json.get("usuario", {}).get("nome"),
                        "email": request.json.get("usuario", {}).get("email")
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
        """Remove um usuário pelo ID"""
        print("🔵 UsuarioControl.destroy()")
        try:
            excluiu = self.__usuario_service.deleteUsuario(id)
            return jsonify({
                "success": True,
                "message": "Excluído com sucesso"
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