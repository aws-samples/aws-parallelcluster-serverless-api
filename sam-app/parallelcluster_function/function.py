import json
import sys
import boto3
import base64
import os
import io
import contextlib
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
    try:
      stdout = io.StringIO()
      stderr = io.StringIO()
      with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        cli.main()
      print("stdout:\n{}".format(stdout.getvalue()))
      print("stderr:\n{}".format(stderr.getvalue()))
    except SystemExit:
      print("stdout:\n{}".format(stdout.getvalue()))
      print("stderr:\n{}".format(stderr.getvalue()))
      
    #retrieve the pcluster output
    output_to_user = ""
    previous_line = ""
    #remove the lines that contain the [ character. Used to remove the parallelcluster debug lines
    to_remove = ['[']
    output = stdout.getvalue() + stderr.getvalue()
    for line in output.splitlines():
      print(line)
      if not any(to_rem in line for to_rem in to_remove):
        if line.strip():
          if previous_line != line:
            output_to_user = output_to_user + '\n' + line
          previous_line = line
    output_to_user = output_to_user + '\n'
    return {
        'statusCode': 200,
        'body': output_to_user
    }
