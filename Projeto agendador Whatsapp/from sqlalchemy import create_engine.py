from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configuração do SQLAlchemy para conectar ao MySQL
DATABASE_URI = 'mysql+mysqlconnector://agendadorwhats:Gp20262595%40@179.188.16.14:3306/agendadorwhats?charset=utf8mb4'

# Criar o engine para o banco de dados
engine = create_engine(DATABASE_URI, pool_recycle=299, pool_timeout=20)

# Função para testar a conexão com o banco de dados
def testar_conexao():
    try:
        # Tentativa de criar uma sessão
        Session = sessionmaker(bind=engine)
        session = Session()

        # Executa uma consulta simples (tabela 'dual' usada para teste no MySQL)
        result = session.execute("SELECT 1")
        
        # Itera sobre o resultado para garantir que a consulta foi bem-sucedida
        for row in result:
            print(f"Conexão bem-sucedida. Resultado da consulta: {row[0]}")

        # Fecha a sessão após o testec
        session.close()
        
    except SQLAlchemyError as e:
        # Exibe o erro caso a conexão falhe
        print(f"Erro ao conectar ao banco de dados: {str(e)}")

print(f"Engine: {engine}")
print(f"Testing connection to: {DATABASE_URI}")


# Chama a função de teste de conexão
if __name__ == '__main__':
    testar_conexao()