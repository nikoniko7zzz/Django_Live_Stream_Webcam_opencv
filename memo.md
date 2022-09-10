python3 -m venv myvenv
source myvenv/bin/activate
python3 -V
Python 3.10.5
deactivate
pip freeze > requirements.txt

python manage.py runserver
