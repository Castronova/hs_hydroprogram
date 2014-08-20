from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from hs_core import hydroshare
from django import forms
from .models import HydroProgramResource
from django.utils.timezone import now
from ga_resources.utils import json_or_jsonp
import json
import os
from django.conf import settings


class DetailView(generic.DetailView):
    model = HydroProgramResource
    #template_name = 'hydromodel/detail.html'
    template_name = 'hs_hydroprogram/detail.html'





class CreateHydroProgramForm(forms.Form):
    title = forms.CharField(required=True)
    creators = forms.CharField(required=False, min_length=0)
    contributors = forms.CharField(required=False, min_length=0)
    abstract = forms.CharField(required=False, min_length=0)
    keywords = forms.CharField(required=False, min_length=0)
    rest_url = forms.URLField(required=False)
    wsdl_url = forms.URLField(required=False)
    reference_type = forms.CharField(required=False, min_length=0)
    site = forms.CharField(required=False, min_length=0)
    variable = forms.CharField(required=False, min_length=0)


@login_required
def create_hydro_program(request, *args, **kwargs):


    eula = json.loads('../static/resources/eula.json')
    print eula

#    return render(request, 'template.html', {"mydata": mydata},
#        content_type="application/xhtml+xml")

    frm = CreateHydroProgramForm(request.POST)
    if frm.is_valid():
        dcterms = [
            { 'term': 'T', 'content': frm.cleaned_data['title']},
            { 'term': 'AB', 'content': frm.cleaned_data['abstract'] or frm.cleaned_data['title']},
            { 'term': 'DTS', 'content': now().isoformat()}
        ]
        for cn in frm.cleaned_data['contributors'].split(','):
            cn = cn.strip()
            dcterms.append({'term' : 'CN', 'content' : cn})
        for cr in frm.cleaned_data['creators'].split(','):
            cr = cr.strip()
            dcterms.append({'term' : 'CR', 'content' : cr})

        if frm.cleaned_data['wsdl_url']:
            url = frm.cleaned_data['wsdl_url']
        elif frm.cleaned_data['rest_url']:
            url = frm.cleaned_data['rest_url']
        else:
            url = ''

        res = hydroshare.create_resource(
            resource_type='HydroProgramResource',
            owner=request.user,
            title=frm.cleaned_data['title'],
            keywords=[k.strip() for k in frm.cleaned_data['keywords'].split(',')] if frm.cleaned_data['keywords'] else None,
            dublin_metadata=dcterms,
            content=frm.cleaned_data['abstract'] or frm.cleaned_data['title'],
            reference_type=frm.cleaned_data['reference_type'],
            url=url,
            data_site=frm.cleaned_data.get('site', ''),
            variable=frm.cleaned_data.get('variable', ''),
            eula = eula
        )
        return HttpResponseRedirect(res.get_absolute_url())


class GetTSValuesForm(forms.Form):
    # name = forms.CharField(min_length=0, required=True)
    # type = forms.CharField(min_length=0, required=True)
    size = forms.CharField(min_length=0, required=True)
    # content = forms.CharField(min_length=0, required=False)

def parse_metadata(request):

    name = request.POST.get('name','NONE')
    type = request.POST.get('type','NONE')
    size = request.POST.get('size','NONE')
    #if f.is_valid():


    data = {'name':name,
            'type':type,
            'size':size}

    return json_response(True,data)




def get_eula(request):

    print 'IN: get_eula(request)'

    name = request.GET.get('name','NONE')
    print name
    response = {'eula':'Could not find a EULA for: '+name}

    formatted_name = name.lower().replace(' ','')

    try:
        path = os.path.join(settings.STATIC_ROOT, 'resources/eulas.json')
        txt = open(path,'r').readlines()[0]
        #print txt

        # todo: move th is to view load, so that it isn't constantly repeated
        # load the eula dictionary
        print 'parsing json'
        #print json.loads('[{"noun": "hello", "Hola": "Hello", "Hoi": "Hello"}]')
        #print json.loads(txt)

        eula_dict = json.loads(txt)
        print 'done'
        print eula_dict.keys()

        print formatted_name in eula_dict
        print formatted_name in eula_dict.keys()

        #print eula_dict.values()


        # set the response
        if formatted_name in eula_dict:
            response['eula'] = eula_dict[formatted_name]
        else:
            print formatted_name, 'not in dictionary!'

    except Exception, e:
        print e

    return json_response(True,response)



def json_response(result, data):
    response = json.dumps({"result" : result, "data" : data })
    return HttpResponse(response, mimetype="application/json")

def my_view(request):
    json_response(True, 'Right away Michael')