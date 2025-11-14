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

    def create(self, objTarefa: Tarefa) -> int:
        print("🟢 TarefaDAO.create()")
        try:
            SQL = """
                INSERT INTO tarefas 
                (titulo, descricao, status, prioridade, concluida, data_limite, 
                 data_inicio, data_fim, projeto_id, usuario_responsavel_id, usuario_atribuidor_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # ✅ CORREÇÃO: Tratamento seguro para datas
            data_limite_value = None
            if objTarefa.data_limite:
                if hasattr(objTarefa.data_limite, 'isoformat'):
                    data_limite_value = objTarefa.data_limite.isoformat()
                else:
                    data_limite_value = str(objTarefa.data_limite)
            
            data_inicio_value = None
            if hasattr(objTarefa, 'data_inicio') and objTarefa.data_inicio:
                if hasattr(objTarefa.data_inicio, 'isoformat'):
                    data_inicio_value = objTarefa.data_inicio.isoformat()
                else:
                    data_inicio_value = str(objTarefa.data_inicio)
            
            data_fim_value = None
            if hasattr(objTarefa, 'data_fim') and objTarefa.data_fim:
                if hasattr(objTarefa.data_fim, 'isoformat'):
                    data_fim_value = objTarefa.data_fim.isoformat()
                else:
                    data_fim_value = str(objTarefa.data_fim)

            params = (
                objTarefa.titulo,
                objTarefa.descricao if hasattr(objTarefa, 'descricao') else "",
                objTarefa.status if hasattr(objTarefa, 'status') else "pendente",
                objTarefa.prioridade if hasattr(objTarefa, 'prioridade') else "media",
                objTarefa.concluida,
                data_limite_value,
                data_inicio_value,
                data_fim_value,
                objTarefa.projeto_id,
                objTarefa.usuario_responsavel_id,
                objTarefa.usuario_atribuidor_id
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir tarefa")
            return insert_id
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.create(): {e}")
            raise

    def delete(self, id: int, usuario_id: int = None) -> bool:
        """
        ✅ CORREÇÃO: Agora verifica por usuario_responsavel_id
        """
        print("🟢 TarefaDAO.delete()")
        try:
            if usuario_id:
                # ✅ CORREÇÃO: Só deleta se a tarefa pertencer ao usuário responsável
                SQL = "DELETE FROM tarefas WHERE id = %s AND usuario_responsavel_id = %s"
                params = (id, usuario_id)
            else:
                SQL = "DELETE FROM tarefas WHERE id = %s"
                params = (id,)
                
            affected = self.__database.execute_query(SQL, params)
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.delete(): {e}")
            raise

    def update(self, objTarefa: Tarefa, usuario_id: int = None) -> bool:
        print("🟢 TarefaDAO.update()")
        try:
            # ✅ CORREÇÃO: SQL completo com novos campos
            SQL = """
                UPDATE tarefas 
                SET titulo=%s, descricao=%s, status=%s, prioridade=%s, concluida=%s, 
                    data_limite=%s, data_inicio=%s, data_fim=%s, projeto_id=%s,
                    usuario_responsavel_id=%s, usuario_atribuidor_id=%s
                WHERE id=%s
            """
            
            # ✅ CORREÇÃO: Agora verifica por usuario_responsavel_id
            if usuario_id:
                SQL += " AND usuario_responsavel_id = %s"

            # ✅ CORREÇÃO: Tratamento seguro para datas (FALTANDO NO SEU CÓDIGO)
            data_limite_value = None
            if objTarefa.data_limite:
                if hasattr(objTarefa.data_limite, 'isoformat'):
                    data_limite_value = objTarefa.data_limite.isoformat()
                else:
                    data_limite_value = str(objTarefa.data_limite)
            
            data_inicio_value = None
            if hasattr(objTarefa, 'data_inicio') and objTarefa.data_inicio:
                if hasattr(objTarefa.data_inicio, 'isoformat'):
                    data_inicio_value = objTarefa.data_inicio.isoformat()
                else:
                    data_inicio_value = str(objTarefa.data_inicio)
            
            data_fim_value = None
            if hasattr(objTarefa, 'data_fim') and objTarefa.data_fim:
                if hasattr(objTarefa.data_fim, 'isoformat'):
                    data_fim_value = objTarefa.data_fim.isoformat()
                else:
                    data_fim_value = str(objTarefa.data_fim)

            # ✅ CORREÇÃO: Parâmetros completos
            params = [
                objTarefa.titulo,
                objTarefa.descricao if hasattr(objTarefa, 'descricao') else "",
                objTarefa.status if hasattr(objTarefa, 'status') else "pendente",
                objTarefa.prioridade if hasattr(objTarefa, 'prioridade') else "media",
                objTarefa.concluida,
                data_limite_value,
                data_inicio_value,
                data_fim_value,
                objTarefa.projeto_id,
                objTarefa.usuario_responsavel_id,
                objTarefa.usuario_atribuidor_id,
                objTarefa.id,
            ]
            
            # ✅ CORREÇÃO: Adiciona usuario_responsavel_id aos parâmetros se fornecido
            if usuario_id:
                params.append(usuario_id)

            affected = self.__database.execute_query(SQL, tuple(params))
            return affected > 0
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.update(): {e}")
            raise

    def updateCampo(self, id: int, campo: str, valor: any, usuario_id: int = None) -> bool:
        """
        ✅ CORREÇÃO: Agora verifica por usuario_responsavel_id
        """
        print(f"🟢 TarefaDAO.updateCampo() - ID: {id}, Campo: {campo}, Valor: {valor}")
        
        # ✅ CORREÇÃO: Query com verificação de usuario_responsavel_id
        if usuario_id:
            query = f"UPDATE tarefas SET {campo} = %s WHERE id = %s AND usuario_responsavel_id = %s"
            params = (valor, id, usuario_id)
        else:
            query = f"UPDATE tarefas SET {campo} = %s WHERE id = %s"
            params = (valor, id)
        
        try:
            result = self.__database.execute_query(query, params)
            return result > 0
        except Exception as e:
            print(f"❌ Erro no TarefaDAO.updateCampo(): {e}")
            raise e

    def marcarConcluida(self, id: int, concluida: bool, usuario_id: int = None) -> bool:
        """
        ✅ CORREÇÃO: Agora verifica por usuario_responsavel_id
        """
        print(f"🟢 TarefaDAO.marcarConcluida() - ID: {id}, Concluída: {concluida}")
        
        # ✅ CORREÇÃO: Query com verificação de usuario_responsavel_id
        if usuario_id:
            query = "UPDATE tarefas SET concluida = %s WHERE id = %s AND usuario_responsavel_id = %s"
            params = (concluida, id, usuario_id)
        else:
            query = "UPDATE tarefas SET concluida = %s WHERE id = %s"
            params = (concluida, id)
        
        try:
            result = self.__database.execute_query(query, params)
            return result > 0
        except Exception as e:
            print(f"❌ Erro no TarefaDAO.marcarConcluida(): {e}")
            raise e

    def findAll(self, usuario_id: int = None) -> list[dict]:
        """
        ✅ CORREÇÃO: Query atualizada com novos campos
        """
        print("🟢 TarefaDAO.findAll()")
        try:
            if usuario_id:
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
                        t.usuario_responsavel_id,
                        t.usuario_atribuidor_id,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome,
                        ua.nome as atribuidor_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    LEFT JOIN usuarios ua ON t.usuario_atribuidor_id = ua.id
                    WHERE t.usuario_responsavel_id = %s
                    ORDER BY t.id DESC
                """
                params = (usuario_id,)
            else:
                # ✅ CORREÇÃO: Query sem filtro também atualizada
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
                        t.usuario_responsavel_id,
                        t.usuario_atribuidor_id,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome,
                        ua.nome as atribuidor_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    LEFT JOIN usuarios ua ON t.usuario_atribuidor_id = ua.id
                    ORDER BY t.id DESC
                """
                params = None

            rows = self.__database.execute_query(SQL, params, fetch=True)

            tarefas = []
            for row in rows:
                tarefa_data = self._row_to_dict(row)
                tarefas.append(tarefa_data)
                
            return tarefas
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findAll(): {e}")
            raise

    def findById(self, id: int, usuario_id: int = None) -> dict | None:
        """
        ✅ CORREÇÃO: Query atualizada com novos campos
        """
        print("✅ TarefaDAO.findById()")
        try:
            if usuario_id:
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
                        t.usuario_responsavel_id,
                        t.usuario_atribuidor_id,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome,
                        ua.nome as atribuidor_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    LEFT JOIN usuarios ua ON t.usuario_atribuidor_id = ua.id
                    WHERE t.id = %s AND t.usuario_responsavel_id = %s
                """
                params = (id, usuario_id)
            else:
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
                        t.usuario_responsavel_id,
                        t.usuario_atribuidor_id,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome,
                        ua.nome as atribuidor_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    LEFT JOIN usuarios ua ON t.usuario_atribuidor_id = ua.id
                    WHERE t.id = %s
                """
                params = (id,)

            rows = self.__database.execute_query(SQL, params, fetch=True)
            
            if not rows:
                return None
                
            row = rows[0]
            return self._row_to_dict(row)
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findById(): {e}")
            raise

    def findByField(self, campo: str, valor, usuario_id: int = None) -> list[dict]:
        """
        ✅ CORREÇÃO: Query atualizada com novos campos
        """
        print(f"🟢 TarefaDAO.findByField() - Campo: {campo}, Valor: {valor}")
        try:
            # ✅ CORREÇÃO: Campos permitidos atualizados
            allowedFields = ["id", "titulo", "concluida", "projeto_id", "status", 
                           "usuario_responsavel_id", "usuario_atribuidor_id"]
            if campo not in allowedFields:
                raise ValueError("Campo inválido para busca")

            if usuario_id:
                SQL = f"""
                    SELECT 
                        t.*,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome,
                        ua.nome as atribuidor_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    LEFT JOIN usuarios ua ON t.usuario_atribuidor_id = ua.id
                    WHERE t.{campo} = %s AND t.usuario_responsavel_id = %s
                """
                params = (valor, usuario_id)
            else:
                SQL = f"""
                    SELECT 
                        t.*,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome,
                        ua.nome as atribuidor_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    LEFT JOIN usuarios ua ON t.usuario_atribuidor_id = ua.id
                    WHERE t.{campo} = %s
                """
                params = (valor,)

            resultados = self.__database.execute_query(SQL, params, fetch=True)
            
            tarefas = []
            for row in resultados:
                tarefa_data = self._row_to_dict(row)
                tarefas.append(tarefa_data)
                
            return tarefas
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findByField(): {e}")
            raise

    def findByProjetoId(self, projeto_id: int, usuario_id: int = None) -> list[dict]:
        """
        ✅ CORREÇÃO: Query atualizada com novos campos
        """
        print("🟢 TarefaDAO.findByProjetoId()")
        try:
            if usuario_id:
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
                        t.usuario_responsavel_id,
                        t.usuario_atribuidor_id,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    WHERE t.projeto_id = %s AND t.usuario_responsavel_id = %s
                """
                params = (projeto_id, usuario_id)
            else:
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
                        t.usuario_responsavel_id,
                        t.usuario_atribuidor_id,
                        p.nome as projeto_nome,
                        ur.nome as responsavel_nome
                    FROM tarefas t
                    LEFT JOIN projetos p ON t.projeto_id = p.id
                    LEFT JOIN usuarios ur ON t.usuario_responsavel_id = ur.id
                    WHERE t.projeto_id = %s
                """
                params = (projeto_id,)

            rows = self.__database.execute_query(SQL, params, fetch=True)

            tarefas = []
            for row in rows:
                tarefa_data = self._row_to_dict(row)
                tarefas.append(tarefa_data)
                
            return tarefas
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findByProjetoId(): {e}")
            raise

    def marcarComoConcluida(self, id: int, usuario_id: int = None) -> bool:
        """
        ✅ CORREÇÃO: Agora verifica por usuario_responsavel_id
        """
        print("🟢 TarefaDAO.marcarComoConcluida()")
        try:
            if usuario_id:
                SQL = "UPDATE tarefas SET concluida = TRUE WHERE id = %s AND usuario_responsavel_id = %s"
                params = (id, usuario_id)
            else:
                SQL = "UPDATE tarefas SET concluida = TRUE WHERE id = %s"
                params = (id,)
                
            affected = self.__database.execute_query(SQL, params)
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.marcarComoConcluida(): {e}")
            raise

    def _row_to_dict(self, row: dict) -> dict:
        """
        ✅ CORREÇÃO: Método auxiliar atualizado para novos campos
        """
        tarefa_data = {
            "id": row["id"],
            "titulo": row["titulo"],
            "descricao": row["descricao"],
            "status": row["status"],
            "prioridade": row["prioridade"],
            "concluida": bool(row["concluida"]),
            "projeto_id": row["projeto_id"],
            "projeto_nome": row.get("projeto_nome"),
            "usuario_responsavel_id": row["usuario_responsavel_id"],
            "usuario_atribuidor_id": row["usuario_atribuidor_id"],
            "responsavel_nome": row.get("responsavel_nome"),
            "atribuidor_nome": row.get("atribuidor_nome")
        }
        
        # ✅ CORREÇÃO: Tratamento seguro para datas
        date_fields = ["data_limite", "data_inicio", "data_fim"]
        for field in date_fields:
            if row.get(field):
                if hasattr(row[field], 'isoformat'):
                    tarefa_data[field] = row[field].isoformat()
                else:
                    tarefa_data[field] = str(row[field])
            else:
                tarefa_data[field] = None
                
        return tarefa_data

    def getTarefasByUsuario(self, usuario_id: int) -> list[dict]:
        """
        ✅ NOVO: Método específico para buscar tarefas de um usuário
        """
        print(f"🟢 TarefaDAO.getTarefasByUsuario() - Usuario ID: {usuario_id}")
        return self.findAll(usuario_id=usuario_id)

    def getEstatisticasUsuario(self, usuario_id: int) -> dict:
        """
        ✅ CORREÇÃO: Query atualizada para usuario_responsavel_id
        """
        print(f"🟢 TarefaDAO.getEstatisticasUsuario() - Usuario ID: {usuario_id}")
        try:
            SQL = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN concluida = TRUE THEN 1 ELSE 0 END) as concluidas,
                    SUM(CASE WHEN concluida = FALSE THEN 1 ELSE 0 END) as pendentes,
                    SUM(CASE WHEN status = 'urgente' THEN 1 ELSE 0 END) as urgentes,
                    SUM(CASE WHEN prioridade = 'alta' THEN 1 ELSE 0 END) as prioridade_alta
                FROM tarefas 
                WHERE usuario_responsavel_id = %s
            """
            rows = self.__database.execute_query(SQL, (usuario_id,), fetch=True)
            
            if not rows:
                return {
                    "total": 0,
                    "concluidas": 0,
                    "pendentes": 0,
                    "urgentes": 0,
                    "prioridade_alta": 0
                }
                
            row = rows[0]
            return {
                "total": row["total"] or 0,
                "concluidas": row["concluidas"] or 0,
                "pendentes": row["pendentes"] or 0,
                "urgentes": row["urgentes"] or 0,
                "prioridade_alta": row["prioridade_alta"] or 0
            }
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.getEstatisticasUsuario(): {e}")
            return {
                "total": 0,
                "concluidas": 0,
                "pendentes": 0,
                "urgentes": 0,
                "prioridade_alta": 0
            }