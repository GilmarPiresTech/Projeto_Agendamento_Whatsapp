import mysql.connector
from mysql.connector import Error

# Configurações do MySQL
DB_HOST = "186.202.152.237"
DB_USER = "agendadorwhats"  # Substitua pelo seu nome de usuário do MySQL
DB_PASSWORD = "Gp20262595!"  # Substitua pela sua senha do MySQL
DB_NAME = "agendadorwhats"  # Substitua pelo nome do banco que deseja criar

def create_database():
    try:
        # Conexão com o MySQL
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Criação do banco de dados
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"Banco de dados '{DB_NAME}' criado ou já existe.")
            cursor.close()
        else:
            print("Erro: Não foi possível conectar ao MySQL.")
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    create_database()
