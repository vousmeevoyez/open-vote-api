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
