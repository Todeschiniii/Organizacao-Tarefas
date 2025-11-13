# -*- coding: utf-8 -*-
from api.dao.projeto_dao import ProjetoDAO
from api.dao.usuario_dao import UsuarioDAO
from api.model.projeto import Projeto
from api.utils.error_response import ErrorResponse
import traceback
from datetime import datetime


"""
Classe responsável pela camada de serviço para a entidade Projeto.

Observações sobre injeção de dependência:
- O ProjetoService recebe instâncias de ProjetoDAO e UsuarioDAO via construtor.
- Isso desacopla o serviço das implementações concretas dos DAOs.
- Facilita testes unitários e uso de mocks.
"""
class ProjetoService:
    def __init__(self, projeto_dao_dependency: ProjetoDAO, usuario_dao_dependency: UsuarioDAO):
        """
        Construtor da classe ProjetoService

        :param projeto_dao_dependency: ProjetoDAO
        :param usuario_dao_dependency: UsuarioDAO
        """
        print("⬆️  ProjetoService.__init__()")
        self.__projetoDAO = projeto_dao_dependency
        self.__usuarioDAO = usuario_dao_dependency

    def createProjeto(self, jsonProjeto: dict) -> int:
        """
        Cria um novo projeto.
        """
        print("🟣 ProjetoService.createProjeto()")

        try:
            objProjeto = Projeto()
            objProjeto.nome = jsonProjeto["nome"]
            objProjeto.descricao = jsonProjeto.get("descricao")
            objProjeto.data_inicio = jsonProjeto.get("data_inicio")
            objProjeto.data_fim = jsonProjeto.get("data_fim")  # ✅ CORREÇÃO: Adicionar data_fim
            objProjeto.status = jsonProjeto.get("status", "pendente")
            objProjeto.usuario_id = jsonProjeto["usuario_id"]

            # ✅ CORREÇÃO: Verifica se usuário existe - find_by_id retorna Usuario ou None
            usuarioExiste = self.__usuarioDAO.find_by_id(objProjeto.usuario_id)
            if not usuarioExiste:  # ✅ CORREÇÃO: Removeu o len()
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

    def findAll(self) -> list[dict]:
        """
        Retorna todos os projetos.
        """
        print("🟣 ProjetoService.findAll()")
        try:
            return self.__projetoDAO.findAll()
        except Exception as e:
            print(f"❌ Erro inesperado em findAll: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse("Erro interno ao buscar projetos", 500)

    def findById(self, id: int) -> dict:
        """
        Busca projeto por ID.

        :param id: int
        :return: dict
        :raises ErrorResponse: se projeto não for encontrado
        """
        try:
            projeto = self.__projetoDAO.findById(id)
            if not projeto:
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

    def updateProjeto(self, id: int, requestBody: dict) -> bool:
        """
        Atualiza dados de um projeto.

        :param id: int
        :param requestBody: dict {"projeto": {...}}
        :return: bool
        """
        print("🟣 ProjetoService.updateProjeto()")

        try:
            jsonProjeto = requestBody["projeto"]

            objProjeto = Projeto()
            objProjeto.id = id
            objProjeto.nome = jsonProjeto["nome"]
            objProjeto.descricao = jsonProjeto.get("descricao")
            objProjeto.data_inicio = jsonProjeto.get("data_inicio")
            objProjeto.status = jsonProjeto["status"]
            objProjeto.usuario_id = jsonProjeto.get("usuario_id")

            # ✅ CORREÇÃO: Verifica se usuário existe se usuario_id foi fornecido
            if objProjeto.usuario_id:
                usuarioExiste = self.__usuarioDAO.find_by_id(objProjeto.usuario_id)
                if not usuarioExiste:  # ✅ CORREÇÃO: Removeu o len()
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

    def deleteProjeto(self, id: int) -> bool:
        """
        Remove projeto por ID.

        :param id: int
        :return: bool
        """
        print("🟣 ProjetoService.deleteProjeto()")
        try:
            return self.__projetoDAO.delete(id)
        except Exception as e:
            print(f"❌ Erro inesperado em deleteProjeto: {e}")
            print(f"🔍 Stack trace: {traceback.format_exc()}")
            raise ErrorResponse(f"Erro interno ao excluir projeto: {str(e)}", 500)

    def findByUsuarioId(self, usuario_id: int) -> list[dict]:
        """
        Busca projetos por ID do usuário.

        :param usuario_id: int
        :return: list[dict]
        :raises ErrorResponse: se usuário não for encontrado
        """
        print("🟣 ProjetoService.findByUsuarioId()")
        
        try:
            # ✅ CORREÇÃO: Verifica se o usuário existe - find_by_id retorna Usuario ou None
            usuarioExiste = self.__usuarioDAO.find_by_id(usuario_id)
            if not usuarioExiste:  # ✅ CORREÇÃO: Removeu o len()
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