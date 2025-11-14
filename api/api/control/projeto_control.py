# -*- coding: utf-8 -*-
from flask import request, jsonify
import traceback
from api.service.projeto_service import ProjetoService
from api.utils.error_response import ErrorResponse


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

    def store(self, usuario_id: int = None):
        """Cria um novo projeto para o usuário autenticado"""
        print("🔵 ProjetoControl.store()")
        try:
            json_projeto = request.json.get("projeto")
            if not json_projeto:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Dados do projeto não fornecidos",
                        "code": 400
                    }
                }), 400

            # ✅ CORREÇÃO: Passa o usuario_id do usuário autenticado
            newIdProjeto = self.__projeto_service.createProjeto(json_projeto, usuario_id)
            
            return jsonify({
                "success": True,
                "message": "Projeto criado com sucesso",
                "data": {
                    "projeto": {
                        "id": newIdProjeto,
                        "nome": json_projeto.get("nome"),
                        "descricao": json_projeto.get("descricao"),
                        "data_inicio": json_projeto.get("data_inicio"),
                        "data_fim": json_projeto.get("data_fim"),
                        "status": json_projeto.get("status", "pendente"),
                        "usuario_id": usuario_id  # ✅ CORREÇÃO: Retorna o usuario_id correto
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

    def index(self, usuario_id: int = None):
        """Lista todos os projetos do usuário autenticado"""
        print("🔵 ProjetoControl.index()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para buscar apenas projetos do usuário
            lista_projetos = self.__projeto_service.findAll(usuario_id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"projetos": lista_projetos}
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

    def show(self, id, usuario_id: int = None):
        """Busca um projeto pelo ID (só retorna se pertencer ao usuário)"""
        print("🔵 ProjetoControl.show()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para verificar permissão
            projeto = self.__projeto_service.findById(id, usuario_id)
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

    def update(self, id, usuario_id: int = None):
        """Atualiza os dados de um projeto existente (só se pertencer ao usuário)"""
        print("🔵 ProjetoControl.update()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para verificar permissão
            projeto_atualizado = self.__projeto_service.updateProjeto(id, request.json, usuario_id)

            return jsonify({
                "success": True,
                "message": "Projeto atualizado com sucesso",
                "data": {
                    "projeto": {
                        "id": int(id),
                        "nome": request.json.get("projeto", {}).get("nome"),
                        "descricao": request.json.get("projeto", {}).get("descricao"),
                        "data_inicio": request.json.get("projeto", {}).get("data_inicio"),
                        "data_fim": request.json.get("projeto", {}).get("data_fim"),
                        "status": request.json.get("projeto", {}).get("status"),
                        "usuario_id": usuario_id  # ✅ CORREÇÃO: Retorna o usuario_id correto
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

    def destroy(self, id, usuario_id: int = None):
        """Remove um projeto pelo ID (só se pertencer ao usuário)"""
        print("🔵 ProjetoControl.destroy()")
        try:
            # ✅ CORREÇÃO: Passa o usuario_id para verificar permissão
            excluiu = self.__projeto_service.deleteProjeto(id, usuario_id)
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

    def show_meus_projetos(self, usuario_id: int):
        """Lista todos os projetos do usuário autenticado"""
        print("🔵 ProjetoControl.show_meus_projetos()")
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
            print(f"❌ Erro inesperado em show_meus_projetos: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def count_projetos(self, usuario_id: int = None):
        """Retorna a contagem de projetos do usuário"""
        print("🔵 ProjetoControl.count_projetos()")
        try:
            if usuario_id:
                projetos = self.__projeto_service.findByUsuarioId(usuario_id)
                total = len(projetos)
                
                # Contar por status
                status_count = {}
                for projeto in projetos:
                    status = projeto.get('status', 'pendente')
                    status_count[status] = status_count.get(status, 0) + 1
            else:
                projetos = self.__projeto_service.findAll()
                total = len(projetos)
                status_count = {"total": total}

            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {
                    "total": total,
                    "por_status": status_count
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
            print(f"❌ Erro inesperado em count_projetos: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def update_status(self, id, usuario_id: int = None):
        """Atualiza apenas o status de um projeto"""
        print("🔵 ProjetoControl.update_status()")
        try:
            json_data = request.json.get("projeto", {})
            novo_status = json_data.get("status")
            
            if not novo_status:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Status não fornecido",
                        "code": 400
                    }
                }), 400

            # Busca o projeto atual
            projeto_atual = self.__projeto_service.findById(id, usuario_id)
            if not projeto_atual:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Projeto não encontrado",
                        "code": 404
                    }
                }), 404

            # Atualiza apenas o status
            dados_atualizacao = {
                "projeto": {
                    "nome": projeto_atual.get("nome"),
                    "descricao": projeto_atual.get("descricao"),
                    "data_inicio": projeto_atual.get("data_inicio"),
                    "data_fim": projeto_atual.get("data_fim"),
                    "status": novo_status,
                    "usuario_id": usuario_id
                }
            }

            projeto_atualizado = self.__projeto_service.updateProjeto(id, dados_atualizacao, usuario_id)

            return jsonify({
                "success": True,
                "message": f"Status do projeto atualizado para '{novo_status}'",
                "data": {
                    "projeto": {
                        "id": int(id),
                        "status": novo_status
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
            print(f"❌ Erro inesperado em update_status: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def search_projetos(self, usuario_id: int = None):
        """Busca projetos por termo (nome ou descrição)"""
        print("🔵 ProjetoControl.search_projetos()")
        try:
            termo = request.args.get('q', '').strip()
            if not termo:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": "Termo de busca não fornecido",
                        "code": 400
                    }
                }), 400

            # Busca todos os projetos do usuário
            projetos = self.__projeto_service.findAll(usuario_id)
            
            # Filtra por termo
            projetos_filtrados = []
            for projeto in projetos:
                nome = projeto.get('nome', '').lower()
                descricao = projeto.get('descricao', '').lower()
                termo_lower = termo.lower()
                
                if termo_lower in nome or termo_lower in descricao:
                    projetos_filtrados.append(projeto)

            return jsonify({
                "success": True,
                "message": "Busca realizada com sucesso",
                "data": {
                    "projetos": projetos_filtrados,
                    "total_encontrado": len(projetos_filtrados),
                    "termo_busca": termo
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
            print(f"❌ Erro inesperado em search_projetos: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def get_projetos_recentes(self, usuario_id: int = None, limite: int = 5):
        """Retorna os projetos mais recentes do usuário"""
        print("🔵 ProjetoControl.get_projetos_recentes()")
        try:
            projetos = self.__projeto_service.findAll(usuario_id)
            
            # Ordena por data de criação (mais recentes primeiro) e limita
            projetos_ordenados = sorted(
                projetos, 
                key=lambda x: x.get('data_criacao', ''), 
                reverse=True
            )[:limite]

            return jsonify({
                "success": True,
                "message": "Projetos recentes recuperados com sucesso",
                "data": {
                    "projetos": projetos_ordenados,
                    "total": len(projetos_ordenados)
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
            print(f"❌ Erro inesperado em get_projetos_recentes: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500