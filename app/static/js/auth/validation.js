$(document).ready(() => {

    $('#password').bind('change paste keyup', (e) => less_than_8_char(e));
    $('#confirm-password').bind('change paste keyup', (e) => compare_passwords(e));

    function less_than_8_char(e) {
        const $input = $(`#${e.currentTarget.id}`);
        if ($input.val().trim().length >= 8)
            $input.removeClass('is-invalid').addClass('is-valid');
        else
            $input.removeClass('is-valid').addClass('is-invalid');
    };

    function compare_passwords(e) {
        const $input = $(`#${e.currentTarget.id}`);
        const input_value = $input.val().trim();
        const password_value = $('#password').val().trim();

        if (!input_value || (input_value != password_value))
            $input.removeClass('is-valid').addClass('is-invalid');
        else
            $input.removeClass('is-invalid').addClass('is-valid');
    };

});
