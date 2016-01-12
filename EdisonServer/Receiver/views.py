from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader, RequestContext

from Utils.Utils import LogManager

START = 'start'

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

        except:
            pass

# Create your views here.
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

    if not case in POSSIBLE_CASES:
        case = 'break'

    log_manager = LogManager()
    message = log_manager.read_first_line_and_erase(case=case)
    if message:
        return HttpResponse(message)
    else:
        return HttpResponse('')
