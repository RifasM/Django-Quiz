# Django Quiz App
Developed for Efkairies Club, CMRIT
#

### Requirements
- Python3
- Python3-pip
- Django 3.x

#
### Features
- Questions scraped and stored in csv format
- Only for image based questions
- Django Admin page to manage the quiz
- Email responses to users on test completion
- Email sent based on tab switch (to prevent malpractice)

#
### Steps to run
- Scrape and save your files named as `quiz1.csv` through `quiz5.csv` in the root directory
- Install and activate your virtual environment 
    - `pip3 install virtualenv`
    - `virtualenv venv`
    - On Ubuntu 
        - `source venv/bin/activate`
    - On Windows 
        - `cd venv\Scripts`\
        - `activate`
- Install required dependencies
    - `pip3 install -r requirements.txt`
- Make migrations for the database
    - `python3 manage.py makemigrations`
- Apply the migrations to the database
    - `python3 manage.py migrate`
- Collect static files to `static` folder
    - `python3 manange.py collectstatic`
- Export your Django `SECRET_KEY` to your environment
    - On Ubuntu
        - `export SECRET_KEY=<your key>`
    - On Windows
        - `python3 manage.py generate_secret_key`
        - `store SECRET_KEY in PATH of machine`
- Export mailing username and password
    - On Ubuntu
        - `export MAIL_USERNAME=<your mail username>`
        - `export MAIL_PASSWORD=<your mail password>`
    - On Windows
        - `store MAIL_USERNAME in your PATH`
        - `store MAIL_PASSWORD in your PATH`
- Run the server
    - Development `python3 manage.py runserver`
    - Development with `DEBUG=False` - `python3 manage.py runserver --insecure`
    - To run on `Port 80` - `python3 manage.py runserver --insecure 0:80`
        -Remember to stop `apache2` service before running on `Port 80`
        
#
### Contribute
- Feel free to raise issues and suggestions are welcome