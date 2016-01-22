from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext

from Utils.Utils import LogManager

START = 'start'
FINISH_COMMAND = 'finish'

POSSIBLE_CASES = ['gear', 'break']

def index(request):

    context = RequestContext(request, {
        'teste': 'teste',
    })

    return render(request, 'index.html', context)

# Create your views here.
@csrf_exempt
def control(request):
    if request.method == 'POST':
        try:
            command = request.POST['command']

            if command == START:
                log_manager = LogManager()
                log_manager.create_logs()
                return HttpResponse('Percurso Iniciado com Sucesso.')

            elif command == FINISH_COMMAND:
                log_manager = LogManager()
                log_manager.finish_logs()
                return HttpResponse('Percurso Finalizado com sucesso.')

        except:
            pass

# Create your views here.
# http://127.0.0.1:8000/receiver/receive_message_data
@csrf_exempt
def receive_message_data(request):
    if request.method == 'POST':
        try:
            message = request.POST['message']
            case = request.POST['case']

            log_manager = LogManager()
            log_manager.append_to_all_logs(message, case=case)

            return HttpResponse(message)
        except:
            pass

def get_next_message(request):

    case = request.GET['case']
    report = request.GET.get('report', False)

    if not case in POSSIBLE_CASES:
        case = 'break'

    log_manager = LogManager()
    if report:
        message = log_manager.read_first_line(case=case)
    else:
        message = log_manager.read_first_line_and_erase(case=case)

    if message:
        return HttpResponse(message.replace("'", '"'))
    else:
        return HttpResponse('')
