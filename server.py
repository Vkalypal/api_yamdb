import subprocess


def main():
    cmd = ["python", "api_yamdb/manage.py", "runserver", "0.0.0.0:8000"]
    subprocess.run(cmd)


def makemigrations():
    cmd = ["python", "yatube_api/manage.py", "makemigrations"]
    subprocess.run(cmd)


def migrate():
    cmd = ["python", "api_yamdb/manage.py", "migrate"]
    subprocess.run(cmd)


def createsuperuser():
    cmd = ["python", "api_yamdb/manage.py", "createsuperuser"]
    subprocess.run(cmd)
