Resumo Completo do Projeto de Agendamento de Consultas
Este projeto � uma aplica��o web para agendamento de consultas, desenvolvida utilizando o framework Flask em Python para o backend, e HTML, CSS (com Tailwind CSS) e JavaScript no frontend. A aplica��o permite que os usu�rios agendem consultas de diferentes tipos, com dura��es e valores variados, e que o administrador configure hor�rios de trabalho, tipos de consulta e folgas.
________________________________________
Tecnologias Utilizadas
� � Backend:
o � Python com o framework Flask para cria��o das rotas e l�gica de neg�cio.
o � openpyxl e pandas para manipula��o de arquivos Excel onde os dados s�o armazenados.
� � Frontend:
o � HTML e CSS para estrutura e estiliza��o das p�ginas.
o � Tailwind CSS para estilos e design responsivo.
o � JavaScript para interatividade e atualiza��o din�mica de conte�do.
o � SweetAlert2 para exibi��o de mensagens de sucesso e erro ao usu�rio.
________________________________________
Estrutura do Projeto
Arquivos Principais
� � app.py: Arquivo principal da aplica��o Flask, contendo todas as rotas e fun��es de backend.
� � Templates HTML:
o � form.html: P�gina principal onde os usu�rios podem agendar consultas.
o � calendario.html: Exibe o calend�rio com os agendamentos existentes.
o � config_horarios.html: Permite ao administrador configurar os hor�rios de trabalho.
o � tipos_consulta.html: Permite ao administrador gerenciar os tipos de consulta.
o � marcar_folga.html: Permite ao administrador marcar folgas.
� � agendamentos.xlsx: Arquivo Excel onde todos os dados (agendamentos, configura��es, tipos de consulta e folgas) s�o armazenados.
________________________________________
Funcionalidades Principais
Agendamento de Consultas
� � Sele��o do Tipo de Consulta:
o � Os usu�rios podem selecionar entre diferentes tipos de consulta, cada um com sua pr�pria dura��o e valor.
o � Os detalhes da consulta selecionada (dura��o e valor) s�o exibidos dinamicamente.
� � Atualiza��o Din�mica de Datas e Hor�rios Dispon�veis:
o � Ap�s selecionar o tipo de consulta, o sistema atualiza as datas e hor�rios dispon�veis com base na dura��o da consulta e nos agendamentos existentes.
o � Apenas hor�rios que n�o conflitam com agendamentos existentes s�o exibidos.
� � Formul�rio de Agendamento:
o � Os usu�rios preenchem seus dados pessoais (nome, email, celular) e podem adicionar um coment�rio adicional.
o � O formul�rio valida se todos os campos obrigat�rios foram preenchidos.
� � Submiss�o do Agendamento:
o � Ao enviar o formul�rio, o sistema verifica novamente a disponibilidade do hor�rio selecionado.
o � Se o hor�rio estiver dispon�vel, o agendamento � salvo no arquivo Excel e uma mensagem de sucesso � exibida.
o � Se o hor�rio n�o estiver dispon�vel, uma mensagem de erro � exibida.
Gest�o de Agendamentos
� � Visualiza��o do Calend�rio:
o � A rota /calendario permite visualizar todos os agendamentos existentes.
o � Os agendamentos s�o listados com detalhes como nome do cliente, data, hor�rio e tipo de consulta.
� � Cancelamento de Agendamentos:
o � Os agendamentos podem ser cancelados, removendo-os do arquivo Excel.
Configura��o do Sistema
� � Configura��o de Hor�rios de Trabalho:
o � A rota /config-horarios permite ao administrador definir os hor�rios de in�cio e fim de trabalho para cada dia da semana.
o � � poss�vel marcar determinados dias da semana como folga.
� � Gest�o de Tipos de Consulta:
o � A rota /tipos-consulta permite adicionar, editar e excluir tipos de consulta.
o � Cada tipo de consulta tem um nome, dura��o (em minutos) e valor.
� � Marca��o de Folgas:
o � A rota /marcar-folga permite marcar dias espec�ficos como folga.
o � Os dias marcados como folga n�o estar�o dispon�veis para agendamento.
________________________________________
Detalhes T�cnicos Importantes
Manipula��o de Dados com Excel
� � Leitura e Escrita:
o � Os dados s�o armazenados no arquivo agendamentos.xlsx, dividido em diferentes abas:
? � Agendamentos: Cont�m todos os agendamentos realizados.
? � Configura��es: Armazena os hor�rios de trabalho para cada dia da semana.
? � Folgas: Lista de datas marcadas como folga.
? � TiposConsulta: Cont�m os tipos de consulta dispon�veis.
o � As bibliotecas openpyxl e pandas s�o utilizadas para manipular o arquivo Excel.
� � Verifica��o e Cria��o do Arquivo Excel:
o � A fun��o verificar_ou_criar_excel() assegura que o arquivo Excel e todas as abas necess�rias existam, criando-os se necess�rio.
L�gica de Agendamento e Verifica��o de Disponibilidade
� � C�lculo de Hor�rios Dispon�veis:
o � A fun��o gerar_dias_disponiveis() calcula os hor�rios dispon�veis para agendamento, considerando:
? � Os hor�rios de trabalho configurados.
? � As folgas marcadas.
? � Os agendamentos j� existentes.
? � A dura��o da consulta selecionada.
o � Os hor�rios s�o gerados em intervalos de 15 minutos, mas apenas s�o considerados dispon�veis se n�o houver sobreposi��o com agendamentos existentes.
� � Verifica��o de Conflitos de Hor�rio:
o � As fun��es verificar_horario_disponivel() e verificar_disponibilidade() verificam se o hor�rio desejado est� dispon�vel, considerando a dura��o da consulta e poss�veis conflitos com agendamentos existentes.
� � Normaliza��o de Dados:
o � Para evitar problemas de compara��o, os nomes dos tipos de consulta s�o normalizados (removendo espa�os extras e ignorando mai�sculas/min�sculas).
Comunica��o entre Frontend e Backend
� � Atualiza��o Din�mica via AJAX:
o � O frontend utiliza fetch para enviar requisi��es AJAX ao backend, obtendo os hor�rios dispon�veis ap�s a sele��o do tipo de consulta.
o � Os dados s�o enviados e recebidos no formato JSON.
� � Renderiza��o Din�mica no Frontend:
o � O JavaScript � utilizado para renderizar dinamicamente os bot�es de datas e hor�rios dispon�veis.
o � Eventos s�o adicionados aos bot�es para que, ao serem clicados, atualizem os campos escondidos que ser�o submetidos no formul�rio.
________________________________________
Fluxo de Uso da Aplica��o
1. �Usu�rio acessa a p�gina de agendamento.
2. �Seleciona o tipo de consulta desejado.
o � Os detalhes da consulta (dura��o e valor) s�o exibidos.
o � As datas e hor�rios dispon�veis s�o atualizados dinamicamente.
3. �Escolhe uma data e um hor�rio dispon�vel.
4. �Preenche os dados pessoais e coment�rio adicional.
5. �Submete o formul�rio de agendamento.
o � O sistema verifica novamente a disponibilidade do hor�rio.
o � Se dispon�vel, o agendamento � salvo e uma mensagem de sucesso � exibida.
6. �Usu�rio recebe confirma��o do agendamento.
o � O sistema envia um email ao cliente confirmando o agendamento 


