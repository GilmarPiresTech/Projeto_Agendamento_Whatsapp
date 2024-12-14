from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from utils.excel_utils import verificar_ou_criar_excel, carregar_agendamentos, salvar_no_excel, excluir_folga
from utils.config_utils import carregar_configuracoes, salvar_horarios_no_excel
from utils.consulta_utils import (
    carregar_tipos_consulta,
    salvar_tipo_consulta_no_excel,
    gerar_dias_disponiveis,
    verificar_dia_disponivel,
    verificar_horario_trabalho,
    verificar_disponibilidade
)
import os

# Inicialização do Flask
app = Flask(__name__)
app.secret_key = 'chave_secreta_para_mensagens_flash'

# Configuração do caminho do arquivo Excel
ARQUIVO_EXCEL = os.path.join(os.path.expanduser('~'), 'Desktop', 'agendamentos.xlsx')
verificar_ou_criar_excel(ARQUIVO_EXCEL)

# Rota principal
@app.route('/')
def index():
    tipos_consulta = carregar_tipos_consulta(ARQUIVO_EXCEL)
    config = carregar_configuracoes(ARQUIVO_EXCEL)
    agendamentos = carregar_agendamentos(ARQUIVO_EXCEL)
    dias_disponiveis = gerar_dias_disponiveis(config, tipos_consulta, agendamentos)
    return render_template('form.html', tipos_consulta=tipos_consulta, dias_disponiveis=dias_disponiveis)

# Rota para submissão de agendamentos
@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    email = request.form['email']
    celular = request.form['celular']
    tipo_consulta = request.form['tipo_consulta']
    data = request.form['selected_date']
    horario = request.form['selected_time']
    comentario = request.form.get('comentario', '')

    # Validações
    if not all([nome, email, celular, data, horario, tipo_consulta]):
        flash('Preencha todos os campos obrigatórios.', 'error')
        return redirect(url_for('index'))
    if not verificar_dia_disponivel(data, ARQUIVO_EXCEL):
        flash('Data indisponível para agendamento.', 'error')
        return redirect(url_for('index'))
    if not verificar_horario_trabalho(data, horario, ARQUIVO_EXCEL):
        flash('Horário fora do expediente.', 'error')
        return redirect(url_for('index'))
    if not verificar_disponibilidade(data, horario, ARQUIVO_EXCEL):
        flash('Horário já ocupado.', 'error')
        return redirect(url_for('index'))

    salvar_no_excel(ARQUIVO_EXCEL, nome, email, celular, data, horario, tipo_consulta, comentario)
    flash('Agendamento realizado com sucesso!', 'success')
    return redirect(url_for('index'))

# Rota para exibir o calendário de agendamentos
@app.route('/calendario')
def calendario():
    agendamentos = carregar_agendamentos(ARQUIVO_EXCEL)
    return render_template('calendario.html', agendamentos=agendamentos)

# Rota para gerenciar tipos de consulta
@app.route('/tipos-consulta', methods=['GET', 'POST'])
def tipos_consulta():
    if request.method == 'POST':
        tipo = request.form['tipo']
        duracao = request.form['duracao']
        valor = request.form['valor']
        if not tipo or not duracao or not valor:
            flash('Preencha todos os campos.', 'error')
            return redirect(url_for('tipos_consulta'))
        salvar_tipo_consulta_no_excel(tipo, duracao, valor, ARQUIVO_EXCEL)
        flash('Tipo de consulta cadastrado com sucesso!', 'success')
        return redirect(url_for('tipos_consulta'))
    else:
        tipos = carregar_tipos_consulta(ARQUIVO_EXCEL)
        return render_template('tipos_consulta.html', tipos=tipos)

# Inicialização do servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
