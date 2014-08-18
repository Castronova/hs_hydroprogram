from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.db import models
from mezzanine.pages.models import Page, RichText
from mezzanine.core.models import Ownable
from hs_core.models import AbstractResource
import datetime as dt


#
# To create a new resource, use these three super-classes. 
#

class HydroProgramResource(Page, RichText, AbstractResource):

    # This will save the file in ./static/media/hs/hydromodel
    hm_zip = models.FileField(verbose_name='Model Archive',name='modelzip',upload_to='./hs/hydromodel',
                                     help_text='Upload Model Archive as *.ZIP')


    hm_description =  models.TextField(verbose_name='Description', null=False,blank=True,default='',
                                              help_text='Add a short description of the model simulation')

    hm_version = models.CharField(verbose_name='Version',null=False,blank=True,default='1.0',max_length=255,
                                          help_text='Specify the simulation version to distinguish between similar model simulations')

    hm_type = models.CharField(verbose_name='Type', default='Instance',max_length=255,
                            help_text='Specify the type of HydroModel (e.g. Model Instance, Model Program, etc...')
    # if instance, choose parent model or create parent model


    # ###########
    # # Program #
    # #---------#
    # # 1 .. 1  #
    # ###########
    #
    # # title
    # title = models.TextField(verbose_name='Program Title', null=False, blank=True, default='',
    #                          help_text='The title of the program')
    #
    # # organization
    # organization = models.TextField(verbose_name='Organization Name', null=False, default='',
    #                                 help_text='The organization affiliated with this program')
    #
    # # description
    # description = models.TextField(verbose_name='Program Description', null=False, default='',
    #                                help_text="A brief description of the program")
    #
    # # subject
    # subject = models.TextField(verbose_name='Subject Keywords', null=False, default='',
    #                            help_text='Subject keywords describing the program, delimited by semicolon')
    #
    # # format
    # format =  'application/octet-stream'
    #
    # # type
    # type = 'HydroProgram'
    #
    # # url
    # program_url = models.TextField(verbose_name='Program URL', null=True, default=None,
    #                        help_text='A URL providing additional information about the program as a whole (e.g. website, documentation, etc...)')
    #

    ############
    # SOFTWARE #
    #----------#
    #  1 .. 1  #
    ############

    # url
    software_url = models.CharField(verbose_name='Software URL', null=True, default= None, max_length=255,
                                    help_text='A URL providing addition information about the software (e.g. source repository, source download, etc...')

    # date_released
    date_released = models.DateTimeField(verbose_name='Date of Software Release',default=dt.datetime.now(),
                                        help_text='The date of the software release (mm/dd/yyyy hh:mm)')

    # version
    software_version = models.CharField(verbose_name="Software Version", null=False,default='',max_length=100,
                                        help_text="The version of the software release")

    # rights
    software_rights = models.TextField(verbose_name="Software Rights", null=False,default="",
                                       help_text="The software rights of the program (e.g. http://creativecommons.org/licenses/by/4.0)")

    # ####################
    # #    REQUIREMENT   #
    # #------------------#
    # # cardinality 0..* #
    # ####################
    #
    # # subject
    # req_subject = models.TextField(verbose_name='Subject Keywords', null=True, default=None,
    #                            help_text='Subject keywords describing the software requirement, delimited by semicolon')
    #
    # # description
    # req_description = models.TextField(verbose_name="Requirement Description", null=False,default='',
    #                                    help_text="A description of the software requirement")
    #
    # # url
    # req_url = models.TextField(verbose_name='Requirement URL', null=True, default=None,
    #                            help_text="A URL providing additional information regarding the software requirement.")


    ###########
    # CREATOR #
    #---------#
    #  1 .. 1 #
    ###########

    # name
    # organization
    # address
    # email
    # phone
    # url

    ###############
    # CONTRIBUTOR #
    #-------------#
    #    0 .. *   #
    ###############

    # name
    # organization
    # address
    # email
    # phone
    # url

    ########
    # Date #
    #------#
    # 1..1 #
    ########

    # created
    # modified










    # #######################
    # # TEMPORAL DEFINITION #
    # #######################
    # # Only for Instance Types
    # hm_begin = models.DateTimeField(verbose_name='Simulation Begin',
    #                              help_text='The start date of the model simulation (mm/dd/yyyy hh:mm)')
    # hm_end  = models.DateTimeField(verbose_name='Simulation End',
    #                             help_text='The end date of the model simulation (mm/dd/yyyy hh:mm)')
    # hm_timestep = models.FloatField(verbose_name='Simulation Time Interval',
    #                              help_text='The timestep interval that is used for calculations (in seconds)')





    class Meta:
        verbose_name = 'HydroProgram'


