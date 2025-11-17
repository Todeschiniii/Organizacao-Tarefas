from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error, pooling
import os
import traceback
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

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

# Configurações de email (ajuste conforme suas credenciais)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'mateus.todeschini.developer@gmail.com',  # ALTERE: Seu email Gmail
    'password': 'mzgn ugkb iofo ilab'   # ALTERE: Senha de app do Gmail
}

# Dicionário temporário para armazenar tokens (em produção, use banco de dados)
tokens_recuperacao = {}

class MySQLDatabase:
    def __init__(self):
        self.connection_pool = None
        self.config = {
            'host': 'localhost',
            'database': 'projeto',
            'user': 'root',
            'password': '',
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'port': 3306,
            'autocommit': True,
            'pool_name': 'flask_pool',
            'pool_size': 5,
            'pool_reset_session': True,
        }
        self._create_pool()
    
    def _create_pool(self):
        """Cria o pool de conexões"""
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(**self.config)
            print("🚀 Pool de conexões MySQL criado com sucesso!")
        except Error as e:
            print(f"❌ Erro ao criar pool de conexões: {e}")
            raise e
    
    def get_connection(self):
        """Obtém uma conexão do pool"""
        try:
            if self.connection_pool:
                connection = self.connection_pool.get_connection()
                if connection.is_connected():
                    return connection
            raise Error("Pool de conexões não disponível")
        except Error as e:
            print(f"❌ Erro ao obter conexão do pool: {e}")
            raise e
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Executa uma query usando uma conexão do pool
        """
        connection = None
        cursor = None
        
        try:
            # ✅ OBTÉM CONEXÃO DO POOL
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            print(f"📝 Executando query: {query[:100]}...")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if not fetch:
                if not connection.autocommit:
                    connection.commit()
                if query.strip().upper().startswith('INSERT'):
                    result = cursor.lastrowid
                else:
                    result = cursor.rowcount
            else:
                result = cursor.fetchall()
            
            return result
            
        except Error as e:
            print(f"❌ Erro na query: {e}")
            print(f"🔍 Query: {query}")
            if params:
                print(f"🔍 Params: {params}")
            
            # ✅ TENTA RECONEXÃO PARA ERROS DE CONEXÃO
            if "MySQL server has gone away" in str(e) or "Cursor is not connected" in str(e):
                print("🔄 Tentando reconectar...")
                try:
                    # Tenta recriar o pool
                    self._create_pool()
                    # Tenta executar novamente
                    if self.connection_pool:
                        connection = self.get_connection()
                        cursor = connection.cursor(dictionary=True)
                        
                        if params:
                            cursor.execute(query, params)
                        else:
                            cursor.execute(query)
                        
                        if not fetch:
                            if not connection.autocommit:
                                connection.commit()
                            if query.strip().upper().startswith('INSERT'):
                                result = cursor.lastrowid
                            else:
                                result = cursor.rowcount
                        else:
                            result = cursor.fetchall()
                        
                        print("✅ Reconexão bem-sucedida!")
                        return result
                except Error as retry_error:
                    print(f"❌ Falha na reconexão: {retry_error}")
            
            if connection and not connection.autocommit:
                try:
                    connection.rollback()
                except:
                    pass
            raise e
            
        finally:
            # ✅ FECHA RECURSOS
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if connection:
                try:
                    connection.close()
                    # print("🔒 Conexão devolvida ao pool!")
                except:
                    pass
    
    def close(self):
        """Fecha todas as conexões do pool"""
        if self.connection_pool:
            try:
                # O pool fecha automaticamente quando o programa termina
                print("🔒 Pool de conexões MySQL será fechado...")
            except:
                pass

def enviar_email_recuperacao(email_destino, token):
    """
    Envia email de recuperação de senha
    """
    try:
        # Configurar mensagem
        assunto = "Recuperação de Senha - Organização de Tarefas"
        
        # URL para redefinir senha (ajuste conforme sua estrutura)
        url_redefinicao = f"http://localhost:5500/redefinir-senha.html?token={token}"
        
        mensagem_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #667eea; text-align: center;">Recuperação de Senha</h2>
                
                <p>Olá,</p>
                
                <p>Você solicitou a redefinição de sua senha no sistema <strong>Organização de Tarefas</strong>.</p>
                
                <p>Clique no botão abaixo para redefinir sua senha:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{url_redefinicao}" style="background-color: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                        Redefinir Senha
                    </a>
                </div>
                
                <p><strong>Este link expira em 1 hora.</strong></p>
                
                <p>Se você não solicitou esta redefinição, por favor ignore este email.</p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                
                <p style="font-size: 12px; color: #666;">
                    Equipe Organização de Tarefas<br>
                    Este é um email automático, por favor não responda.
                </p>
            </div>
        </body>
        </html>
        """

        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = email_destino
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem_html, 'html'))

        # Conectar e enviar email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        server.send_message(msg)
        server.quit()

        print(f"✅ Email de recuperação enviado para: {email_destino}")
        return True

    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

