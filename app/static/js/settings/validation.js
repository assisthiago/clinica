$(document).ready(() => {

    $('#unit').bind('change', (e) => enable_doctor_select(e));
    $('#confirm-password').bind('change paste keyup', (e) => compare_passwords(e));

    function enable_doctor_select(e) {
        const $input = $(`#${e.currentTarget.id}`);
        const option = $input.val().trim();

        if (option != '') {
            $('div#input-placeholder').addClass('d-none');
            $('div.unit-selects').addClass('d-none');

            const $target = $(`div#${option}`);
            $target.removeClass('d-none');
        }
        else {
            $('div#input-placeholder').removeClass('d-none');
            $('div.unit-selects').addClass('d-none');
        }
    };
});
