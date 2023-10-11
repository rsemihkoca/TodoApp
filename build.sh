#!/bin/bash
pwd

ls -a
# Step 1: Create the 'todo' virtual environment
python3 -m venv todo

# Step 2: Activate the 'todo' virtual environment
source todo/bin/activate

# Step 3: Install project dependencies from 'requirements.txt'
pip install -r requirements.txt
echo "Dependencies installed"

# Step 4: Navigate to the Django project directory
# shellcheck disable=SC2164
cd todo_list
echo "Directory changed"

python manage.py collectstatic --noinput
echo "Static files collected"

# Step 5: Create and apply database migrations
python manage.py makemigrations
python manage.py migrate
echo "Database migrated"
# Step 6: Start the Django development server
python manage.py runserver
echo "Server started"