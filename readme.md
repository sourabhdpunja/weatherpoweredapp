
The directory is subdivided into two directories
    1. python-app : server side. Django 
    2. weather-app : client side. React

To Install react client:
    1. Navigate inside to folder -> weatherpoweredapp/weather-app/.
    2. Run command -> npm install
    3. After the packages are installed, Run command -> npm start
    4. Open in browser the URL "http://localhost:3000"

To Install Django Server:
    1. Navigate inside to folder -> weatherpoweredapp/python-app/weatherproject/
    2. To run in virtual environmenat
        i)  Run command for windows-> pip install virtualenvwrapper-win
            Run command for Linux/Mac -> sudo pip install virtualenv
        ii) Run command for windows -> mkvirtualenv myproject
            Run command for Linux/Mac -> virtualenv myproject
        iii) Run Command for window -> workon myproject

            Run Command for Linux/Mac -> i) cd myproject
                                         ii) source bin/activate

    3. Run command for windows -> pip install -r requirements.txt
       Run command for Linux/Mac -> sudo pip install -r requirements.txt

    4. Change the settings in .env file.
        Change the database settings in .env file. I have configured it to mysql database engine. You can enter your database
        engine.
        Enter your user and password of the db in DB_USER, DB_PASSWORD settings
        Enter the weatherbit api key in this API_KEY setting.
        You can change the EMAIL_HOST_USER, EMAIL_HOST_PASSWORD for create the smtp connection
        You can change the FROM_EMAIL_ADDRESS for create the email address to be sent to customers through this email Id.
    
    5. Run command -> python manage.py makemigrations weatherproject

    6. Run command -> python manage.py migrate

    7. Run command -> python manage.py runserver

How to use the app after the server and client are running:
    
    1. Using front end application subscribe using a emailaddress and location.
    2. Once successful registration of the user is done, Navigate to folder weatherpoweredapp/python-app/weatherproject/
    3. Run the Django management command -> python manage.py email_trigger
    4. After the cli completes running, the user registered shoud obtain the newsletter





