#!/usr/bin/env python
###
### Copyright 2014, Boundary
###
### Licensed under the Apache License, Version 2.0 (the "License");
### you may not use this file except in compliance with the License.
### You may obtain a copy of the License at
###
###     http://www.apache.org/licenses/LICENSE-2.0
###
### Unless required by applicable law or agreed to in writing, software
### distributed under the License is distributed on an "AS IS" BASIS,
### WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
### See the License for the specific language governing permissions and
### limitations under the License.
###

'''
Base class definitions for metric command line tools
'''

import argparse
import errno
import json
import logging
import os
from pprint import pprint
import re
from string import split
import sys

import requests


class MetricCommand():

  def __init__(self,description):
    '''
    Initialize the instance
    '''
    self.parser = argparse.ArgumentParser(description=description)
    self.filter_expression = None

  def getEnvironment(self):
    try:
      self.email = os.environ['BOUNDARY_PREMIUM_EMAIL']
    except(KeyError):
      self.email = None
    try:
      self.apikey = os.environ['BOUNDARY_PREMIUM_API_TOKEN']
    except(KeyError):
      self.apikey = None
    try:
      self.apihost = os.environ['BOUNDARY_PREMIUM_API_HOST']
    except(KeyError):
        self.apihost = 'premium-api.boundary.com'
        
  def configureLogging(self):
    # Handle debug logging correctly
    if self.args.debug == True:
      level = logging.DEBUG
    else:
      level = logging.ERROR
    logging.basicConfig(level=level)

  def validateEnvironment(self):
    # If the email and API key were supplied on the command line
    # then the override those in environment variables
    if self.args.email != None:
      self.email = self.args.email
    if self.args.apikey != None:
      self.apikey = self.args.apikey
    
    # If we do not have either an e-mail or api key then we cannot proceed
    # exit indicating invalid arguments
    if self.email == None or self.apikey == None:
      self.parser.print_usage()
      sys.exit(errno.EINVAL)

  def initialize(self):
    '''
    Initialization operations
    '''
    self.getEnvironment() 
    self.configureArgs()
    self.validateEnvironment()
    self.configureLogging()
          


  def configureArgs(self):
    self.parser.add_argument('-d','--debug',dest='debug',action='store_true',help='Enables debugging')
    self.parser.add_argument('-e','--email',dest='email',action='store',help='e-mail uses to create the account')
    self.parser.add_argument('-t','--api-key',dest='apikey',required=False,action='store')
    self.parser.add_argument('-v', dest='verbose', action='store_true',help='verbose mode')

    self.args = self.parser.parse_args()

    # Output the collected arguments
    logging.debug(self.args.debug)
    logging.debug(self.args.email)
    logging.debug(self.args.patterns)
    logging.debug(self.args.apikey)
    logging.debug(self.args.verbose)

  def fetch(self):
    '''
    Make an API call to get all the metrics associated with the account
    '''
    project = split(self.apikey, '-')[-1]
    url = "https://{0}/project/{1}/metricsEdit".format(self.apihost, project)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, auth=(self.email, self.apikey))
    if r.status_code != 200:
      print(url)
      print(headers)
      print(r)
    self.metrics = json.loads(r.text)
    logging.debug(r.text)

        
if __name__ == "__main__":
  p = MetricExport()
  p.initialize()
