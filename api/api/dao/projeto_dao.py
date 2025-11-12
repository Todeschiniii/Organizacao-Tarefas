# -*- coding: utf-8 -*-
from api.model.projeto import Projeto

"""
Classe responsável por gerenciar operações CRUD
para a entidade Projeto no banco de dados.
"""

class ProjetoDAO:
    def __init__(self, database_dependency):
        print("⬆️  ProjetoDAO.__init__()")
        self.__database = database_dependency
        # ✅ REMOVIDO: self._create_tables() - tabelas já existem do Banco.sql

    def create(self, objProjeto: Projeto) -> int:
        print("🟢 ProjetoDAO.create()")
        try:
            # ✅ CORREÇÃO: Query simplificada e corrigida
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

    def delete(self, id: int) -> bool:
        print("🟢 ProjetoDAO.delete()")
        try:
            SQL = "DELETE FROM projetos WHERE id = %s"
            affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.delete(): {e}")
            raise

    def update(self, objProjeto: Projeto) -> bool:
        print("🟢 ProjetoDAO.update()")
        try:
            # ✅ CORREÇÃO: Query atualizada
            SQL = """
                UPDATE projetos 
                SET nome=%s, descricao=%s, data_inicio=%s, data_fim=%s, status=%s, usuario_id=%s 
                WHERE id=%s
            """
            params = (
                objProjeto.nome,
                objProjeto.descricao,
                objProjeto.data_inicio,
                objProjeto.data_fim,
                objProjeto.status,
                objProjeto.usuario_id,
                objProjeto.id,
            )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.update(): {e}")
            raise

    def findAll(self) -> list[dict]:
        print("🟢 ProjetoDAO.findAll()")
        try:
            # ✅ CORREÇÃO: Query corrigida com LEFT JOIN e tratamento de datas
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
                
                # ✅ CORREÇÃO: Tratamento seguro para datas
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

    def findById(self, id: int) -> dict | None:
        print("✅ ProjetoDAO.findById()")
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
            
            # ✅ CORREÇÃO: Tratamento seguro para datas
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

    def findByField(self, campo: str, valor) -> list[dict]:
        print(f"🟢 ProjetoDAO.findByField() - Campo: {campo}, Valor: {valor}")
        try:
            allowedFields = ["id", "nome", "status", "usuario_id"]
            if campo not in allowedFields:
                raise ValueError("Campo inválido para busca")

            SQL = f"""
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
                WHERE p.{campo} = %s
            """
            resultados = self.__database.execute_query(SQL, (valor,), fetch=True)
            
            projetos = []
            for row in resultados:
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
            print(f"❌ Erro em ProjetoDAO.findByField(): {e}")
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