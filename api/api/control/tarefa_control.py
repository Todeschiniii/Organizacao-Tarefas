# -*- coding: utf-8 -*-
from flask import request, jsonify
import traceback
from api.service.tarefa_service import TarefaService
from api.utils.error_response import ErrorResponse

"""
Classe responsável por controlar os endpoints da API REST para a entidade Tarefa.

Implementa métodos de CRUD, utilizando injeção de dependência
para receber a instância de TarefaService, desacoplando a lógica de negócio
da camada de controle.
"""
class TarefaControl:
    def __init__(self, tarefa_service: TarefaService):
        """
        Construtor da classe TarefaControl
        :param tarefa_service: Instância do TarefaService (injeção de dependência)
        """
        print("⬆️  TarefaControl.constructor()")
        self.__tarefa_service = tarefa_service

    def store(self):
        """Cria uma nova tarefa"""
        print("🔵 TarefaControl.store()")
        try:
            json_tarefa = request.json.get("tarefa")
            newIdTarefa = self.__tarefa_service.createTarefa(json_tarefa)
            return jsonify({
                "success": True,
                "message": "Tarefa criada com sucesso",
                "data": {
                    "tarefa": {
                        "id": newIdTarefa,
                        "titulo": json_tarefa.get("titulo"),
                        "concluida": json_tarefa.get("concluida", False),
                        "data_limite": json_tarefa.get("data_limite"),
                        "projeto_id": json_tarefa.get("projeto_id")
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
        """Lista todas as tarefas cadastradas"""
        print("🔵 TarefaControl.index()")
        try:
            lista_tarefas = self.__tarefa_service.findAll()
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"tarefas": lista_tarefas}
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
        """Busca uma tarefa pelo ID"""
        print("🔵 TarefaControl.show()")
        try:
            tarefa = self.__tarefa_service.findById(id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": tarefa
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
        """Atualiza os dados de uma tarefa existente"""
        print("🔵 TarefaControl.update()")
        try:
            tarefa_atualizada = self.__tarefa_service.updateTarefa(id, request.json)

            return jsonify({
                "success": True,
                "message": "Tarefa atualizada com sucesso",
                "data": {
                    "tarefa": {
                        "id": int(id),
                        "titulo": request.json.get("tarefa", {}).get("titulo"),
                        "concluida": request.json.get("tarefa", {}).get("concluida")
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
        """Remove uma tarefa pelo ID"""
        print("🔵 TarefaControl.destroy()")
        try:
            excluiu = self.__tarefa_service.deleteTarefa(id)
            return jsonify({
                "success": True,
                "message": "Tarefa excluída com sucesso"
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

    def show_by_projeto(self, projeto_id):
        """Lista todas as tarefas de um projeto específico"""
        print("🔵 TarefaControl.show_by_projeto()")
        try:
            tarefas = self.__tarefa_service.findByProjetoId(projeto_id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"tarefas": tarefas}
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
            print(f"❌ Erro inesperado em show_by_projeto: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def marcar_concluida(self, id):
        """Marca uma tarefa como concluída"""
        print("🔵 TarefaControl.marcar_concluida()")
        try:
            tarefa_concluida = self.__tarefa_service.marcarComoConcluida(id)
            
            return jsonify({
                "success": True,
                "message": "Tarefa marcada como concluída",
                "data": {
                    "tarefa": {
                        "id": int(id),
                        "concluida": True
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
            print(f"❌ Erro inesperado em marcar_concluida: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500