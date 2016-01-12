var REQUEST_PERIOD = 600;

function getNewMessages(){
    $.get("get_next_message", function(data){
        if (data != ""){
            new_line = "<p>" + data + "</p>"
            var break_div = $("#break_messages");
            break_div.append(new_line);
            break_div[0].scrollTop = break_div[0].scrollHeight;
        }
    });
}

setInterval(getNewMessages, REQUEST_PERIOD);

$(document).ready(function (){
  getNewMessages();
});