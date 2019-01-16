document.addEventListener('DOMContentLoaded', () => {

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, configure buttons
  socket.on('connect', () => {

    // a submot should emit a "create channel" event
    document.querySelectorAll('input').forEach(input => {
      input.onsubmit = () => {
        const channel_name = input.text;
        socket.emit('create channel', {'channel_name': channel_name});
      };
    });
  });

  // When a new channel is created, add to the unordered list
  socket.on('create channel', input.text => {
    const li = document.createElement('li');
    li.innerHTML = `Channel: ${input.text}`;
    document.querySelector('#channel_list').append(li);
  });
});
