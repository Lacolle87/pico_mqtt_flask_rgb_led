$(function () {
    const speedInput = document.getElementById('speed');
    const reversedValue = parseInt(speedInput.max) + parseInt(speedInput.min) - parseInt(speedInput.value);
    speedInput.value = reversedValue;

    $('#rainbow_mode').change(function () {
        const rainbowMode = $(this).is(':checked');
        const mode = rainbowMode ? 'rainbow' : 'solid';
        $('#speed').prop('disabled', !rainbowMode);
        $('#red, #green, #blue').prop('disabled', rainbowMode);
        $.post('/', {'rainbow_mode': mode});
    });

    $('#led-form').submit(function (event) {
        event.preventDefault();
        var red = $('#red').val();
        var green = $('#green').val();
        var blue = $('#blue').val();
        var speed = $('#speed').val();
        var mode = $('#rainbow_mode').is(':checked') ? 'rainbow' : 'solid';
        var message = `rgb:${red},${green},${blue}`;
        if (mode === 'rainbow') {
            var rainbowEffect = $('#rainbow_effect').val();
            if (rainbowEffect === 'rainbow') {
                message = 'rainbow';
            } else if (rainbowEffect === 'cycle') {
                message = 'cycle';
            } else if (rainbowEffect === 'sync') {
                message = 'sync';
            }
            var reversedSpeed = parseInt(speedInput.max) + parseInt(speedInput.min) - parseInt(speed);
            message += `.${reversedSpeed}`;
        }
        $.post('/', {
            'color': message,
            'mode': mode
        });
    });
});
