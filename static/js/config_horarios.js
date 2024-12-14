// Exibindo mensagens flash com SweetAlert2
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
    {% for category, message in messages %}
        Swal.fire({
            icon: '{{ "success" if category == "success" else "error" }}',
            title: '{{ message }}',
            showConfirmButton: false,
            timer: 3000 // Duração do popup em milissegundos
        });
    {% endfor %}
{% endif %}
{% endwith %}
