# -*- coding: utf-8 -*-
from api.model.projeto import Projeto

class ProjetoDAO:
    def __init__(self, database_dependency):
        print("⬆️  ProjetoDAO.__init__()")
        self.__database = database_dependency

    def create(self, objProjeto: Projeto) -> int:
        print("🟢 ProjetoDAO.create()")
        try:
            SQL = """
                INSERT INTO projetos 
                (nome, descricao, data_inicio, data_fim, status, usuario_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                objProjeto.nome,
                objProjeto.descricao,
                objProjeto.data_inicio,
                objProjeto.data_fim,
                objProjeto.status,
                objProjeto.usuario_id,
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir projeto")
            return insert_id
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.create(): {e}")
            raise

    def delete(self, id: int, usuario_id: int = None) -> bool:
        print("🟢 ProjetoDAO.delete()")
        try:
            if usuario_id:
                # ✅ CORREÇÃO: Só deleta se o projeto pertencer ao usuário
                SQL = "DELETE FROM projetos WHERE id = %s AND usuario_id = %s"
                affected = self.__database.execute_query(SQL, (id, usuario_id))
            else:
                SQL = "DELETE FROM projetos WHERE id = %s"
                affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.delete(): {e}")
            raise

    def update(self, objProjeto: Projeto) -> bool:
        print("🟢 ProjetoDAO.update()")
        try:
            # ✅ CORREÇÃO: Só atualiza se o projeto pertencer ao usuário
            SQL = """
                UPDATE projetos 
                SET nome=%s, descricao=%s, data_inicio=%s, data_fim=%s, status=%s
                WHERE id=%s AND usuario_id=%s
            """
            params = (
                objProjeto.nome,
                objProjeto.descricao,
                objProjeto.data_inicio,
                objProjeto.data_fim,
                objProjeto.status,
                objProjeto.id,
                objProjeto.usuario_id,
            )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.update(): {e}")
            raise

    def findAll(self, usuario_id: int = None) -> list[dict]:
        print("🟢 ProjetoDAO.findAll()")
        try:
            if usuario_id:
                # ✅ CORREÇÃO: Só retorna projetos do usuário específico
                SQL = """
                    SELECT 
                        p.id, 
                        p.nome, 
                        p.descricao, 
                        p.data_inicio, 
                        p.data_fim,
                        p.status, 
                        p.usuario_id,
                        u.nome as usuario_nome
                    FROM projetos p
                    LEFT JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.usuario_id = %s
                    ORDER BY p.id DESC
                """
                rows = self.__database.execute_query(SQL, (usuario_id,), fetch=True)
            else:
                # Retorna todos os projetos (apenas para admin)
                SQL = """
                    SELECT 
                        p.id, 
                        p.nome, 
                        p.descricao, 
                        p.data_inicio, 
                        p.data_fim,
                        p.status, 
                        p.usuario_id,
                        u.nome as usuario_nome
                    FROM projetos p
                    LEFT JOIN usuarios u ON p.usuario_id = u.id
                    ORDER BY p.id DESC
                """
                rows = self.__database.execute_query(SQL, fetch=True)

            projetos = []
            for row in rows:
                projeto_data = {
                    "id": row["id"],
                    "nome": row["nome"],
                    "descricao": row["descricao"],
                    "status": row["status"],
                    "usuario_id": row["usuario_id"],
                    "usuario_nome": row["usuario_nome"]
                }
                
                # Tratamento seguro para datas
                if row["data_inicio"]:
                    if hasattr(row["data_inicio"], 'isoformat'):
                        projeto_data["data_inicio"] = row["data_inicio"].isoformat()
                    else:
                        projeto_data["data_inicio"] = str(row["data_inicio"])
                else:
                    projeto_data["data_inicio"] = None
                    
                if row["data_fim"]:
                    if hasattr(row["data_fim"], 'isoformat'):
                        projeto_data["data_fim"] = row["data_fim"].isoformat()
                    else:
                        projeto_data["data_fim"] = str(row["data_fim"])
                else:
                    projeto_data["data_fim"] = None
                
                projetos.append(projeto_data)
                
            return projetos
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.findAll(): {e}")
            raise

    def findById(self, id: int, usuario_id: int = None) -> dict | None:
        print("✅ ProjetoDAO.findById()")
        try:
            if usuario_id:
                # ✅ CORREÇÃO: Só retorna projeto se pertencer ao usuário
                SQL = """
                    SELECT 
                        p.id, 
                        p.nome, 
                        p.descricao, 
                        p.data_inicio, 
                        p.data_fim,
                        p.status, 
                        p.usuario_id,
                        u.nome as usuario_nome
                    FROM projetos p
                    LEFT JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.id = %s AND p.usuario_id = %s
                """
                rows = self.__database.execute_query(SQL, (id, usuario_id), fetch=True)
            else:
                SQL = """
                    SELECT 
                        p.id, 
                        p.nome, 
                        p.descricao, 
                        p.data_inicio, 
                        p.data_fim,
                        p.status, 
                        p.usuario_id,
                        u.nome as usuario_nome
                    FROM projetos p
                    LEFT JOIN usuarios u ON p.usuario_id = u.id
                    WHERE p.id = %s
                """
                rows = self.__database.execute_query(SQL, (id,), fetch=True)
            
            if not rows:
                return None
                
            row = rows[0]
            projeto_data = {
                "id": row["id"],
                "nome": row["nome"],
                "descricao": row["descricao"],
                "status": row["status"],
                "usuario_id": row["usuario_id"],
                "usuario_nome": row["usuario_nome"]
            }
            
            # Tratamento seguro para datas
            if row["data_inicio"]:
                if hasattr(row["data_inicio"], 'isoformat'):
                    projeto_data["data_inicio"] = row["data_inicio"].isoformat()
                else:
                    projeto_data["data_inicio"] = str(row["data_inicio"])
            else:
                projeto_data["data_inicio"] = None
                
            if row["data_fim"]:
                if hasattr(row["data_fim"], 'isoformat'):
                    projeto_data["data_fim"] = row["data_fim"].isoformat()
                else:
                    projeto_data["data_fim"] = str(row["data_fim"])
            else:
                projeto_data["data_fim"] = None
                
            return projeto_data
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.findById(): {e}")
            raise

    def findByUsuarioId(self, usuario_id: int) -> list[dict]:
        print("🟢 ProjetoDAO.findByUsuarioId()")
        try:
            SQL = """
                SELECT 
                    p.id, 
                    p.nome, 
                    p.descricao, 
                    p.data_inicio, 
                    p.data_fim,
                    p.status, 
                    p.usuario_id,
                    u.nome as usuario_nome
                FROM projetos p
                LEFT JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.usuario_id = %s
                ORDER BY p.data_criacao DESC
            """
            rows = self.__database.execute_query(SQL, (usuario_id,), fetch=True)

            projetos = []
            for row in rows:
                projeto_data = {
                    "id": row["id"],
                    "nome": row["nome"],
                    "descricao": row["descricao"],
                    "status": row["status"],
                    "usuario_id": row["usuario_id"],
                    "usuario_nome": row["usuario_nome"]
                }
                
                # Tratamento seguro para datas
                if row["data_inicio"]:
                    if hasattr(row["data_inicio"], 'isoformat'):
                        projeto_data["data_inicio"] = row["data_inicio"].isoformat()
                    else:
                        projeto_data["data_inicio"] = str(row["data_inicio"])
                else:
                    projeto_data["data_inicio"] = None
                    
                if row["data_fim"]:
                    if hasattr(row["data_fim"], 'isoformat'):
                        projeto_data["data_fim"] = row["data_fim"].isoformat()
                    else:
                        projeto_data["data_fim"] = str(row["data_fim"])
                else:
                    projeto_data["data_fim"] = None
                
                projetos.append(projeto_data)
                
            return projetos
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.findByUsuarioId(): {e}")
            raise