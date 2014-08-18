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
            variable=frm.cleaned_data.get('variable', '')
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

    #return json_or_jsonp(request, ts)

        # params = f.cleaned_data
        # ref_type = params['ref_type']
        # url = params['service_url']
        # site = params.get('site')
        # variable = params.get('variable')
        # if ref_type == 'rest':
        #     ts = ts_utils.time_series_from_service(url, ref_type)
        # else:
        #     ts = ts_utils.time_series_from_service(url, ref_type, site_name_or_code=site, variable_code=variable)
        # return json_or_jsonp(request, ts)


import json

def json_response(result, data):
    response = json.dumps({"result" : result, "data" : data })
    return HttpResponse(response, mimetype="application/json")

def my_view(request):
    json_response(True, 'Right away Michael')