$(document).ready(() => {

    $('#unit').bind('change', (e) => enable_doctor_select(e));
    $('#confirm-password').bind('change paste keyup', (e) => compare_passwords(e));

    function enable_doctor_select(e) {
        const option = $(`#${e.currentTarget.id} option:selected`).data('target');
        if (option) {
            $('div#input-placeholder').addClass('d-none');
            $('div.unit-selects').addClass('d-none');

            $('select.doctor').attr('required', false);
            $(`select#${option}`).attr('required', true);
            $(`div#${option}`).removeClass('d-none');
            return;
        }
        $('div#input-placeholder').removeClass('d-none');
        $('div.unit-selects').addClass('d-none');
    };
});
