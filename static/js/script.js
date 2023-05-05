$(function () {
  const speedInput = document.getElementById('speed');
  const reversedValue = parseInt(speedInput.max) + parseInt(speedInput.min) - parseInt(speedInput.value);
  speedInput.value = reversedValue;

  $('#rainbow_mode').change(function () {
    const isRainbow = $(this).is(':checked');
    $('#speed').prop('disabled', !isRainbow);
    $('#red, #green, #blue').prop('disabled', isRainbow);
    $.post('/', {'rainbow_mode': isRainbow});
  });

  $('#led-form').submit(function (event) {
    event.preventDefault();
    const red = $('#red').val();
    const green = $('#green').val();
    const blue = $('#blue').val();
    const speed = $('#speed').val();
    const isRainbow = $('#rainbow_mode').is(':checked');
    let message;
    if (isRainbow) {
      const rainbowEffect = $('#rainbow_effect').val();
      if (rainbowEffect === 'rainbow') {
        message = 'rainbow';
      } else if (rainbowEffect === 'cycle') {
        message = 'cycle';
      } else if (rainbowEffect === 'sync') {
        message = 'sync';
      }
      const reversedSpeed = parseInt(speedInput.max) + parseInt(speedInput.min) - parseInt(speed);
      message += `.${reversedSpeed}`;
    } else {
      message = `rgb:${red},${green},${blue}`;
    }
    $.post('/', {
      'color': message,
      'mode': isRainbow
    });
  });
});
