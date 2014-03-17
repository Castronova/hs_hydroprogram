from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.db import models
from mezzanine.pages.models import Page, RichText
from mezzanine.core.models import Ownable
from hs_core.models import AbstractResource

#
# To create a new resource, use these three super-classes. 
#

class HydromodelResource(Page, RichText, AbstractResource):

    resource_description =  models.TextField(null=False,blank=True,default='My Text Field')
    resource_file = models.FileField(verbose_name='Model Archive',name='model_archive',upload_to='hs.hydromodel',storage=None,
                                     help_text='Upload Model Archive as *.ZIP')


    class Meta:
        verbose_name = 'HydroModel'


