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

    # This will save the file in ./static/media/hs/hydromodel
    hm_zip = models.FileField(verbose_name='Model Archive',name='modelzip',upload_to='./hs/hydromodel',
                                    help_text='Upload Model Archive as *.ZIP')


    hm_description =  models.TextField(verbose_name='Description', null=False,blank=True,default='',
                                             help_text='Add a short description of the model simulation')

    hm_version = models.CharField(verbose_name='Version',null=False,blank=True,default='1.0',
                                          help_text='Specify the simulation version to distinguish between similar model simulations')

    hm_type = models.CharField(verbose_name='Type', default='Instance',
                            help_text='Specify the type of HydroModel (e.g. Model Instance, Model Program, etc...')
    # if instance, choose parent model or create parent model


    #######################
    # TEMPORAL DEFINITION #
    #######################
    # Only for Instance Types
    hm_begin = models.DateTimeField(verbose_name='Simulation Begin',
                                 help_text='The start date of the model simulation (mm/dd/yyyy hh:mm)')
    hm_end  = models.DateTimeField(verbose_name='Simulation End',
                                help_text='The end date of the model simulation (mm/dd/yyyy hh:mm)')
    hm_timestep = models.FloatField(verbose_name='Simulation Time Interval',
                                 help_text='The timestep interval that is used for calculations (in seconds)')




    class Meta:
        verbose_name = 'HydroModel'


