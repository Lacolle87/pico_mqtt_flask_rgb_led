$(function() {
  // Reverse the values of the speed range slider when the page loads
  var speedInput = document.getElementById('speed');
  var reversedValue = parseInt(speedInput.max) + parseInt(speedInput.min) - parseInt(speedInput.value);
  speedInput.setAttribute('value', reversedValue);

  $('#rainbow_mode').change(function() {
    var rainbowMode = $(this).is(':checked');
    if (rainbowMode) {
      $('#speed').prop('disabled', false);
      $('#red, #green, #blue').prop('disabled', true);
      $.post('/', {
        'rainbow_mode': 'rainbow'
      });
    } else {
      $('#speed').prop('disabled', true);
      $('#red, #green, #blue').prop('disabled', false);
      $.post('/', {
        'rainbow_mode': 'solid'
      });
    }
  });

  $('#led-form').submit(function(event) {
    event.preventDefault();
    var red = $('#red').val();
    var green = $('#green').val();
    var blue = $('#blue').val();
    var speed = $('#speed').val();
    var mode = $('#rainbow_mode').is(':checked') ? 'rainbow' : 'solid';
    var message = `rgb:${red},${green},${blue}`;
    if (mode === 'rainbow') {
      // Reverse the speed value before appending it to the message
      var reversedSpeed = parseInt(speedInput.max) + parseInt(speedInput.min) - parseInt(speed);
      message += `:rainbow.${reversedSpeed}`;
    }
    $.post('/', {
      'color': message,
      'mode': mode
    });
  });
});
