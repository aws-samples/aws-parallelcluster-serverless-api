import json
import sys
import boto3
import base64
import os
import io
import contextlib
import logging
from pcluster import cli

from io import StringIO

import sys


def lambda_handler(event, context):
    #command to execute with ParallelCluster
    command = event["queryStringParameters"]["command"]
    #the cluster name
    cluster_name = ""
    try:
      cluster_name = event["queryStringParameters"]["cluster_name"]
    except:
      cluster_name = ""
    
    #Retrieve pcluster configuration file
    try:
        file_content = base64.b64decode(event['body'])
        path_config = '/tmp/config'
        config_file = open(path_config,'w')
        config_file.write(file_content.decode('utf-8'))
        config_file.close()
    except:
        return {
           'statusCode': 200,
           'body': 'Please specify the pcluster configuration file\n'
        }
    os.environ['HOME'] = '/tmp'
    sys.argv = ["pcluster"]
    sys.argv.append(command)
    
    #append the additional parameters
    try:
      additional_parameters = event["headers"]["additional_parameters"]
      add_params = additional_parameters.split()
      sys.argv = sys.argv + add_params
    except:
      print("no_param")
    sys.argv.append('--config')
    sys.argv.append('/tmp/config')
    if command in ['create', 'delete', 'update', 'start', 'stop', 'status']:
      sys.argv.append(cluster_name)
      
    #execute the pcluster command
    output = ''
    try:
      pcluster_logger = logging.getLogger("pcluster")
      pcluster_logger.propagate = False
      stdout = io.StringIO()
      stderr = io.StringIO()
      with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        cli.main()
      print("stdout:\n{}".format(stdout.getvalue()))
      print("stderr:\n{}".format(stderr.getvalue()))
      output = stdout.getvalue() + '\n' + stderr.getvalue() + '\n'
    except SystemExit as e:
      print("stdout:\n{}".format(stdout.getvalue()))
      print("stderr:\n{}".format(stderr.getvalue()))
      print("exception: {}".format(e))
      output = stdout.getvalue() + '\n' + stderr.getvalue() + '\n' + str(e) + '\n'
        
    return {
        'statusCode': 200,
        'body': output
    }