def create_app():
    """
    Factory function para criar e configurar a aplicação Flask.
    """
    app = Flask(__name__)
    
    # ✅ CORREÇÃO: Configuração CORS ÚNICA
    CORS(app, 
        origins=["http://localhost", "http://127.0.0.1", "http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:3000"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With", "Origin"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        expose_headers=["Content-Type", "Authorization"]
    )
    
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-em-producao'
    
    # ✅ INICIALIZAÇÃO DO BANCO COM TRATAMENTO DE ERRO MELHORADO
    try:
        database_dependency = MySQLDatabase()
        # Testa a conexão
        test_result = database_dependency.execute_query("SELECT 1 as test", fetch=True)
        if test_result and test_result[0]['test'] == 1:
            print("✅ Conexão com MySQL testada e funcionando!")
        else:
            raise Exception("Teste de conexão falhou")
            
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
                        "senha_hash": "$2b$12$K5rDsVk7c5p2wY8zQ8b8XeX5rDsVk7c5p2wY8zQ8b8Xe",
                        "data_criacao": "2024-01-01 00:00:00"
                    }
                ]
                self.mock_projetos = []
                self.mock_tarefas = []
                self.last_id = 1
            
            def execute_query(self, query, params=None, fetch=False):
                print(f"📝 MockDatabase.execute_query: {query[:100]}...")
                
                if query.upper().startswith('INSERT'):
                    self.last_id += 1
                    return self.last_id
                
                if fetch:
                    if 'WHERE email' in query and params:
                        email = params[0]
                        for usuario in self.mock_usuarios:
                            if usuario['email'] == email:
                                return [usuario]
                        return []
                    return self.mock_usuarios
                return 1
            
            def get_connection(self): 
                return self
            def close(self): 
                pass
            def _create_pool(self):
                pass
        
        database_dependency = MockDatabase()
    
    # ✅ INICIALIZAÇÃO DOS COMPONENTES
    try:
        # DAOs
        usuario_dao = UsuarioDAO(database_dependency=database_dependency)
        projeto_dao = ProjetoDAO(database_dependency=database_dependency)
        tarefa_dao = TarefaDAO(database_dependency=database_dependency)
        
        # Services
        usuario_service = UsuarioService(usuario_dao_dependency=usuario_dao)
        projeto_service = ProjetoService(
            projeto_dao_dependency=projeto_dao,
            usuario_dao_dependency=usuario_dao
        )
        tarefa_service = TarefaService(
            tarefa_dao_dependency=tarefa_dao,
            projeto_dao_dependency=projeto_dao,
            usuario_dao_dependency=usuario_dao
        )
        
        # Controls
        usuario_control = UsuarioControl(usuario_service)
        projeto_control = ProjetoControl(projeto_service)
        tarefa_control = TarefaControl(tarefa_service)
        
        # Middlewares
        jwt_middleware = JwtMiddleware()
        usuario_middleware = UsuarioMiddleware()
        projeto_middleware = ProjetoMiddleware()
        tarefa_middleware = TarefaMiddleware()
        
        # Roteadores
        usuario_roteador = UsuarioRoteador(jwt_middleware, usuario_middleware, usuario_control)
        projeto_roteador = ProjetoRoteador(jwt_middleware, projeto_middleware, projeto_control)
        tarefa_roteador = TarefaRoteador(jwt_middleware, tarefa_middleware, tarefa_control)
        
        # Blueprints
        app.register_blueprint(usuario_roteador.create_routes(), url_prefix='/api/usuario')
        app.register_blueprint(projeto_roteador.create_routes(), url_prefix='/api/projeto')
        app.register_blueprint(tarefa_roteador.create_routes(), url_prefix='/api/tarefa')
        
        print("✅ Todos os componentes inicializados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na inicialização dos componentes: {e}")
        print(f"🔍 Stack trace: {traceback.format_exc()}")
        raise e

    # ✅ ROTAS DE RECUPERAÇÃO DE SENHA
    @app.route('/api/auth/recuperar-senha', methods=['POST'])
    def recuperar_senha():
        try:
            data = request.get_json()
            email = data.get('email')

            if not email:
                return jsonify({'success': False, 'error': {'message': 'Email é obrigatório'}}), 400

            # Verificar se o usuário existe
            usuario = usuario_dao.buscar_por_email(email)
            if not usuario:
                # Por segurança, não revelar se o email existe ou não
                return jsonify({'success': True, 'message': 'Se o email existir, enviaremos um link de recuperação'})

            # Gerar token único
            token = secrets.token_urlsafe(32)
            expiracao = datetime.now() + timedelta(hours=1)  # Token válido por 1 hora

            # Armazenar token (em produção, salve no banco de dados)
            tokens_recuperacao[token] = {
                'user_id': usuario['id'],
                'email': email,
                'expiracao': expiracao
            }

            # Enviar email
            if enviar_email_recuperacao(email, token):
                return jsonify({'success': True, 'message': 'Email de recuperação enviado com sucesso'})
            else:
                return jsonify({'success': False, 'error': {'message': 'Erro ao enviar email'}}), 500

        except Exception as e:
            print(f"❌ Erro em recuperar_senha: {e}")
            return jsonify({'success': False, 'error': {'message': str(e)}}), 500

    @app.route('/api/auth/redefinir-senha', methods=['POST'])
    def redefinir_senha():
        try:
            data = request.get_json()
            token = data.get('token')
            nova_senha = data.get('nova_senha')

            if not token or not nova_senha:
                return jsonify({'success': False, 'error': {'message': 'Token e nova senha são obrigatórios'}}), 400

            # Verificar token
            token_data = tokens_recuperacao.get(token)
            if not token_data:
                return jsonify({'success': False, 'error': {'message': 'Token inválido ou expirado'}}), 400

            if datetime.now() > token_data['expiracao']:
                del tokens_recuperacao[token]
                return jsonify({'success': False, 'error': {'message': 'Token expirado'}}), 400

            # Buscar usuário
            usuario = usuario_dao.buscar_por_id(token_data['user_id'])
            if not usuario:
                return jsonify({'success': False, 'error': {'message': 'Usuário não encontrado'}}), 404

            # Atualizar senha
            senha_hash = generate_password_hash(nova_senha)
            usuario_dao.atualizar_senha(token_data['user_id'], senha_hash)

            # Remover token usado
            del tokens_recuperacao[token]

            return jsonify({'success': True, 'message': 'Senha redefinida com sucesso'})

        except Exception as e:
            print(f"❌ Erro em redefinir_senha: {e}")
            return jsonify({'success': False, 'error': {'message': str(e)}}), 500

    # ✅ HANDLERS DE ERRO
    @app.errorhandler(Exception)
    def handle_global_exception(e):
        print(f"❌ ERRO GLOBAL CAPTURADO: {e}")
        print(f"🔍 Stack trace: {traceback.format_exc()}")
        
        import logging
        logging.basicConfig(filename='app_errors.log', level=logging.ERROR)
        logging.error(f"Erro global: {e}\n{traceback.format_exc()}")
        
        return jsonify({
            "success": False,
            "error": {
                "message": "Erro interno do servidor",
                "code": 500,
                "details": str(e) if app.debug else "Contate o administrador"
            }
        }), 500
    
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({
            "success": False,
            "error": {
                "message": "Endpoint não encontrado",
                "code": 404
            }
        }), 404

    # ✅ ROTAS DE HEALTH CHECK
    @app.route('/health', methods=['GET'])
    def health_check():
        try:
            # Testa o banco
            if hasattr(database_dependency, 'execute_query'):
                test_result = database_dependency.execute_query("SELECT 1 as status", fetch=True)
                db_status = "connected" if test_result and test_result[0]['status'] == 1 else "error"
            else:
                db_status = "mock"
                
            return jsonify({
                "status": "healthy",
                "message": "API está funcionando corretamente",
                "database": db_status,
                "timestamp": traceback.format_stack()[-1] if app.debug else None
            })
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "message": "Problemas na API",
                "error": str(e),
                "database": "error"
            }), 500
    
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            "message": "✅ API Flask funcionando!",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "usuarios": "/api/usuario/",
                "cadastro": "POST /api/usuario/",
                "login": "POST /api/usuario/login",
                "recuperar_senha": "POST /api/auth/recuperar-senha",
                "redefinir_senha": "POST /api/auth/redefinir-senha",
                "projetos": "/api/projeto/",
                "tarefas": "/api/tarefa/"
            },
            "documentation": "Consulte a documentação para mais detalhes"
        })
    
    # ✅ TEARDOWN PARA LIMPEZA
    @app.teardown_appcontext
    def close_db_connection(exception=None):
        if hasattr(database_dependency, 'close'):
            try:
                database_dependency.close()
            except Exception as e:
                print(f"❌ Erro ao fechar conexões: {e}")
    
    print("=" * 60)
    print("🚀 FLASK APP INICIALIZADA COM SUCESSO!")
    print("📍 URL: http://localhost:5000")
    print("📊 Banco de dados: projeto (com pool de conexões)")
    print("🔧 Modo: Debug" if app.debug else "🔧 Modo: Produção")
    print("👤 Usuários: Isolados por ID")
    print("📁 Projetos: Filtrados por usuário") 
    print("✅ Tarefas: Filtradas por usuário")
    print("✅ CORS configurado corretamente")
    print("✅ Sistema de recuperação de senha ativo")
    print("=" * 60)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🔥 Iniciando servidor Flask...")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        print("🔄 Reiniciando servidor em 5 segundos...")
        import time
        time.sleep(5)
        try:
            app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        except Exception as e2:
            print(f"❌ ERRO CRÍTICO NOVAMENTE: {e2}")
            print("💡 O servidor não conseguiu reiniciar. Verifique:")
            print("   - XAMPP MySQL está rodando?")
            print("   - Porta 5000 está livre?")
            print("   - Banco 'projeto' existe?")