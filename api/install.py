import subprocess
import sys
import mysql.connector
from mysql.connector import errorcode

# --------- Passo 1: Instalar bibliotecas ---------
def install_packages():
    packages = ["flask", "mysql-connector-python", "bcrypt", "pyjwt", "flask-cors"]
    for pkg in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# --------- Passo 2: Criar banco de dados a partir do arquivo SQL ---------
def setup_database(host="127.0.0.1", user="root", password="", database="gestao_rh", port=3306, sql_file="./docs/Banco.sql"):
    try:
        # Conecta ao MySQL (sem especificar database ainda)
        cnx = mysql.connector.connect(host=host, user=user, password=password, port=port)
        cursor = cnx.cursor()

        # Executa o SQL do arquivo
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Separar comandos individuais por ';'
        commands = sql_script.split(';')

        for command in commands:
            command = command.strip()
            if command:
                cursor.execute(command)

        cnx.commit()
        print(f"Script SQL '{sql_file}' executado com sucesso!")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Usuário ou senha incorretos")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()

# --------- Execução ---------
if __name__ == "__main__":
    print("Instalando pacotes...")
    install_packages()
    print("Configurando banco de dados...")
    setup_database(password="")  # coloque sua senha do MySQL aqui
