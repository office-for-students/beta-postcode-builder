#!/usr/bin/env python

""" exceptions.py: ETL Pipeline Custom Exceptions """

class Error(Exception):
   """ Base Exception Class """
   pass

class StopEtlPipelineWarningException(Error):
    """ A warning is raised during the ETL Pipeline """
    pass

class StopEtlPipelineErrorException(Error):
    """ An error is raised during the ETL Pipeline """
    pass