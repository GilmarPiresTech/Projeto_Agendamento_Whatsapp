Resumo Completo do Projeto de Agendamento de Consultas
Visão Geral
Este projeto é uma aplicação web para agendamento de consultas, desenvolvida utilizando o framework Flask em Python para o backend, e HTML, CSS (com Tailwind CSS) e JavaScript no frontend. A aplicação permite que os usuários agendem consultas de diferentes tipos, com durações e valores variados, e que o administrador configure horários de trabalho, tipos de consulta e folgas.
________________________________________
Tecnologias Utilizadas
•	Backend:
o	Python com o framework Flask para criação das rotas e lógica de negócio.
o	openpyxl e pandas para manipulação de arquivos Excel onde os dados são armazenados.
•	Frontend:
o	HTML e CSS para estrutura e estilização das páginas.
o	Tailwind CSS para estilos e design responsivo.
o	JavaScript para interatividade e atualização dinâmica de conteúdo.
o	SweetAlert2 para exibição de mensagens de sucesso e erro ao usuário.
________________________________________
Estrutura do Projeto
Arquivos Principais
•	app.py: Arquivo principal da aplicação Flask, contendo todas as rotas e funções de backend.
•	Templates HTML:
o	form.html: Página principal onde os usuários podem agendar consultas.
o	calendario.html: Exibe o calendário com os agendamentos existentes.
o	config_horarios.html: Permite ao administrador configurar os horários de trabalho.
o	tipos_consulta.html: Permite ao administrador gerenciar os tipos de consulta.
o	marcar_folga.html: Permite ao administrador marcar folgas.
•	agendamentos.xlsx: Arquivo Excel onde todos os dados (agendamentos, configurações, tipos de consulta e folgas) são armazenados.
________________________________________
Funcionalidades Principais
Agendamento de Consultas
•	Seleção do Tipo de Consulta:
o	Os usuários podem selecionar entre diferentes tipos de consulta, cada um com sua própria duração e valor.
o	Os detalhes da consulta selecionada (duração e valor) são exibidos dinamicamente.
•	Atualização Dinâmica de Datas e Horários Disponíveis:
o	Após selecionar o tipo de consulta, o sistema atualiza as datas e horários disponíveis com base na duração da consulta e nos agendamentos existentes.
o	Apenas horários que não conflitam com agendamentos existentes são exibidos.
•	Formulário de Agendamento:
o	Os usuários preenchem seus dados pessoais (nome, email, celular) e podem adicionar um comentário adicional.
o	O formulário valida se todos os campos obrigatórios foram preenchidos.
•	Submissão do Agendamento:
o	Ao enviar o formulário, o sistema verifica novamente a disponibilidade do horário selecionado.
o	Se o horário estiver disponível, o agendamento é salvo no arquivo Excel e uma mensagem de sucesso é exibida.
o	Se o horário não estiver disponível, uma mensagem de erro é exibida.
Gestão de Agendamentos
•	Visualização do Calendário:
o	A rota /calendario permite visualizar todos os agendamentos existentes.
o	Os agendamentos são listados com detalhes como nome do cliente, data, horário e tipo de consulta.
•	Cancelamento de Agendamentos:
o	Os agendamentos podem ser cancelados, removendo-os do arquivo Excel.
Configuração do Sistema
•	Configuração de Horários de Trabalho:
o	A rota /config-horarios permite ao administrador definir os horários de início e fim de trabalho para cada dia da semana.
o	É possível marcar determinados dias da semana como folga.
•	Gestão de Tipos de Consulta:
o	A rota /tipos-consulta permite adicionar, editar e excluir tipos de consulta.
o	Cada tipo de consulta tem um nome, duração (em minutos) e valor.
•	Marcação de Folgas:
o	A rota /marcar-folga permite marcar dias específicos como folga.
o	Os dias marcados como folga não estarão disponíveis para agendamento.
________________________________________
Detalhes Técnicos Importantes
Manipulação de Dados com Excel
•	Leitura e Escrita:
o	Os dados são armazenados no arquivo agendamentos.xlsx, dividido em diferentes abas:
	Agendamentos: Contém todos os agendamentos realizados.
	Configurações: Armazena os horários de trabalho para cada dia da semana.
	Folgas: Lista de datas marcadas como folga.
	TiposConsulta: Contém os tipos de consulta disponíveis.
o	As bibliotecas openpyxl e pandas são utilizadas para manipular o arquivo Excel.
•	Verificação e Criação do Arquivo Excel:
o	A função verificar_ou_criar_excel() assegura que o arquivo Excel e todas as abas necessárias existam, criando-os se necessário.
Lógica de Agendamento e Verificação de Disponibilidade
•	Cálculo de Horários Disponíveis:
o	A função gerar_dias_disponiveis() calcula os horários disponíveis para agendamento, considerando:
	Os horários de trabalho configurados.
	As folgas marcadas.
	Os agendamentos já existentes.
	A duração da consulta selecionada.
o	Os horários são gerados em intervalos de 15 minutos, mas apenas são considerados disponíveis se não houver sobreposição com agendamentos existentes.
•	Verificação de Conflitos de Horário:
o	As funções verificar_horario_disponivel() e verificar_disponibilidade() verificam se o horário desejado está disponível, considerando a duração da consulta e possíveis conflitos com agendamentos existentes.
•	Normalização de Dados:
o	Para evitar problemas de comparação, os nomes dos tipos de consulta são normalizados (removendo espaços extras e ignorando maiúsculas/minúsculas).
Comunicação entre Frontend e Backend
•	Atualização Dinâmica via AJAX:
o	O frontend utiliza fetch para enviar requisições AJAX ao backend, obtendo os horários disponíveis após a seleção do tipo de consulta.
o	Os dados são enviados e recebidos no formato JSON.
•	Renderização Dinâmica no Frontend:
o	O JavaScript é utilizado para renderizar dinamicamente os botões de datas e horários disponíveis.
o	Eventos são adicionados aos botões para que, ao serem clicados, atualizem os campos escondidos que serão submetidos no formulário.
________________________________________
Fluxo de Uso da Aplicação
1.	Usuário acessa a página de agendamento.
2.	Seleciona o tipo de consulta desejado.
o	Os detalhes da consulta (duração e valor) são exibidos.
o	As datas e horários disponíveis são atualizados dinamicamente.
3.	Escolhe uma data e um horário disponível.
4.	Preenche os dados pessoais e comentário adicional.
5.	Submete o formulário de agendamento.
o	O sistema verifica novamente a disponibilidade do horário.
o	Se disponível, o agendamento é salvo e uma mensagem de sucesso é exibida.
6.	Usuário recebe confirmação do agendamento.
o	O sistema envia um email ao cliente confirmando o agendamento 
