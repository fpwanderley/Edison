var REQUEST_PERIOD = 600;
var TIMER_PERIOD = 1;
var status = 'IDLE';

function initialize_index(){
    status = 'IDLE';
    breakintervalID = setInterval(getNewMessageBreak, REQUEST_PERIOD);
    gearintervalID = setInterval(getNewMessageGear, REQUEST_PERIOD);
}

function getNewMessageBreak(){

    // Break Case.
    var user_case = 'break';
    var param = '?case=' + user_case;
    var url = "get_next_message" + param;
    $.get(url, function(data){
        if (data == 'finished'){
            clearInterval(breakintervalID);
            status = 'FINISHED';
            getReportData();
        }
        else if (data != ""){
            start_process();
            new_line = "<p>" + data + "</p>"
            var div_name = '#'+ user_case + '_messages';
            var break_div = $(div_name);
            break_div.append(new_line);
            break_div[0].scrollTop = break_div[0].scrollHeight;
        }
    });
}

function getNewMessageGear(){

    // Gear Case.
    var user_case = 'gear';
    var param = '?case=' + user_case;
    var url = "get_next_message" + param;
    $.get(url, function(data){
        if (data == 'finished'){
            clearInterval(gearintervalID);
            status = 'FINISHED';
        }
        else if (data != ""){
            start_process();
            new_line = "<p>" + data + "</p>"
            var div_name = '#'+ user_case + '_messages';
            var break_div = $(div_name);
            break_div.append(new_line);
            break_div[0].scrollTop = break_div[0].scrollHeight;
        }
    });
}

function increaseTimer(){
    timer_value = timer_value + 1;
    var new_time = timer_value;
    $('#time_counter')[0].innerHTML = (new_time/1000) + ' s';
}

function start_process(){
    if (status == 'IDLE'){
        status = 'ON_GOING';

        $('#path_information')[0].style.backgroundColor = 'green';

//        timer_value = 0;
//        timerintervalID = setInterval(increaseTimer, TIMER_PERIOD);
    }
}

function getReportData(){
    clearInterval(timerintervalID);
    $('#path_information')[0].style.backgroundColor = 'lightblue';
    console.log('Recuperando Report Data');
}
