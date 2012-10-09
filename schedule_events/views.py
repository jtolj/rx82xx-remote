from django.conf import settings
from django.core import serializers
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponseRedirect,HttpResponse
from schedule_events.models import Schedule_event
from datetime import datetime, timedelta
from django.contrib import messages
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

def index(request):
    schedule_events = Schedule_event.objects.exclude(status=3).filter(datetime__gte=datetime.now() - timedelta(minutes=15)).order_by("datetime")
    receivers = settings.RECEIVERS.keys()
    schedules = settings.SCHEDULES.keys()
    return render_to_response('app/index.html', {'receivers' : sorted(receivers), 'schedules': sorted(schedules), 'events': schedule_events}, context_instance=RequestContext(request))

#returns tuple of polarity, frequency, symbol rate, mpeg service
def _get_status(ip):
    #get polarity
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,2,2,1,0))
    )
    polarity = varBinds[0][1]
    
    input = int(polarity + 1)
    
    #get frequency
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,2,2,15,1,3,input))
    )
    
    frequency = varBinds[0][1]
    
    #get symbol rate
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,2,2,15,1,4,input))
    )
    
    symbol_rate = varBinds[0][1]
    
    #get mpeg service number
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,4,1,2,0))
    )
    
    mpeg_service = varBinds[0][1]
    
    return (polarity, frequency, symbol_rate, mpeg_service)

def status(request):
    status = {}
    for receiver, ip in settings.RECEIVERS.iteritems():
        data = _get_status(ip)
        status[receiver] = [k for k, v in settings.SCHEDULES.iteritems() if v == data]
    return HttpResponse(simplejson.dumps(status), mimetype='application/json')

def events(request):
    schedule_events = serializers.serialize("json", Schedule_event.objects.all().order_by("datetime"))
    return HttpResponse(schedule_events, mimetype='application/json')

def add(request):
    post = request.POST
    if (len(post['datetime']) and len(post['receiver']) and len(post['schedule'])) :
        if (datetime.strptime(post['datetime'], '%m/%d/%Y %H:%M:%S') < datetime.now()):
            messages.error(request, 'Date/Time must be in the future')
        else :
            event = Schedule_event()
            event.datetime = datetime.strptime(post['datetime'], '%m/%d/%Y %H:%M:%S')
            event.receiver = post['receiver']
            event.schedule = post['schedule']
            event.save()
            messages.success(request, 'New event saved.')
    else :
        messages.error(request, 'All fields are required.')
    return HttpResponseRedirect('/')
    
def edit(request, event_id):
    event = get_object_or_404(Schedule_event, pk=event_id)
    post = request.POST
    if (len(post['datetime']) and len(post['receiver']) and len(post['schedule'])) :
        event.datetime = datetime.strptime(post['datetime'], '%m/%d/%Y %H:%M:%S')
        event.receiver = post['receiver']
        event.schedule = post['schedule']
        event.status = 2 #mark as changed so dispatcher requeues job
        event.save()
        messages.success(request, 'Event has been updated.')
        return HttpResponseRedirect('/')
    else:
        messages.error(request, 'All fields are required.')
        return HttpResponseRedirect('/')
    
def delete(request, event_id):
    event = get_object_or_404(Schedule_event, pk=event_id)
    event.status = 3
    event.save()
    messages.success(request, 'Event has been deleted.')
    return HttpResponseRedirect('/')