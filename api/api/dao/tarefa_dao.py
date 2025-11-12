# -*- coding: utf-8 -*-
from api.model.tarefa import Tarefa

"""
Classe responsável por gerenciar operações CRUD
para a entidade Tarefa no banco de dados.
"""

class TarefaDAO:
    def __init__(self, database_dependency):
        print("⬆️  TarefaDAO.__init__()")
        self.__database = database_dependency
        # ✅ REMOVIDO: self._create_tables() - tabelas já existem do Banco.sql

    def create(self, objTarefa: Tarefa) -> int:
        print("🟢 TarefaDAO.create()")
        try:
            # ✅ CORREÇÃO: Query atualizada com as novas colunas
            SQL = """
                INSERT INTO tarefas 
                (titulo, descricao, status, prioridade, concluida, data_limite, data_inicio, data_fim, projeto_id, usuario_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                objTarefa.titulo,
                objTarefa.descricao if hasattr(objTarefa, 'descricao') else "",
                objTarefa.status if hasattr(objTarefa, 'status') else "pendente",
                objTarefa.prioridade if hasattr(objTarefa, 'prioridade') else "media",
                objTarefa.concluida,
                objTarefa.data_limite,
                objTarefa.data_inicio if hasattr(objTarefa, 'data_inicio') else None,
                objTarefa.data_fim if hasattr(objTarefa, 'data_fim') else None,
                objTarefa.projeto_id,
                objTarefa.usuario_id if hasattr(objTarefa, 'usuario_id') else None,
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir tarefa")
            return insert_id
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.create(): {e}")
            raise

    def delete(self, id: int) -> bool:
        print("🟢 TarefaDAO.delete()")
        try:
            SQL = "DELETE FROM tarefas WHERE id = %s"
            affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.delete(): {e}")
            raise

    def update(self, objTarefa: Tarefa) -> bool:
        print("🟢 TarefaDAO.update()")
        try:
            # ✅ CORREÇÃO: Query atualizada com as novas colunas
            SQL = """
                UPDATE tarefas 
                SET titulo=%s, descricao=%s, status=%s, prioridade=%s, concluida=%s, 
                    data_limite=%s, data_inicio=%s, data_fim=%s, projeto_id=%s, usuario_id=%s 
                WHERE id=%s
            """
            params = (
                objTarefa.titulo,
                objTarefa.descricao if hasattr(objTarefa, 'descricao') else "",
                objTarefa.status if hasattr(objTarefa, 'status') else "pendente",
                objTarefa.prioridade if hasattr(objTarefa, 'prioridade') else "media",
                objTarefa.concluida,
                objTarefa.data_limite,
                objTarefa.data_inicio if hasattr(objTarefa, 'data_inicio') else None,
                objTarefa.data_fim if hasattr(objTarefa, 'data_fim') else None,
                objTarefa.projeto_id,
                objTarefa.usuario_id if hasattr(objTarefa, 'usuario_id') else None,
                objTarefa.id,
            )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.update(): {e}")
            raise

    def findAll(self) -> list[dict]:
        print("🟢 TarefaDAO.findAll()")
        try:
            # ✅ CORREÇÃO: Query atualizada com LEFT JOIN e tratamento seguro de datas
            SQL = """
                SELECT 
                    t.id, 
                    t.titulo,
                    t.descricao,
                    t.status,
                    t.prioridade,
                    t.concluida, 
                    t.data_limite, 
                    t.data_inicio,
                    t.data_fim,
                    t.projeto_id,
                    t.usuario_id,
                    p.nome as projeto_nome,
                    u.nome as usuario_nome
                FROM tarefas t
                LEFT JOIN projetos p ON t.projeto_id = p.id
                LEFT JOIN usuarios u ON t.usuario_id = u.id
                ORDER BY t.id DESC
            """
            rows = self.__database.execute_query(SQL, fetch=True)

            tarefas = []
            for row in rows:
                tarefa_data = {
                    "id": row["id"],
                    "titulo": row["titulo"],
                    "descricao": row["descricao"],
                    "status": row["status"],
                    "prioridade": row["prioridade"],
                    "concluida": bool(row["concluida"]),
                    "projeto_id": row["projeto_id"],
                    "projeto_nome": row["projeto_nome"],
                    "usuario_id": row["usuario_id"],
                    "usuario_nome": row["usuario_nome"]
                }
                
                # ✅ CORREÇÃO: Tratamento seguro para datas
                if row["data_limite"]:
                    if hasattr(row["data_limite"], 'isoformat'):
                        tarefa_data["data_limite"] = row["data_limite"].isoformat()
                    else:
                        tarefa_data["data_limite"] = str(row["data_limite"])
                else:
                    tarefa_data["data_limite"] = None
                    
                if row["data_inicio"]:
                    if hasattr(row["data_inicio"], 'isoformat'):
                        tarefa_data["data_inicio"] = row["data_inicio"].isoformat()
                    else:
                        tarefa_data["data_inicio"] = str(row["data_inicio"])
                else:
                    tarefa_data["data_inicio"] = None
                    
                if row["data_fim"]:
                    if hasattr(row["data_fim"], 'isoformat'):
                        tarefa_data["data_fim"] = row["data_fim"].isoformat()
                    else:
                        tarefa_data["data_fim"] = str(row["data_fim"])
                else:
                    tarefa_data["data_fim"] = None
                
                tarefas.append(tarefa_data)
                
            return tarefas
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findAll(): {e}")
            raise

    def findById(self, id: int) -> dict | None:
        print("✅ TarefaDAO.findById()")
        try:
            SQL = """
                SELECT 
                    t.id, 
                    t.titulo,
                    t.descricao,
                    t.status,
                    t.prioridade,
                    t.concluida, 
                    t.data_limite, 
                    t.data_inicio,
                    t.data_fim,
                    t.projeto_id,
                    t.usuario_id,
                    p.nome as projeto_nome,
                    u.nome as usuario_nome
                FROM tarefas t
                LEFT JOIN projetos p ON t.projeto_id = p.id
                LEFT JOIN usuarios u ON t.usuario_id = u.id
                WHERE t.id = %s
            """
            rows = self.__database.execute_query(SQL, (id,), fetch=True)
            
            if not rows:
                return None
                
            row = rows[0]
            tarefa_data = {
                "id": row["id"],
                "titulo": row["titulo"],
                "descricao": row["descricao"],
                "status": row["status"],
                "prioridade": row["prioridade"],
                "concluida": bool(row["concluida"]),
                "projeto_id": row["projeto_id"],
                "projeto_nome": row["projeto_nome"],
                "usuario_id": row["usuario_id"],
                "usuario_nome": row["usuario_nome"]
            }
            
            # ✅ CORREÇÃO: Tratamento seguro para datas
            if row["data_limite"]:
                if hasattr(row["data_limite"], 'isoformat'):
                    tarefa_data["data_limite"] = row["data_limite"].isoformat()
                else:
                    tarefa_data["data_limite"] = str(row["data_limite"])
            else:
                tarefa_data["data_limite"] = None
                
            if row["data_inicio"]:
                if hasattr(row["data_inicio"], 'isoformat'):
                    tarefa_data["data_inicio"] = row["data_inicio"].isoformat()
                else:
                    tarefa_data["data_inicio"] = str(row["data_inicio"])
            else:
                tarefa_data["data_inicio"] = None
                
            if row["data_fim"]:
                if hasattr(row["data_fim"], 'isoformat'):
                    tarefa_data["data_fim"] = row["data_fim"].isoformat()
                else:
                    tarefa_data["data_fim"] = str(row["data_fim"])
            else:
                tarefa_data["data_fim"] = None
                
            return tarefa_data
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findById(): {e}")
            raise

    def findByField(self, campo: str, valor) -> list[dict]:
        print(f"🟢 TarefaDAO.findByField() - Campo: {campo}, Valor: {valor}")
        try:
            allowedFields = ["id", "titulo", "concluida", "projeto_id", "status", "usuario_id"]
            if campo not in allowedFields:
                raise ValueError("Campo inválido para busca")

            SQL = f"""
                SELECT 
                    t.*,
                    p.nome as projeto_nome,
                    u.nome as usuario_nome
                FROM tarefas t
                LEFT JOIN projetos p ON t.projeto_id = p.id
                LEFT JOIN usuarios u ON t.usuario_id = u.id
                WHERE t.{campo} = %s
            """
            resultados = self.__database.execute_query(SQL, (valor,), fetch=True)
            
            tarefas = []
            for row in resultados:
                tarefa_data = {
                    "id": row["id"],
                    "titulo": row["titulo"],
                    "descricao": row["descricao"],
                    "status": row["status"],
                    "prioridade": row["prioridade"],
                    "concluida": bool(row["concluida"]),
                    "projeto_id": row["projeto_id"],
                    "projeto_nome": row["projeto_nome"],
                    "usuario_id": row["usuario_id"],
                    "usuario_nome": row["usuario_nome"]
                }
                
                # Tratamento seguro para datas
                if row["data_limite"]:
                    if hasattr(row["data_limite"], 'isoformat'):
                        tarefa_data["data_limite"] = row["data_limite"].isoformat()
                    else:
                        tarefa_data["data_limite"] = str(row["data_limite"])
                else:
                    tarefa_data["data_limite"] = None
                    
                if row["data_inicio"]:
                    if hasattr(row["data_inicio"], 'isoformat'):
                        tarefa_data["data_inicio"] = row["data_inicio"].isoformat()
                    else:
                        tarefa_data["data_inicio"] = str(row["data_inicio"])
                else:
                    tarefa_data["data_inicio"] = None
                    
                if row["data_fim"]:
                    if hasattr(row["data_fim"], 'isoformat'):
                        tarefa_data["data_fim"] = row["data_fim"].isoformat()
                    else:
                        tarefa_data["data_fim"] = str(row["data_fim"])
                else:
                    tarefa_data["data_fim"] = None
                
                tarefas.append(tarefa_data)
                
            return tarefas
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findByField(): {e}")
            raise

    def findByProjetoId(self, projeto_id: int) -> list[dict]:
        print("🟢 TarefaDAO.findByProjetoId()")
        try:
            SQL = """
                SELECT 
                    t.id, 
                    t.titulo,
                    t.descricao,
                    t.status,
                    t.prioridade,
                    t.concluida, 
                    t.data_limite, 
                    t.data_inicio,
                    t.data_fim,
                    t.projeto_id,
                    t.usuario_id,
                    p.nome as projeto_nome
                FROM tarefas t
                LEFT JOIN projetos p ON t.projeto_id = p.id
                WHERE t.projeto_id = %s
            """
            rows = self.__database.execute_query(SQL, (projeto_id,), fetch=True)

            tarefas = []
            for row in rows:
                tarefa_data = {
                    "id": row["id"],
                    "titulo": row["titulo"],
                    "descricao": row["descricao"],
                    "status": row["status"],
                    "prioridade": row["prioridade"],
                    "concluida": bool(row["concluida"]),
                    "projeto_id": row["projeto_id"],
                    "projeto_nome": row["projeto_nome"],
                    "usuario_id": row["usuario_id"]
                }
                
                # Tratamento seguro para datas
                if row["data_limite"]:
                    if hasattr(row["data_limite"], 'isoformat'):
                        tarefa_data["data_limite"] = row["data_limite"].isoformat()
                    else:
                        tarefa_data["data_limite"] = str(row["data_limite"])
                else:
                    tarefa_data["data_limite"] = None
                    
                if row["data_inicio"]:
                    if hasattr(row["data_inicio"], 'isoformat'):
                        tarefa_data["data_inicio"] = row["data_inicio"].isoformat()
                    else:
                        tarefa_data["data_inicio"] = str(row["data_inicio"])
                else:
                    tarefa_data["data_inicio"] = None
                    
                if row["data_fim"]:
                    if hasattr(row["data_fim"], 'isoformat'):
                        tarefa_data["data_fim"] = row["data_fim"].isoformat()
                    else:
                        tarefa_data["data_fim"] = str(row["data_fim"])
                else:
                    tarefa_data["data_fim"] = None
                
                tarefas.append(tarefa_data)
                
            return tarefas
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findByProjetoId(): {e}")
            raise

    def marcarComoConcluida(self, id: int) -> bool:
        print("🟢 TarefaDAO.marcarComoConcluida()")
        try:
            SQL = "UPDATE tarefas SET concluida = TRUE WHERE id = %s"
            affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.marcarComoConcluida(): {e}")
            raise