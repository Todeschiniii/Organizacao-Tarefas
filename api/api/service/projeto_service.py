# -*- coding: utf-8 -*-
from api.dao.projeto_dao import ProjetoDAO
from api.dao.usuario_dao import UsuarioDAO
from api.model.projeto import Projeto
from api.utils.error_response import ErrorResponse


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

        :param jsonProjeto: dict contendo dados do projeto
        :return: int ID do projeto criado
        :raises ErrorResponse: se usuário não existir
        """
        print("🟣 ProjetoService.createProjeto()")

        objProjeto = Projeto()
        objProjeto.nome = jsonProjeto["nome"]
        objProjeto.descricao = jsonProjeto.get("descricao")
        objProjeto.data_inicio = jsonProjeto.get("data_inicio")
        objProjeto.status = jsonProjeto.get("status", "Pendente")
        objProjeto.usuario_id = jsonProjeto["usuario_id"]

        # regra de negócio: validar se usuário existe
        usuarioExiste = self.__usuarioDAO.findByField("id", objProjeto.usuario_id)
        if not usuarioExiste or len(usuarioExiste) == 0:
            raise ErrorResponse(
                400,
                "Usuário não encontrado",
                {"message": f"O usuário com ID {objProjeto.usuario_id} não existe"}
            )

        return self.__projetoDAO.create(objProjeto)

    def findAll(self) -> list[dict]:
        """
        Retorna todos os projetos.
        """
        print("🟣 ProjetoService.findAll()")
        return self.__projetoDAO.findAll()

    def findById(self, id: int) -> dict:
        """
        Busca projeto por ID.

        :param id: int
        :return: dict
        :raises ErrorResponse: se projeto não for encontrado
        """
        projeto = self.__projetoDAO.findById(id)
        if not projeto:
            raise ErrorResponse(
                404,
                "Projeto não encontrado",
                {"message": f"Não existe projeto com id {id}"}
            )
        return projeto

    def updateProjeto(self, id: int, requestBody: dict) -> bool:
        """
        Atualiza dados de um projeto.

        :param id: int
        :param requestBody: dict {"projeto": {...}}
        :return: bool
        """
        print("🟣 ProjetoService.updateProjeto()")

        jsonProjeto = requestBody["projeto"]

        objProjeto = Projeto()
        objProjeto.id = id
        objProjeto.nome = jsonProjeto["nome"]
        objProjeto.descricao = jsonProjeto.get("descricao")
        objProjeto.data_inicio = jsonProjeto.get("data_inicio")
        objProjeto.status = jsonProjeto["status"]
        objProjeto.usuario_id = jsonProjeto.get("usuario_id")

        return self.__projetoDAO.update(objProjeto)

    def deleteProjeto(self, id: int) -> bool:
        """
        Remove projeto por ID.

        :param id: int
        :return: bool
        """
        print("🟣 ProjetoService.deleteProjeto()")
        return self.__projetoDAO.delete(id)

    def findByUsuarioId(self, usuario_id: int) -> list[dict]:
        """
        Busca projetos por ID do usuário.

        :param usuario_id: int
        :return: list[dict]
        :raises ErrorResponse: se usuário não for encontrado
        """
        print("🟣 ProjetoService.findByUsuarioId()")
        
        # Verifica se o usuário existe
        usuarioExiste = self.__usuarioDAO.findByField("id", usuario_id)
        if not usuarioExiste or len(usuarioExiste) == 0:
            raise ErrorResponse(
                404,
                "Usuário não encontrado",
                {"message": f"Não existe usuário com id {usuario_id}"}
            )

        return self.__projetoDAO.findByUsuarioId(usuario_id)