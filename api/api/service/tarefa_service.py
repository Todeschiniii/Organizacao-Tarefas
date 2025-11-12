# -*- coding: utf-8 -*-
from api.dao.tarefa_dao import TarefaDAO
from api.dao.projeto_dao import ProjetoDAO
from api.model.tarefa import Tarefa
from api.utils.error_response import ErrorResponse


"""
Classe responsável pela camada de serviço para a entidade Tarefa.
"""
class TarefaService:
    def __init__(self, tarefa_dao_dependency: TarefaDAO, projeto_dao_dependency: ProjetoDAO):
        print("⬆️  TarefaService.__init__()")
        self.__tarefaDAO = tarefa_dao_dependency
        self.__projetoDAO = projeto_dao_dependency

    def createTarefa(self, jsonTarefa: dict) -> int:
        """
        Cria uma nova tarefa.
        """
        print("🟣 TarefaService.createTarefa()")

        objTarefa = Tarefa()
        objTarefa.titulo = jsonTarefa["titulo"]
        objTarefa.concluida = jsonTarefa.get("concluida", False)
        
        # ✅ CORREÇÃO: data_limite pode ser None ou string
        data_limite = jsonTarefa.get("data_limite")
        objTarefa.data_limite = data_limite if data_limite else None
        
        objTarefa.projeto_id = jsonTarefa["projeto_id"]

        # regra de negócio: validar se projeto existe
        projetoExiste = self.__projetoDAO.findByField("id", objTarefa.projeto_id)
        if not projetoExiste or len(projetoExiste) == 0:
            raise ErrorResponse(
                400,
                "Projeto não encontrado",
                {"message": f"O projeto com ID {objTarefa.projeto_id} não existe"}
            )

        return self.__tarefaDAO.create(objTarefa)

    def findAll(self) -> list[dict]:
        """
        Retorna todas as tarefas.
        """
        print("🟣 TarefaService.findAll()")
        return self.__tarefaDAO.findAll()

    def findById(self, id: int) -> dict:
        """
        Busca tarefa por ID.
        """
        tarefa = self.__tarefaDAO.findById(id)
        if not tarefa:
            raise ErrorResponse(
                404,
                "Tarefa não encontrada",
                {"message": f"Não existe tarefa com id {id}"}
            )
        return tarefa

    def updateTarefa(self, id: int, requestBody: dict) -> bool:
        """
        Atualiza dados de uma tarefa.
        """
        print("🟣 TarefaService.updateTarefa()")

        jsonTarefa = requestBody["tarefa"]

        objTarefa = Tarefa()
        objTarefa.id = id
        objTarefa.titulo = jsonTarefa["titulo"]
        objTarefa.concluida = jsonTarefa["concluida"]
        
        # ✅ CORREÇÃO: data_limite pode ser None ou string
        data_limite = jsonTarefa.get("data_limite")
        objTarefa.data_limite = data_limite if data_limite else None
        
        objTarefa.projeto_id = jsonTarefa.get("projeto_id")

        return self.__tarefaDAO.update(objTarefa)

    def deleteTarefa(self, id: int) -> bool:
        """
        Remove tarefa por ID.
        """
        print("🟣 TarefaService.deleteTarefa()")
        return self.__tarefaDAO.delete(id)

    def findByProjetoId(self, projeto_id: int) -> list[dict]:
        """
        Busca tarefas por ID do projeto.
        """
        print("🟣 TarefaService.findByProjetoId()")
        
        # Verifica se o projeto existe
        projetoExiste = self.__projetoDAO.findByField("id", projeto_id)
        if not projetoExiste or len(projetoExiste) == 0:
            raise ErrorResponse(
                404,
                "Projeto não encontrado",
                {"message": f"Não existe projeto com id {projeto_id}"}
            )

        return self.__tarefaDAO.findByProjetoId(projeto_id)

    def marcarComoConcluida(self, id: int) -> bool:
        """
        Marca uma tarefa como concluída.
        """
        print("🟣 TarefaService.marcarComoConcluida()")
        
        # Verifica se a tarefa existe
        tarefaExiste = self.__tarefaDAO.findById(id)
        if not tarefaExiste:
            raise ErrorResponse(
                404,
                "Tarefa não encontrada",
                {"message": f"Não existe tarefa com id {id}"}
            )

        return self.__tarefaDAO.marcarComoConcluida(id)