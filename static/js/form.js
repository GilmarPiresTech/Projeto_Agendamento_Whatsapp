function atualizarDetalhesConsulta() {
    const select = document.getElementById('tipo_consulta');
    const selectedOption = select.options[select.selectedIndex];
    const duracao = parseInt(selectedOption.getAttribute('data-duracao'));
    const valor = selectedOption.getAttribute('data-valor');

    document.getElementById('duracao').value = duracao + ' minutos';
    document.getElementById('valor').value = 'R$ ' + parseFloat(valor).toFixed(2);
    document.getElementById('detalhes-consulta').classList.remove('hidden');
    renderAvailableDatesAndTimes(duracao);
}

function renderAvailableDatesAndTimes(duracaoConsulta) {
    const availableDates = {{ dias_disponiveis.keys() | list | tojson }};
    const availableTimes = {{ dias_disponiveis | tojson }};
    const dateSelection = document.getElementById('date-selection');
    const timeSelection = document.getElementById('time-selection');
    dateSelection.innerHTML = '';
    timeSelection.innerHTML = '';

    availableDates.forEach(date => {
        const dateButton = document.createElement('button');
        dateButton.textContent = new Date(date).toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'short' });
        dateButton.classList.add('date-button');

        dateButton.onclick = function () {
            document.querySelectorAll('.date-button').forEach(btn => btn.classList.remove('active'));
            dateButton.classList.add('active');
            document.getElementById('selected_date').value = date;
            renderTimes(date, duracaoConsulta);
        };
        dateSelection.appendChild(dateButton);
    });
}

function renderTimes(selectedDate, duracaoConsulta) {
    const timeSelection = document.getElementById('time-selection');
    timeSelection.innerHTML = '';
    const availableTimes = {{ dias_disponiveis | tojson }};
    (availableTimes[selectedDate] || []).forEach(time => {
        const timeButton = document.createElement('button');
        timeButton.textContent = time;
        timeButton.classList.add('time-button');

        timeButton.onclick = function () {
            document.querySelectorAll('.time-button').forEach(btn => btn.classList.remove('active'));
            timeButton.classList.add('active');
            document.getElementById('selected_time').value = time;
        };
        timeSelection.appendChild(timeButton);
    });
}
