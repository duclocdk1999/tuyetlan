### Create virtual environment
    python3 -m venv venv            # generate a virtual environemnt
    source venv/bin/activate        # activate the env in terminal

### Install required packages:
    pip install -r requirements.txt

### Makemigrations && migrate
    python manage.py makemigrations
    python manage.py migrate

### Initialize data for system
    python manage.py loaddata tuyetlan/fixtures/initial_data

### Run the system
    python manage.py runserver

### Notes:

