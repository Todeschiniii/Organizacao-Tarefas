# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import pooling, Error
import sys
import os
import time


class MysqlDatabase:
    """
    Classe responsável por gerenciar a conexão com o MySQL.
    """
    __pool = None
    __instance = None

    def __init__(self, pool_name="projeto_pool", pool_size=5, pool_reset_session=True,
                 host="127.0.0.1", user="root", password="", database="projeto", port=3306):
        """
        Configurações padrão para XAMPP:
        - host: 127.0.0.1
        - user: root  
        - password: (vazia)
        - database: projeto
        - port: 3306
        """
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.pool_reset_session = pool_reset_session
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(MysqlDatabase, cls).__new__(cls)
        return cls.__instance

    def connect(self):
        """
        Cria e retorna o pool de conexões MySQL com tratamento de erro melhorado.
        """
        if MysqlDatabase.__pool is None:
            try:
                print("🔄 Iniciando pool de conexões MySQL...")
                
                # Primeiro tenta conectar sem database para verificar se MySQL está rodando
                test_config = {
                    'host': self.host,
                    'user': self.user,
                    'password': self.password,
                    'port': self.port
                }
                
                # Testa conexão básica
                test_conn = mysql.connector.connect(**test_config)
                test_cursor = test_conn.cursor()
                
                # Verifica se o database existe
                test_cursor.execute("SHOW DATABASES LIKE %s", (self.database,))
                db_exists = test_cursor.fetchone()
                
                if not db_exists:
                    print(f"⚠️  Banco '{self.database}' não existe. Criando...")
                    test_cursor.execute(f"CREATE DATABASE {self.database}")
                    print(f"✅ Banco '{self.database}' criado com sucesso!")
                
                test_cursor.close()
                test_conn.close()
                
                # Agora cria o pool com o database
                MysqlDatabase.__pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    pool_reset_session=self.pool_reset_session,
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    autocommit=False
                )

                # Testa a conexão com o database
                conn = MysqlDatabase.__pool.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                
                cursor.close()
                conn.close()
                
                print(f"✅ Conectado ao MySQL {version} (banco: {self.database})")
                
            except mysql.connector.Error as err:
                print(f"❌ Falha ao conectar ao MySQL: {err}")
                print(f"🔧 Configuração: {self.host}:{self.port}, user: {self.user}")
                print("💡 Verifique se:")
                print("   - MySQL está rodando (XAMPP)")
                print("   - Serviço MySQL foi iniciado")
                print("   - Porta 3306 está livre")
                raise

        return MysqlDatabase.__pool

    def get_connection(self):
        """
        Obtém uma conexão do pool com retry.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                pool = self.connect()
                conn = pool.get_connection()
                conn.autocommit = False
                return conn
            except mysql.connector.Error as err:
                print(f"❌ Tentativa {attempt + 1}/{max_retries} - Erro ao obter conexão: {err}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)  # Espera 1 segundo antes de tentar novamente

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Executa uma query e retorna os resultados.
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                return cursor.lastrowid if query.strip().upper().startswith('INSERT') else cursor.rowcount
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao executar query: {err}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def test_connection(self):
        """
        Teste de conexão mais simples e robusto.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Query simples para testar
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            print("✅ Conexão com MySQL testada com sucesso!")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Erro ao testar conexão: {err}")
            return False

    def get_pool_status(self):
        if MysqlDatabase.__pool is None:
            return {"status": "Pool não inicializado"}
        
        return {
            "status": "Ativo",
            "pool_name": self.pool_name,
            "pool_size": self.pool_size,
            "database": self.database
        }

    def close_pool(self):
        if MysqlDatabase.__pool is not None:
            print("🔒 Fechando pool de conexões MySQL...")
            MysqlDatabase.__pool = None
            MysqlDatabase.__instance = None
            print("✅ Pool de conexões fechado.")


def create_database_instance():
    """
    Factory function com fallback para quando o banco padrão não funciona.
    """
    config = {
        'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'projeto'),
        'port': int(os.getenv('MYSQL_PORT', '3306')),
        'pool_size': int(os.getenv('MYSQL_POOL_SIZE', '5'))
    }
    
    return MysqlDatabase(**config)


if __name__ == "__main__":
    print("🧪 Testando conexão com MySQL...")
    
    db = create_database_instance()
    
    if db.test_connection():
        print("🎉 Conexão estabelecida com sucesso!")
    else:
        print("💥 Falha na conexão com o banco!")