from wsgiref import simple_server
import os
import sys
import falcon
import json
import requests
import subprocess

fmt = lambda obj: json.dumps(obj, indent=4, sort_keys=True)

def cors_header(req, resp):
    """ Set CORs Header in response """
    resp.set_header('Access-Control-Allow-Origin', '*')


class openHeatingValveResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200 
        resp.set_header('Access-Control-Allow-Origin', '*') # This is the default status
        p = subprocess.Popen(['~/NestAPI/setvent.sh 85 open'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            if line == '' and p.poll() != None:
                break
        output = ''.join(stdout)
        response = {} 
        response['console_response'] = str(output)
        resp.body = response
        return response

class closeHeatingValveResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.set_header('Access-Control-Allow-Origin', '*')  # This is the default status
        p = subprocess.Popen(['~/NestAPI/setvent.sh 85 close'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            if line == '' and p.poll() != None:
                break
        output = ''.join(stdout)
        response = {} 
        response['console_response'] = str(output)
        resp.body = response
        return response

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
openValve = openHeatingValveResource()
closeValve = closeHeatingValveResource()

# things will handle all requests to the '/things' URL path
app.add_route('/valve/open', openValve)
app.add_route('/valve/close', closeValve)

if __name__ == '__main__':
    # For testing outside a WSGI like gunicorn
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()