from django.template import Context, loader
from polls.models import Poll
from django.http import HttpResponse

_choices = {}

def index(request):
    '''Try building the list of HTML widgets here to allow the template to populate from the Context...'''
    latest_poll_list = Poll.objects.all().order_by('pub_date')[:5]
    t = loader.get_template('polls/index.html')
    polls = []
    for item in latest_poll_list:
        p = Poll.objects.get(pk=item.id)
        p.num = len(polls)+1
        p.is_radio_set = len(p.choice_set.all())>0
        for choice in p.choice_set.all():
            _choices[choice.choice] = choice.choice.find('(please specify)') == -1
        p.is_choice_radio = lambda s:s.find('(please specify)') == -1
        polls.append(p)
    c = Context({
        'latest_poll_list': polls,
        'd_choices':_choices
    })
    return HttpResponse(t.render(c))
