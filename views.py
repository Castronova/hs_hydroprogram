from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import HydromodelResource

class DetailView(generic.DetailView):
    model = HydromodelResource
    template_name = 'hydromodel/detail.html'
