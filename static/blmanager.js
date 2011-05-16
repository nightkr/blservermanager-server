$(function(){
	server_status_change("not connected");

	socket = new io.Socket(window.location.hostname, {resource: "blmanager", rememberTransport: false, port: 8000});
	socket.on('connect', function(message){
		socket.send("key:" + key);
	});
	socket.on('message', function(message){
		var messageParts = explode(":", message, 2);
		switch(messageParts[0]) {
			case "console_line":
				new_console_line(messageParts[1]);
				break;
			case "server_status":
				server_status_change(messageParts[1]);
				break;
		}
	});
	socket.on('disconnect', function(message){
		server_status_change("not connected");
	});
	socket.connect();

	$("#consoleInput").keydown(function(event){
		if (event.keyCode == 13) {
			event.preventDefault();
			eval_console_line();
		}
	});

	$("#startButton").click(function() {
		socket.send("start_server");
	});
	$("#stopButton").click(function() {
		socket.send("stop_server");
	});

	$(window).unload(function() {
		socket.close();
	});
});

function server_status_change(newStatus) {
	$("#serverStatus").html(newStatus);
	$("#consoleInput").attr("readonly", newStatus != "online");
	$("#startButton").attr("disabled", newStatus != "offline");
	$("#stopButton").attr("disabled", newStatus != "online");
}

function new_console_line(line) {
	$("#console").html($("#console").html() + line + "\n");
	$("#console").scrollTop($("#console").attr("scrollHeight") - $("#console").height());
}
function eval_console_line() {
	var line = $("#consoleInput").val();
	new_console_line(line);
	socket.send("eval:" + line);
	$("#consoleInput").val("");
}
