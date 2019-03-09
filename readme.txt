
The directory is subdivided into two directories
    1. weather-app-server : server side. Django 
    2. weather-app : client side. React

To Install react client:
    1. Navigate inside to folder -> weatherpoweredapp/weather-app/.
    2. Run command -> npm install
    3. After the packages are installed, Run command -> npm start
    4. After the previous command completes, Open in browser the URL "http://localhost:3000"

To Install Django Server:
    System Requirements:
        Python 3
        Pip 3
    1. Navigate inside to folder -> weatherpoweredapp/weather-app-server/
    2. Activate virtual environment(optional)
    3. Run command for windows -> pip install -r requirements.txt
       Run command for Linux/Mac -> sudo pip install -r requirements.txt

    4. Change the settings in .env file.
        Enter the weatherbit api key in this API_KEY setting.
        You can change the EMAIL_HOST_USER, EMAIL_HOST_PASSWORD for create the smtp connection
        You can change the FROM_EMAIL_ADDRESS for create the email address to be sent to customers through this email Id.
    
    5. Run command -> python manage.py makemigrations weatherapp

    6. Run command -> python manage.py migrate

    7. Run command -> python manage.py runserver

How to use the app after the server and client are running:
    
    1. Using front end application subscribe using a emailaddress and location.
    2. Once successful registration of the user is done, Navigate to folder weatherpoweredapp/weather-app-server/
    3. Run the Django management command -> python manage.py email_trigger
    4. After the cli completes running, the user registered shoud obtain an email.





