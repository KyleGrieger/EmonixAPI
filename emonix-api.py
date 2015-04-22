from wsgiref import simple_server
import os
import sys
import falcon
import json
import requests
import subprocess
import smtplib

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
        response['console_response'] = output
        resp.body = fmt(response)
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
        response['console_response'] = output
        resp.body = fmt(response)
        return response
class emailResource:
    def on_get(self, req, resp, message, email, name, subject ):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.set_header('Access-Control-Allow-Origin', '*')
        try:
            
            s=smtplib.SMTP()
            s.connect("smtp.gmail.com",587)
            s.starttls()
            s.login("wirelessdigitalthings@gmail.com", "YOURMOM.COM")
            FROM = str(email)
            TO = ["wirelessdigitalthings@gmail.com"]
            headers = "\r\n".join(["from: " + email,
                       "subject: " + subject,
                       "to: wirelessdigitalthings@gmail.com",
                       "mime-version: 1.0",
                       "content-type: text/html"])
            body = 'name: ' + name + ' email:  ' + email + ' message: ' + message
            # body_of_email can be plaintext or html!                    
            content = headers + "\r\n\r\n" + body
            print(content)
            s.sendmail(FROM, TO, content)
            s.quit()
            response = 'message: ' + content +' was sent'
            resp.body = fmt(response)
            return response

        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            print('exception %s was thrown' % exceptionValue)
            resp.body = 'exception %s was thrown' % exceptionValue
            return 'exception %s was thrown' % exceptionValue


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
openValve = openHeatingValveResource()
closeValve = closeHeatingValveResource()
sendEmail = emailResource()

# things will handle all requests to the '/things' URL path
app.add_route('/valve/open', openValve)
app.add_route('/valve/close', closeValve)
app.add_route('/email/{message}/from/{email}/name/{name}/sub/{subject}', sendEmail)

if __name__ == '__main__':
    # For testing outside a WSGI like gunicorn
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()