from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from datetime import datetime, timedelta, time
import uuid
import logging
from flask_sqlalchemy import SQLAlchemy
from email_service import enviar_confirmacao_agendamento

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_mensagens_flash'

# Configuração do SQLAlchemy para conectar ao MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://agendadorwhats:Gp250412%40@agendadorwhats.mysql.dbaas.com.br:3306/agendadorwhats?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)


# Configuração básica do logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Modelos de Tabelas MySQL

# Modelo da tabela Agendamento
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'  # Nome da tabela personalizada
    id = db.Column(db.String(255), primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    celular = db.Column(db.String(50))
    data = db.Column(db.Date)
    horario = db.Column(db.Time)
    tipo_consulta = db.Column(db.String(50))
    comentario = db.Column(db.String(255))

# Modelo da tabela Configuracao
class Configuracao(db.Model):
    __tablename__ = 'configuração'  # Nome da tabela personalizada
    dia = db.Column(db.String(50), primary_key=True)
    inicio = db.Column(db.Time)
    inicio_almoco = db.Column(db.Time)
    fim_almoco = db.Column(db.Time)
    fim = db.Column(db.Time)
    status = db.Column(db.String(50))
    nao_ha_almoco = db.Column(db.String(10))

# Modelo da tabela Folga
class Folga(db.Model):
    __tablename__ = 'folgas'  # Nome da tabela personalizada
    data = db.Column(db.Date, primary_key=True)

# Modelo da tabela TipoConsulta
class TipoConsulta(db.Model):
    __tablename__ = 'tipos_de_consulta'  # Nome da tabela personalizada
    tipo = db.Column(db.String(50), primary_key=True)
    duracao = db.Column(db.Integer)
    valor = db.Column(db.Numeric(10, 2))


# Criar tabelas no banco de dados
with app.app_context():
    db.create_all()

# Função para carregar os tipos de consulta do MySQL
def carregar_tipos_consulta():
    try:
        tipos_consulta = TipoConsulta.query.all()
        return [{'Tipo': tipo.tipo, 'Duração': tipo.duracao, 'Valor': tipo.valor} for tipo in tipos_consulta]
    except Exception as e:
        print(f"[ERRO] Erro ao carregar tipos de consulta: {e}")
        flash('Erro ao carregar tipos de consulta.', 'error')
        return []

# Função para salvar um novo tipo de consulta no MySQL
def salvar_tipo_consulta_no_mysql(tipo, duracao, valor):
    try:
        if TipoConsulta.query.filter_by(tipo=tipo).first():
            flash('Este tipo de consulta já está cadastrado.', 'error')
            return
        novo_tipo = TipoConsulta(tipo=tipo, duracao=int(duracao), valor=float(valor))
        db.session.add(novo_tipo)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar tipo de consulta: {e}")
        flash('Erro ao salvar tipo de consulta.', 'error')

# Função para carregar agendamentos do MySQL
def carregar_agendamentos():
    try:
        agendamentos = Agendamento.query.all()
        return [{'ID': agendamento.id, 'Nome': agendamento.nome, 'Email': agendamento.email, 'Celular': agendamento.celular,
                 'Data': agendamento.data, 'Horário': agendamento.horario, 'Tipo de Consulta': agendamento.tipo_consulta, 'Comentário': agendamento.comentario}
                for agendamento in agendamentos]
    except Exception as e:
        print(f"Erro ao carregar agendamentos: {e}")
        return []

# Função para salvar um novo agendamento no MySQL
def salvar_no_mysql(nome, email, celular, data, horario, tipo_consulta, comentario):
    try:
        agendamento_id = str(uuid.uuid4())
        novo_agendamento = Agendamento(id=agendamento_id, nome=nome, email=email, celular=celular, data=data,
                                       horario=horario, tipo_consulta=tipo_consulta, comentario=comentario)
        db.session.add(novo_agendamento)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar agendamento: {e}")
        flash('Erro ao salvar agendamento.', 'error')

# Função para carregar folgas do MySQL
def carregar_folgas():
    try:
        folgas = Folga.query.all()
        return [folga.data for folga in folgas]
    except Exception as e:
        print(f"Erro ao carregar folgas: {e}")
        flash('Erro ao carregar folgas.', 'error')
        return []

# Função para salvar uma nova folga no MySQL
def marcar_folga_no_mysql(data):
    try:
        if Folga.query.filter_by(data=data).first():
            flash('Esta data já está marcada como folga.', 'error')
            return
        nova_folga = Folga(data=data)
        db.session.add(nova_folga)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar folga: {e}")
        flash('Erro ao salvar folga.', 'error')

# Função para excluir uma folga do MySQL
def excluir_folga(data):
    try:
        folga = Folga.query.filter_by(data=data).first()
        if folga:
            db.session.delete(folga)
            db.session.commit()
            flash('Folga excluída com sucesso!', 'success')
        else:
            flash('Folga não encontrada.', 'error')
    except Exception as e:
        print(f"Erro ao excluir folga: {e}")
        flash('Erro ao excluir folga.', 'error')

# Função para carregar configurações de horários do MySQL
def carregar_configuracoes():
    try:
        configuracoes = Configuracao.query.all()
        config = {}
        for conf in configuracoes:
            config[conf.dia] = {
                'Início': conf.inicio,
                'Início_Almoço': conf.inicio_almoco,
                'Fim_Almoço': conf.fim_almoco,
                'Fim': conf.fim,
                'Status': conf.status,
                'Nao_Ha_Almoco': conf.nao_ha_almoco
            }
        return config
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        flash('Erro ao carregar configurações de horários.', 'error')
        return {}

# Função para salvar configurações de horários no MySQL
def salvar_horarios_no_mysql(dias, inicio, fim, folgas, inicio_almoco, fim_almoco, nao_ha_almoco):
    try:
        for i in range(len(dias)):
            status = 'Folga' if dias[i] in folgas else 'Trabalho'

            logging.info(f"Processando dia: {dias[i]} com status: {status}")
            
            almoco_inicio = None
            almoco_fim = None

            # Verificação para manter os valores atuais se não forem preenchidos
            conf = Configuracao.query.filter_by(dia=dias[i]).first()

            if conf:
                # Atualize apenas se o valor for enviado no formulário
                if inicio[i]:
                    conf.inicio = datetime.strptime(inicio[i], '%H:%M').time()
                    logging.info(f"Início atualizado para {conf.inicio} no dia {dias[i]}")
                if fim[i]:
                    conf.fim = datetime.strptime(fim[i], '%H:%M').time()
                    logging.info(f"Fim atualizado para {conf.fim} no dia {dias[i]}")
                if inicio_almoco[i] and not nao_ha_almoco[i]:
                    almoco_inicio = datetime.strptime(inicio_almoco[i], '%H:%M').time()
                if fim_almoco[i] and not nao_ha_almoco[i]:
                    almoco_fim = datetime.strptime(fim_almoco[i], '%H:%M').time()

                # Atualiza os valores do almoço apenas se foram enviados
                if almoco_inicio:
                    conf.inicio_almoco = almoco_inicio
                    logging.info(f"Início do almoço atualizado para {conf.inicio_almoco} no dia {dias[i]}")
                if almoco_fim:
                    conf.fim_almoco = almoco_fim
                    logging.info(f"Fim do almoço atualizado para {conf.fim_almoco} no dia {dias[i]}")

                conf.status = status
                conf.nao_ha_almoco = 'Sim' if nao_ha_almoco[i] else 'Não'
                logging.info(f"Status atualizado para {conf.status} no dia {dias[i]}")

            else:
                # Criação de nova configuração se ainda não existe
                nova_config = Configuracao(
                    dia=dias[i],
                    inicio=datetime.strptime(inicio[i], '%H:%M').time() if inicio[i] else None,
                    fim=datetime.strptime(fim[i], '%H:%M').time() if fim[i] else None,
                    inicio_almoco=datetime.strptime(inicio_almoco[i], '%H:%M').time() if inicio_almoco[i] and not nao_ha_almoco[i] else None,
                    fim_almoco=datetime.strptime(fim_almoco[i], '%H:%M').time() if fim_almoco[i] and not nao_ha_almoco[i] else None,
                    status=status,
                    nao_ha_almoco='Sim' if nao_ha_almoco[i] else 'Não'
                )
                db.session.add(nova_config)
                logging.info(f"Nova configuração criada para o dia {dias[i]}")

        # Tenta fazer o commit no banco de dados
        logging.info("Tentando salvar as configurações no banco de dados...")
        db.session.commit()
        logging.info("Configurações de horários salvas com sucesso!")
        flash('Configurações de horários salvas com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()  # Em caso de erro, faz o rollback
        logging.error(f"Erro ao salvar configurações de horários: {e}", exc_info=True)
        flash('Erro ao salvar configurações de horários.', 'error')




# Função para verificar disponibilidade do horário
def verificar_disponibilidade(data, horario, duracao_consulta):
    try:
        agendamentos = carregar_agendamentos()
        horario_inicio_consulta = datetime.strptime(f"{data} {horario}", '%Y-%m-%d %H:%M')
        horario_fim_consulta = horario_inicio_consulta + timedelta(minutes=int(duracao_consulta))

        for agendamento in agendamentos:
            if agendamento['Data'] == data:
                agendamento_inicio = datetime.strptime(f"{agendamento['Data']} {agendamento['Horário']}", '%Y-%m-%d %H:%M')
                duracao_agendamento = int(next(
                    (int(tipo['Duração']) for tipo in carregar_tipos_consulta()
                     if tipo['Tipo'].strip().lower() == agendamento['Tipo de Consulta'].strip().lower()),
                    15
                ))
                agendamento_fim = agendamento_inicio + timedelta(minutes=duracao_agendamento)

                if (horario_inicio_consulta < agendamento_fim) and (horario_fim_consulta > agendamento_inicio):
                    return False
        return True
    except Exception as e:
        print(f"Erro ao verificar disponibilidade: {e}")
        flash('Erro ao verificar disponibilidade do horário.', 'error')
        return False

# Função para gerar todos os horários disponíveis
def gerar_todos_horarios_disponiveis(inicio, fim):
    horarios_disponiveis = []
    
    # Verifica se 'inicio' e 'fim' são objetos datetime.time e converte para string no formato '%H:%M'
    if isinstance(inicio, time):  # Aqui usamos 'time' diretamente
        inicio = inicio.strftime('%H:%M')
    if isinstance(fim, time):  # Aqui usamos 'time' diretamente
        fim = fim.strftime('%H:%M')

    horario_atual = datetime.strptime(inicio, '%H:%M')
    horario_fim_expediente = datetime.strptime(fim, '%H:%M')

    while horario_atual < horario_fim_expediente:
        horarios_disponiveis.append(horario_atual.strftime('%H:%M'))
        horario_atual += timedelta(minutes=15)  # Mantemos o incremento de 15 minutos
    return horarios_disponiveis



# Verificação de disponibilidade de horário
def verificar_horario_disponivel(horario, duracao_consulta, agendamentos_existentes, data, fim_expediente, inicio_almoco=None, fim_almoco=None, nao_ha_almoco=False):
    horario_inicio = datetime.strptime(f"{data} {horario}", '%Y-%m-%d %H:%M')
    horario_fim = horario_inicio + timedelta(minutes=duracao_consulta)

    # Verifica se o horário final está dentro do expediente
    fim_expediente_datetime = datetime.strptime(f"{data} {fim_expediente}", '%Y-%m-%d %H:%M')
    if horario_fim > fim_expediente_datetime:
        return False

    # Lógica de verificação de almoço
    if not nao_ha_almoco and inicio_almoco and fim_almoco:
        inicio_almoco_datetime = datetime.strptime(f"{data} {inicio_almoco}", '%Y-%m-%d %H:%M')
        fim_almoco_datetime = datetime.strptime(f"{data} {fim_almoco}", '%Y-%m-%d %H:%M')

        # Bloquear agendamentos que ocorram durante o horário de almoço
        if (horario_inicio >= inicio_almoco_datetime and horario_inicio < fim_almoco_datetime) or \
           (horario_fim > inicio_almoco_datetime and horario_inicio < fim_almoco_datetime):
            return False

    # Verifica sobreposição com agendamentos existentes
    for agendamento in agendamentos_existentes:
        if agendamento['Data'] == data:
            agendamento_inicio = datetime.strptime(f"{agendamento['Data']} {agendamento['Horário']}", '%Y-%m-%d %H:%M')
            duracao_agendamento = int(next(
                (int(tipo['Duração']) for tipo in carregar_tipos_consulta()
                 if tipo['Tipo'].strip().lower() == agendamento['Tipo de Consulta'].strip().lower()),
                15  # Valor padrão se não encontrado
            ))
            agendamento_fim = agendamento_inicio + timedelta(minutes=duracao_agendamento)

            if (horario_inicio < agendamento_fim) and (horario_fim > agendamento_inicio):
                return False

    return True

# Função para gerar dias disponíveis
def gerar_dias_disponiveis(config, duracao_consulta, agendamentos_existentes, folgas):
    dias_disponiveis = {}
    hoje = datetime.today()

    for i in range(90):  # Ajuste o número de dias conforme necessário
        dia = hoje + timedelta(days=i)
        data_str = dia.strftime('%Y-%m-%d')
        dia_semana = dia.strftime('%A')
        dias_semana_portugues = {
            'Monday': 'Segunda-feira',
            'Tuesday': 'Terça-feira',
            'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira',
            'Friday': 'Sexta-feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        dia_semana_pt = dias_semana_portugues.get(dia_semana)
        configuracao = config.get(dia_semana_pt)

        if configuracao and configuracao['Status'] == 'Trabalho' and data_str not in folgas:
            inicio = configuracao['Início']
            fim = configuracao['Fim']
            inicio_almoco = configuracao.get('Início_Almoço', None)
            fim_almoco = configuracao.get('Fim_Almoço', None)
            nao_ha_almoco = configuracao.get('Nao_Ha_Almoco', 'Não') == 'Sim'

            if inicio and fim:
                # Gera todos os horários possíveis
                todos_horarios = gerar_todos_horarios_disponiveis(inicio, fim)

                # Filtra horários disponíveis
                horarios_validos = []
                for horario in todos_horarios:
                    if verificar_horario_disponivel(horario, duracao_consulta, agendamentos_existentes, data_str, fim, inicio_almoco, fim_almoco, nao_ha_almoco):
                        horarios_validos.append(horario)

                if horarios_validos:
                    dias_disponiveis[data_str] = horarios_validos

    return dias_disponiveis

# Rota principal que renderiza o formulário de agendamento
@app.route('/', methods=['GET', 'POST'])
def index():
    tipos_consulta = carregar_tipos_consulta()
    config = carregar_configuracoes()
    agendamentos_existentes = carregar_agendamentos()
    folgas = carregar_folgas()

    dias_disponiveis = {}
    duracao_consulta = None

    if request.method == 'POST':
        tipo_selecionado = request.form.get('tipo_consulta')
        duracao_consulta = next(
            (int(tipo['Duração']) for tipo in tipos_consulta if tipo['Tipo'] == tipo_selecionado),
            15
        )
    else:
        # Duração padrão se nenhum tipo for selecionado
        if tipos_consulta:
            tipo_selecionado = tipos_consulta[0]['Tipo']
            duracao_consulta = int(tipos_consulta[0]['Duração'])
        else:
            tipo_selecionado = None

    if tipos_consulta and config and duracao_consulta:
        dias_disponiveis = gerar_dias_disponiveis(config, duracao_consulta, agendamentos_existentes, folgas)

    return render_template(
        'form.html',
        tipos_consulta=tipos_consulta,
        dias_disponiveis=dias_disponiveis,
        tipo_selecionado=tipo_selecionado
    )

# Função para submissão do agendamento
@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    email = request.form['email']
    celular = request.form['celular']
    tipo_consulta = request.form['tipo_consulta']
    comentario = request.form['comentario']
    data = request.form.get('selected_date')
    horario = request.form.get('selected_time')

    tipos_consulta = carregar_tipos_consulta()
    duracao_consulta = next(
        (int(tipo['Duração']) for tipo in tipos_consulta if tipo['Tipo'] == tipo_consulta),
        15
    )

    if not nome or not email or not celular or not data or not horario or not tipo_consulta:
        flash('Por favor, preencha todos os campos obrigatórios.', 'error')
        return redirect(url_for('index'))

    if not verificar_disponibilidade(data, horario, duracao_consulta):
        flash('O horário selecionado já está ocupado. Por favor, escolha outro horário ou dia.', 'error')
        return redirect(url_for('index'))

    salvar_no_mysql(nome, email, celular, data, horario, tipo_consulta, comentario)
    flash('Agendamento realizado com sucesso!', 'success')

    # Enviar o email de confirmação de agendamento (sem o argumento `mail`)
    enviar_confirmacao_agendamento(email, nome, data, horario, tipo_consulta)

    return redirect(url_for('index'))

# Rota para cancelar agendamentos
@app.route('/cancelar', methods=['POST'])
def cancelar_agendamento():
    agendamento_id = request.form.get('id')
    try:
        agendamento = Agendamento.query.filter_by(id=agendamento_id).first()
        if agendamento:
            db.session.delete(agendamento)
            db.session.commit()
            flash('Agendamento cancelado com sucesso.', 'success')
        return redirect(url_for('calendario'))
    except Exception as e:
        print(f"Erro ao cancelar agendamento: {e}")
        flash('Erro ao cancelar agendamento. Tente novamente.', 'error')
        return redirect(url_for('calendario'))

# Rota para exibir o calendário de agendamentos
@app.route('/calendario')
def calendario():
    agendamentos = carregar_agendamentos()
    return render_template('calendario.html', agendamentos=agendamentos)

# Rota para marcar um dia como folga
@app.route('/marcar-folga', methods=['GET', 'POST'])
def marcar_folga():
    if request.method == 'POST':
        data = request.form['data_folga']
        if not data:
            flash('Por favor, selecione uma data.', 'error')
            return redirect(url_for('marcar_folga'))
        marcar_folga_no_mysql(data)
        flash(f'O dia {data} foi marcado como folga!', 'success')
        return redirect(url_for('marcar_folga'))
    else:
        folgas = carregar_folgas()
        return render_template('marcar_folga.html', folgas=folgas)

# Rota para excluir uma folga específica
@app.route('/excluir_folga', methods=['POST'])
def excluir_folga_route():
    data = request.form['data']
    excluir_folga(data)
    return redirect(url_for('marcar_folga'))

# Rota para configurar horários de trabalho
@app.route('/config-horarios', methods=['GET', 'POST'])
def config_horarios():
    if request.method == 'POST':
        try:
            dias = request.form.getlist('dia')  # Captura todos os dias da semana enviados
            horarios_inicio = request.form.getlist('inicio')
            horarios_fim = request.form.getlist('fim')
            inicio_almoco = request.form.getlist('inicio_almoco')
            fim_almoco = request.form.getlist('fim_almoco')
            folgas = request.form.getlist('folga')

            nao_ha_almoco = []
            for i in range(len(dias)):
                nao_ha_almoco.append('true' if f'nao_ha_almoco_{i}' in request.form else 'false')

            nao_ha_almoco = [nh == 'true' for nh in nao_ha_almoco]

            salvar_horarios_no_mysql(dias, horarios_inicio, horarios_fim, folgas, inicio_almoco, fim_almoco, nao_ha_almoco)

            flash('Configurações de horários atualizadas com sucesso!', 'success')
        except Exception as e:
            logging.error(f"Erro ao salvar configurações: {e}")
            flash('Erro ao salvar configurações de horários.', 'error')

        return redirect(url_for('config_horarios'))
    else:
        config = carregar_configuracoes()
        return render_template('config_horarios.html', config=config)


# Função para cadastrar tipos de consulta
@app.route('/tipos-consulta', methods=['GET', 'POST'])
def tipos_consulta():
    if request.method == 'POST':
        tipo = request.form['tipo']
        duracao = request.form['duracao']
        valor = request.form['valor']
        if not tipo or not duracao or not valor:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('tipos_consulta'))
        salvar_tipo_consulta_no_mysql(tipo, duracao, valor)
        flash('Tipo de consulta cadastrado com sucesso!', 'success')
        return redirect(url_for('tipos_consulta'))
    else:
        tipos = carregar_tipos_consulta()
        return render_template('tipos_consulta.html', tipos=tipos)

# Rota para editar tipo de consulta
@app.route('/editar_tipo_consulta/<int:id>', methods=['GET', 'POST'])
def editar_tipo_consulta(id):
    tipos = carregar_tipos_consulta()

    if id < 0 or id >= len(tipos):
        flash('Tipo de consulta não encontrado.', 'error')
        return redirect(url_for('tipos_consulta'))

    tipo_consulta = tipos[id]

    if request.method == 'POST':
        novo_tipo = request.form['tipo']
        nova_duracao = request.form['duracao']
        novo_valor = request.form['valor']

        if not novo_tipo or not nova_duracao or not novo_valor:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('editar_tipo_consulta', id=id))

        tipos[id]['Tipo'] = novo_tipo
        tipos[id]['Duração'] = int(nova_duracao)
        tipos[id]['Valor'] = float(novo_valor)

        salvar_tipo_consulta_no_mysql(novo_tipo, nova_duracao, novo_valor)
        flash('Tipo de consulta atualizado com sucesso!', 'success')
        return redirect(url_for('tipos_consulta'))

    return render_template('editar_tipo_consulta.html', tipo=tipo_consulta, id=id)

# Rota para excluir tipo de consulta
@app.route('/excluir_tipo_consulta/<int:id>', methods=['POST'])
def excluir_tipo_consulta(id):
    tipos = carregar_tipos_consulta()

    if id < 0 or id >= len(tipos):
        flash('Tipo de consulta não encontrado.', 'error')
        return redirect(url_for('tipos_consulta'))

    tipo = TipoConsulta.query.filter_by(tipo=tipos[id]['Tipo']).first()
    if tipo:
        db.session.delete(tipo)
        db.session.commit()
    flash('Tipo de consulta excluído com sucesso!', 'success')
    return redirect(url_for('tipos_consulta'))

# Iniciar a aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
