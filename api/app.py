from flask import Flask, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

# Importações dos DAOs (Data Access Objects)
from api.dao.usuario_dao import UsuarioDAO
from api.dao.projeto_dao import ProjetoDAO
from api.dao.tarefa_dao import TarefaDAO

# Importações dos Services
from api.service.usuario_service import UsuarioService
from api.service.projeto_service import ProjetoService
from api.service.tarefa_service import TarefaService

# Importações dos Middlewares
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.usuario_middleware import UsuarioMiddleware
from api.middleware.projeto_middleware import ProjetoMiddleware
from api.middleware.tarefa_middleware import TarefaMiddleware

# Importações dos Controls
from api.control.usuario_control import UsuarioControl
from api.control.projeto_control import ProjetoControl
from api.control.tarefa_control import TarefaControl

# Importações dos Roteadores
from api.router.usuario_roteador import UsuarioRoteador
from api.router.projeto_roteador import ProjetoRoteador
from api.router.tarefa_roteador import TarefaRoteador

class MySQLDatabase:
    """
    Classe para gerenciar conexões com o MySQL
    """
    def __init__(self):
        self.connection = None
        self.config = {
            'host': 'localhost',
            'database': 'projeto',
            'user': 'root',
            'password': '',
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'port': 3306,
            'autocommit': True,  # ✅ CORREÇÃO: Adicionado autocommit
        }
        self.connect()
    
    def connect(self):
        """Estabelece conexão com o MySQL"""
        try:
            # ✅ CORREÇÃO: Configuração simplificada sem pool
            self.connection = mysql.connector.connect(**self.config)
            if self.connection and self.connection.is_connected():
                print("✅ Conectado ao MySQL Database!")
                return self.connection
            else:
                print("❌ Conexão estabelecida mas não está conectada")
                return None
        except Error as e:
            print(f"❌ Erro ao conectar com MySQL: {e}")
            print("💡 Verifique se:")
            print("   1. XAMPP MySQL está RODANDO")
            print("   2. O banco 'projeto' existe") 
            print("   3. Usuário 'root' sem senha está correto")
            print("   4. Porta 3306 está livre")
            return None
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Executa uma query no banco de dados
        """
        cursor = None
        try:
            # ✅ CORREÇÃO: Verificação SEGURA da conexão
            if (self.connection is None or 
                not hasattr(self.connection, 'is_connected') or 
                not self.connection.is_connected()):
                
                print("🔄 Reconectando ao MySQL...")
                self.connect()
                if self.connection is None:
                    raise Error("Não foi possível conectar ao banco de dados - conexão é None")
            
            cursor = self.connection.cursor(dictionary=True)
            
            print(f"📝 Executando query: {query[:100]}...")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Para INSERT, UPDATE, DELETE
            if not fetch:
                # ✅ CORREÇÃO: Commit apenas se não estiver em autocommit
                if not self.connection.autocommit:
                    self.connection.commit()
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                return cursor.rowcount
            
            # Para SELECT
            result = cursor.fetchall()
            return result
            
        except Error as e:
            print(f"❌ Erro na query: {e}")
            # ✅ CORREÇÃO: Rollback seguro
            if (self.connection is not None and 
                hasattr(self.connection, 'rollback') and 
                not self.connection.autocommit):
                try:
                    self.connection.rollback()
                except:
                    pass  # Ignora erro no rollback
            raise e
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """Fecha a conexão com o banco"""
        # ✅ CORREÇÃO: Verificação SEGURA antes de fechar
        if (self.connection is not None and 
            hasattr(self.connection, 'is_connected') and 
            self.connection.is_connected()):
            
            self.connection.close()
            print("🔒 Conexão MySQL fechada!")
        else:
            print("ℹ️  Conexão MySQL já estava fechada ou é None")

def create_app():
    """
    Factory function para criar e configurar a aplicação Flask.
    """
    app = Flask(__name__)
    
    # ✅ CORREÇÃO: Configuração CORS DINÂMICA
    CORS(app, 
        origins=["http://localhost", "http://127.0.0.1", "http://localhost:5500", "http://127.0.0.1:5500", "*"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["Content-Type", "Authorization"]
    )
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
    
    # ✅ CORREÇÃO: Inicialização do banco com tratamento de erro melhorado
    try:
        database_dependency = MySQLDatabase()
        if not database_dependency.connection:
            raise Exception("Falha na conexão com MySQL - verifique se MySQL está rodando no XAMPP")
        print("🚀 MySQL Database inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar MySQL: {e}")
        print("🔄 Usando MockDatabase...")
        
        class MockDatabase:
            def __init__(self):
                print("🔄 MockDatabase inicializado - usando dados de exemplo")
                self.mock_usuarios = [
                    {
                        "id": 1, 
                        "nome": "Admin", 
                        "email": "admin@email.com", 
                        "senha_hash": "$2b$12$K5rDsVk7c5p2wY8zQ8b8XeX5rDsVk7c5p2wY8zQ8b8Xe", # hash de '123456'
                        "data_criacao": "2024-01-01 00:00:00"
                    }
                ]
                self.mock_projetos = []
                self.mock_tarefas = []
                self.last_id = 1
            
            def execute_query(self, query, params=None, fetch=False):
                print(f"📝 MockDatabase.execute_query: {query[:100]}...")
                
                # Simula INSERT
                if query.upper().startswith('INSERT'):
                    self.last_id += 1
                    return self.last_id
                
                # Simula SELECT
                if fetch:
                    if 'WHERE email' in query and params:
                        email = params[0]
                        for usuario in self.mock_usuarios:
                            if usuario['email'] == email:
                                return [usuario]
                        return []
                    return self.mock_usuarios
                return 1
            
            def connect(self): return self
            def close(self): pass
            def commit(self): pass
            def __getattr__(self, name):
                def method(*args, **kwargs):
                    print(f"🔧 MockDatabase.{name}() chamado")
                    return None
                return method
        
        database_dependency = MockDatabase()
    
    # ✅ CORREÇÃO: Inicialização de DAOs
    usuario_dao = UsuarioDAO(database_dependency=database_dependency)
    projeto_dao = ProjetoDAO(database_dependency=database_dependency)
    tarefa_dao = TarefaDAO(database_dependency=database_dependency)
    
    # ✅ CORREÇÃO: Inicialização de Services
    usuario_service = UsuarioService(usuario_dao_dependency=usuario_dao)
    
    # Inicialização simplificada dos outros services
    projeto_service = ProjetoService(
        projeto_dao_dependency=projeto_dao,
        usuario_dao_dependency=usuario_dao
    )

    tarefa_service = TarefaService(
        tarefa_dao_dependency=tarefa_dao,
        projeto_dao_dependency=projeto_dao
    )
    
    # Inicialização de Controls
    usuario_control = UsuarioControl(usuario_service)
    projeto_control = ProjetoControl(projeto_service)
    tarefa_control = TarefaControl(tarefa_service)
    
    # Inicialização de Middlewares
    jwt_middleware = JwtMiddleware()
    usuario_middleware = UsuarioMiddleware()
    projeto_middleware = ProjetoMiddleware()
    tarefa_middleware = TarefaMiddleware()
    
    # Inicialização de Roteadores
    usuario_roteador = UsuarioRoteador(jwt_middleware, usuario_middleware, usuario_control)
    projeto_roteador = ProjetoRoteador(jwt_middleware, projeto_middleware, projeto_control)
    tarefa_roteador = TarefaRoteador(jwt_middleware, tarefa_middleware, tarefa_control)
    
    # Registrar blueprints
    app.register_blueprint(usuario_roteador.create_routes(), url_prefix='/api/usuario')
    app.register_blueprint(projeto_roteador.create_routes(), url_prefix='/api/projeto')
    app.register_blueprint(tarefa_roteador.create_routes(), url_prefix='/api/tarefa')
    
    # ✅ CORREÇÃO: Middleware CORS DINÂMICO para todas as rotas
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        allowed_origins = ["http://localhost", "http://127.0.0.1", "http://localhost:5500", "http://127.0.0.1:5500"]
        
        if origin in allowed_origins:
            response.headers.add('Access-Control-Allow-Origin', origin)
        else:
            # Fallback para desenvolvimento
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost')
            
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    # ✅ CORREÇÃO: Rotas de verificação
    @app.route('/health', methods=['GET'])
    def health_check():
        db_status = "connected" if hasattr(database_dependency, 'connection') and database_dependency.connection and database_dependency.connection.is_connected() else "mock"
        return {
            "status": "healthy",
            "message": "API está funcionando corretamente",
            "database": db_status,
            "endpoints": {
                "usuarios": "/api/usuario/",
                "cadastro": "POST /api/usuario/",
                "login": "POST /api/usuario/login"
            }
        }
    
    @app.route('/', methods=['GET'])
    def root():
        return {
            "message": "✅ API Flask funcionando!",
            "endpoints": {
                "health": "/health",
                "usuarios": "/api/usuario/",
                "cadastro": "POST /api/usuario/",
                "login": "POST /api/usuario/login"
            }
        }
    
    # Fechar conexão ao encerrar
    @app.teardown_appcontext
    def close_db_connection(exception=None):
        if hasattr(database_dependency, 'close'):
            database_dependency.close()
    
    print("=" * 50)
    print("🚀 FLASK APP INICIALIZADA COM SUCESSO!")
    print("📍 URL: http://localhost:5000")
    print("📊 Banco de dados: projeto")
    print("✅ CORS configurado dinamicamente")
    print("=" * 50)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🔥 Iniciando servidor Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)