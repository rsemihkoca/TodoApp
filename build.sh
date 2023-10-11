pip install -r requirements.txt
cd todo_list
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
