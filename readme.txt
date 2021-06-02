Steps to install and run test_management on your local machine

Run $ sudo apt install python3.9-venv` command to install virtual environment
Run $ python3.9 -m venv env command to Create Virtual environment
Run $ source env/bin/activate command to activate virtual environment

Run $ cd test_management command for jump into the project directory
Run $ pip install -r requirements.txt command to Install project requirement file
Run $ python manage.py migrate command to apply migrations on your local machine
Run $ python manage.py runserver command to run project on your local machine


To run the admin side follow the given instructions.
Create super user with the help of $ python manage.py createsuperuser.
Set the credentials for the super user by following the instructions on terminal.
Run "http://127.0.0.1:8000/admin/" on the browser to open the admin panel.
Enter the credentials(i.e. username and password) to login.


To run the user-side flow for category and product management.
Check the postman json(ManagmentAPI's.postman_collection.json) in the project root directory
Import it in your postman All the user related APIs you can find their.

