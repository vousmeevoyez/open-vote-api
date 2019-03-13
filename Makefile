clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
init:
	python manage.py init

upgrade:
	python manage.py db upgrade

tests:
	python manage.py test

run:
	python manage.py run

shell:
	python manage.py shell

coverage:
	coverage run --source app/api -m unittest discover -s app/test/

run-prod:
	gunicorn -b flask:5000 -w 2 manage:app

run-stream:
	gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -b flask:5000 -w 1 manage:app 
