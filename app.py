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

@app.route('/config-horarios')
def config_horarios():
    # Lógica para carregar as configurações de horários
    return render_template('config_horarios.html')

@app.route('/marcar-folga', methods=['GET', 'POST'])
def marcar_folga():
    if request.method == 'POST':
        # Lógica para processar dados enviados no formulário de marcação de folgas
        folga = request.form.get("data_folga")  # Exemplo de campo no formulário
        # Adicione lógica para salvar essa folga em um arquivo Excel
        return "Folga marcada com sucesso!"
    return render_template('marcar_folga.html')

@app.route('/editar-tipo-consulta/<int:id>', methods=['GET', 'POST'])
def editar_tipo_consulta(id):
    import pandas as pd

    # Caminho do arquivo onde os dados estão armazenados
    caminho_arquivo = "dados_tipos_consulta.xlsx"

    if request.method == 'POST':
        try:
            # Ler os dados existentes
            df = pd.read_excel(caminho_arquivo)

            # Atualizar o tipo de consulta
            df.loc[df['id'] == id, 'nome'] = request.form.get("nome_tipo")
            df.loc[df['id'] == id, 'duracao'] = request.form.get("duracao")
            df.loc[df['id'] == id, 'preco'] = request.form.get("preco")

            # Salvar de volta no Excel
            df.to_excel(caminho_arquivo, index=False)

            return f"Tipo de consulta {id} atualizado com sucesso!"
        except Exception as e:
            return f"Erro ao atualizar o tipo de consulta: {str(e)}"

    try:
        # Ler os dados para exibição no formulário
        df = pd.read_excel(caminho_arquivo)
        tipo_consulta = df[df['id'] == id].to_dict('records')[0]
    except Exception as e:
        return f"Erro ao carregar os dados: {str(e)}"

    return render_template('editar_tipo_consulta.html', tipo_consulta=tipo_consulta)



@app.route('/agendar', methods=['POST'])
def agendar():
    try:
        # Capturar dados do formulário de agendamento
        nome = request.form.get("nome")
        data = request.form.get("data")
        tipo_consulta = request.form.get("tipo_consulta")
        # Salve no arquivo Excel
        return "Agendamento realizado com sucesso!"
    except Exception as e:
        return f"Erro ao realizar agendamento: {str(e)}"
    
    @app.route('/tipos-consulta', methods=['GET'])
def tipos_consulta():
    # Simule a leitura de tipos de consulta de um banco de dados ou arquivo
    tipos = [
        {"id": 1, "nome": "Consulta Básica", "duracao": "30 minutos", "preco": "100"},
        {"id": 2, "nome": "Consulta Avançada", "duracao": "60 minutos", "preco": "200"}
    ]
    return render_template('tipos_consulta.html', tipos=tipos)


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
