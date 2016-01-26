var REQUEST_PERIOD = 600;
var TIMER_PERIOD = 1;
var status = 'IDLE';
breakintervalID = 0;
gearintervalID = 0;
iaDataID = 0;

var TOTAL_CHARTS = 2;
var showed_charts = 0;

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
        if(data != ''){
            var json_data = JSON.parse(data);
            var type = json_data.type;
            var new_data = json_data.data;

            if (type == 'chat_data'){
                start_process();
                new_line = "<p>" + new_data + "</p>"
                var div_name = '#'+ user_case + '_messages';
                var break_div = $(div_name);
                break_div.append(new_line);
                break_div[0].scrollTop = break_div[0].scrollHeight;
            }
            else if(type == 'chart_data'){
                clearInterval(breakintervalID);
                showed_charts = showed_charts + 1;
                getReportData(user_case, new_data);

                check_for_ia_data();

            }
            else if(type == 'ia_data'){
                $("#ia_class_value").attr('data-value', new_data);
            }
        }
    });
}

function getNewMessageGear(){

    // Gear Case.
    var user_case = 'gear';
    var param = '?case=' + user_case;

    var url = "get_next_message" + param;
    $.get(url, function(data){
        if(data != ''){
            var json_data = JSON.parse(data);
            var type = json_data.type;
            var new_data = json_data.data;

            if (type == 'chat_data'){
                start_process();
                new_line = "<p>" + new_data + "</p>"
                var div_name = '#'+ user_case + '_messages';
                var break_div = $(div_name);
                break_div.append(new_line);
                break_div[0].scrollTop = break_div[0].scrollHeight;
            }
            else if(type == 'chart_data'){
                clearInterval(gearintervalID);
                showed_charts = showed_charts + 1;
                getReportData(user_case, new_data);

                check_for_ia_data();
            }
        }
    });
}

function increaseTimer(){
    timer_value = timer_value + 1;
    var new_time = timer_value;
    $('#time_counter')[0].innerHTML = (new_time/1000) + ' s';
}

function start_process(){
    $('#path_information')[0].style.backgroundColor = 'green';
}

function getReportData(user_case, chart_data){
    // clearInterval(timerintervalID);
    $('#path_information')[0].style.backgroundColor = 'lightblue';

    // Removendo a listagem de mensagens.
    if (user_case == 'break'){
        var message_div = $('#break_messages');
        message_div.addClass('display-none');
        var message_title = $('#break_title');
        message_title.addClass('display-none');
        initialize_chart('Break Analysis', chart_data, 'break_chart_container');
    }
    else if (user_case == 'gear'){
        var message_div = $('#gear_messages');
        message_div.addClass('display-none');
        var message_title = $('#gear_title');
        message_title.addClass('display-none');
        initialize_chart('Gear Analysis', chart_data, 'gear_chart_container');
    }
}

function initialize_chart(chart_name, data, container_id){
    var container = $('#'+container_id);
    var series_data = data;

    container.highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: chart_name,
            margin: 1
        },
        tooltip: {
            pointFormat: '<b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },
        series: [{
            type: 'pie',
            name: chart_name,

            colors: ['#66FF66','#FFFF66','#A00000'], // Usar Verde, Amarelo, Vermelho sempre.
            data: series_data
        }]
    });

    container.removeClass('display-none');
}

function openStarDiv(driver_class){
    $("#ia_div").show();

//  Desabilita edição.
    $("#ia_stars")[0].disabled=true;
//  Seta o valor correto para as estrelas.

    if (driver_class == 1.0){
        var star = 'star5';
    }
    else if (driver_class == 2.0){
        var star = 'star4';
    }
    else if (driver_class == 3.0){
        var star = 'star3';
    }
    else if (driver_class == 4.0){
        var star = 'star2';
    }
    else if (driver_class == 5.0){
        var star = 'star1';
    }
    else{
        var star = 'star1';
    }
    $("#"+star)[0].checked=true;
}

function check_for_ia_data(ia_class){
    // Deve buscar pela informação de IA.
    if (showed_charts == TOTAL_CHARTS){

        var ia_class = $('#ia_class_value').attr('data-value');

        if (ia_class != ''){
            clearInterval(iaDataID);
            openStarDiv(parseInt(ia_class));
        }
        else{
            getNewMessageBreak();
            clearInterval(iaDataID);
            iaDataID = setInterval(check_for_ia_data, 4*REQUEST_PERIOD);
        }
    }
}