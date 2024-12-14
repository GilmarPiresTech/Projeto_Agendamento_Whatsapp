import smtplib
from email.mime.text import MIMEText
import os

def enviar_confirmacao_agendamento(destinatario, nome_cliente, data, horario, tipo_consulta):
    # Pegando as credenciais das variáveis de ambiente
    user = os.environ.get('EMAIL_USERNAME')  # Seu usuário (email completo)
    password = os.environ.get('EMAIL_PASSWORD')  # Sua senha de email
    sender = user  # O remetente será o próprio usuário

    # Verificando se as variáveis foram carregadas corretamente (debug temporário)
    if not user or not password:
        print("[ERRO] As variáveis de ambiente EMAIL_USERNAME ou EMAIL_PASSWORD não estão configuradas.")
        return

    print(f"[DEBUG] Usando o email: {user}")

    # Criando o corpo da mensagem
    corpo_mensagem = f"""
    Olá {nome_cliente},

    Seu agendamento para {tipo_consulta} foi realizado com sucesso.

    Data: {data}
    Horário: {horario}

    Agradecemos por escolher nossos serviços.

    Atenciosamente,
    Equipe de Agendamentos.
    """

    # Configurando a mensagem MIME
    msg = MIMEText(corpo_mensagem)
    msg['Subject'] = 'Confirmação de Agendamento'
    msg['From'] = sender
    msg['To'] = destinatario

    try:
        # Iniciando a conexão SMTP com a Locaweb usando SSL e a porta 465
        with smtplib.SMTP_SSL('email-ssl.com.br', 465) as s:
            s.set_debuglevel(1)  # Habilita o debug para ver os detalhes da conexão
            s.login(user, password)  # Logando no servidor SMTP
            s.sendmail(sender, [destinatario], msg.as_string())  # Enviando o email

        print("[INFO] Email de confirmação enviado com sucesso.")

    except Exception as e:
        print(f"[ERRO] Falha ao enviar email: {e}")

