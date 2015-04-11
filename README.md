# EmonixAPI

Falcon Rest api for Emonix

## Setup

	virtualenv ENV
	source ENV/bin/activate
	pip install -r requirements.txt

## Running

Locally

	gunicorn  emonix-api:app

Globally on studioxps

	gunicorn --bind [::]:15000 emonix-api:app

## Usage

	curl http://studioxps.wings.cs.wisc.edu:15000/valve/open

Should open the valve and return stdout

	curl http://studioxps.wings.cs.wisc.edu:15000/valve/close

Should close the valve and return stdout

*Please note that this is not a secure API and does not require authentication.
The api should only be run for demonstration purposes until authentication is added.





