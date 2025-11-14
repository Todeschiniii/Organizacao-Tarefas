# -*- coding: utf-8 -*-
from api.dao.projeto_dao import ProjetoDAO
from api.dao.usuario_dao import UsuarioDAO
from api.model.projeto import Projeto
from api.utils.error_response import ErrorResponse
import traceback
from datetime import datetime

class ProjetoService:
    def __init__(self, projeto_dao_dependency: ProjetoDAO, usuario_dao_dependency: UsuarioDAO):
        print("⬆️  ProjetoService.__init__()")
        self.__projetoDAO = projeto_dao_dependency
        self.__usuarioDAO = usuario_dao_dependency

    def createProjeto(self, jsonProjeto: dict, usuario_id: int = None) -> int:
        """
        Cria um novo projeto.
        Se usuario_id for fornecido, garante que o projeto seja criado para esse usuário.
        """
        print("🟣 ProjetoService.createProjeto()")
        print(f"📝 Dados recebidos para criar projeto: {jsonProjeto}")

        try:
            objProjeto = Projeto()
            objProjeto.nome = jsonProjeto["nome"]
            objProjeto.descricao = jsonProjeto.get("descricao")
            objProjeto.data_inicio = jsonProjeto.get("data_inicio")
            objProjeto.data_fim = jsonProjeto.get("data_fim")
            objProjeto.status = jsonProjeto.get("status", "pendente")
            
            # ✅ CORREÇÃO: Define o usuario_id do usuário autenticado
            if usuario_id:
                objProjeto.usuario_id = usuario_id
            else:
                objProjeto.usuario_id = jsonProjeto.get("usuario_id")

            # Verifica se usuário existe
            usuarioExiste = self.__usuarioDAO.find_by_id(objProjeto.usuario_id)
            if not usuarioExiste:
                raise ErrorResponse(
                    400,
                    "Usuário não encontrado",
                    {"message": f"O usuário com ID {objProjeto.usuario_id} não existe"}
                )

            return self.__projetoDAO.create(objProjeto)

        except ValueError as e:
            print(f"❌ Erro de validação em createProjeto: {e}")
            raise ErrorResponse(str(e), 400)
        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em createProjeto: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(f"Erro interno ao criar projeto: {str(e)}", 500)

    def findAll(self, usuario_id: int = None) -> list[dict]:
        """
        Retorna todos os projetos.
        Se usuario_id for fornecido, retorna apenas projetos desse usuário.
        """
        print("🟣 ProjetoService.findAll()")
        try:
            return self.__projetoDAO.findAll(usuario_id)
        except Exception as e:
            print(f"❌ Erro inesperado em findAll: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao buscar projetos", 500)

    def findById(self, id: int, usuario_id: int = None) -> dict:
        """
        Busca projeto por ID.
        Se usuario_id for fornecido, só retorna se o projeto pertencer ao usuário.
        """
        try:
            projeto = self.__projetoDAO.findById(id, usuario_id)
            if not projeto:
                if usuario_id:
                    raise ErrorResponse(
                        404,
                        "Projeto não encontrado",
                        {"message": f"Não existe projeto com id {id} para o usuário {usuario_id}"}
                    )
                else:
                    raise ErrorResponse(
                        404,
                        "Projeto não encontrado",
                        {"message": f"Não existe projeto com id {id}"}
                    )
            return projeto
        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em findById: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao buscar projeto", 500)

    def updateProjeto(self, id: int, requestBody: dict, usuario_id: int = None) -> bool:
        """
        Atualiza dados de um projeto.
        Se usuario_id for fornecido, só atualiza se o projeto pertencer ao usuário.
        """
        print("🟣 ProjetoService.updateProjeto()")
        print(f"📝 Dados recebidos para atualizar projeto {id}: {requestBody}")

        try:
            jsonProjeto = requestBody["projeto"]

            objProjeto = Projeto()
            objProjeto.id = id
            objProjeto.nome = jsonProjeto["nome"]
            objProjeto.descricao = jsonProjeto.get("descricao")
            objProjeto.data_inicio = jsonProjeto.get("data_inicio")
            objProjeto.data_fim = jsonProjeto.get("data_fim")
            objProjeto.status = jsonProjeto["status"]
            
            # ✅ CORREÇÃO: Define o usuario_id do usuário autenticado
            if usuario_id:
                objProjeto.usuario_id = usuario_id
            else:
                objProjeto.usuario_id = jsonProjeto.get("usuario_id")

            # Verifica se usuário existe se usuario_id foi fornecido
            if objProjeto.usuario_id:
                usuarioExiste = self.__usuarioDAO.find_by_id(objProjeto.usuario_id)
                if not usuarioExiste:
                    raise ErrorResponse(
                        400,
                        "Usuário não encontrado",
                        {"message": f"O usuário com ID {objProjeto.usuario_id} não existe"}
                    )

            return self.__projetoDAO.update(objProjeto)

        except ValueError as e:
            print(f"❌ Erro de validação em updateProjeto: {e}")
            raise ErrorResponse(str(e), 400)
        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em updateProjeto: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(f"Erro interno ao atualizar projeto: {str(e)}", 500)

    def deleteProjeto(self, id: int, usuario_id: int = None) -> bool:
        """
        Remove projeto por ID.
        Se usuario_id for fornecido, só deleta se o projeto pertencer ao usuário.
        """
        print("🟣 ProjetoService.deleteProjeto()")
        try:
            return self.__projetoDAO.delete(id, usuario_id)
        except Exception as e:
            print(f"❌ Erro inesperado em deleteProjeto: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(f"Erro interno ao excluir projeto: {str(e)}", 500)

    def findByUsuarioId(self, usuario_id: int) -> list[dict]:
        """
        Busca projetos por ID do usuário.
        """
        print("🟣 ProjetoService.findByUsuarioId()")
        
        try:
            # Verifica se o usuário existe
            usuarioExiste = self.__usuarioDAO.find_by_id(usuario_id)
            if not usuarioExiste:
                raise ErrorResponse(
                    404,
                    "Usuário não encontrado",
                    {"message": f"Não existe usuário com id {usuario_id}"}
                )

            return self.__projetoDAO.findByUsuarioId(usuario_id)
        except ErrorResponse:
            raise
        except Exception as e:
            print(f"❌ Erro inesperado em findByUsuarioId: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao buscar projetos do usuário", 500)