
Installation steps::
========================================================================================================
The directory is subdivided into two directories
    1. weather-app-server : server side - Django 
    2. weather-app : client side - React

To Install react client:
    1. Navigate inside to folder -> weatherpoweredapp/weather-app/.
    2. Run command -> npm install
    3. After the packages are installed, Run command -> npm start
    4. After the previous command completes, Open in browser the URL "http://localhost:3000"

To Install Django Server:
    System Requirements:
        Python 3
        Pip 3
    Steps Involved:
    1. Navigate inside to folder -> weatherpoweredapp/weather-app-server/
    2. Activate virtual environment(optional)
    3. Run command for windows -> pip install -r requirements.txt
       Run command for Linux/Mac -> sudo pip install -r requirements.txt

    4. Change the settings in .env file using any text editor.(.env file might be a hidden file in mac and windows)
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

=====================================================================================================
Summary of the project:

Frontend::
------------------------------------------------------------------------------------------------------------- 
I have used react to build the front end application. To make the application have a good look and feel I used components from Material UI. Also To improve reusability I used react-places-autocomplete library to implement the location population leveraging autocompletion for hinted location selection. This made it relatively easy to code and did not have to reinvent the wheel.

Backend::
------------------------------------------------------------------------------------------------------------- 
I have learned and used Django to build the back end application. I have added logging in the application. All the logs are stored inside file "logfile" in weather-app-server/weatherapp/logs folder. To store environment variables I used ".env" file stored in the folder weather-app-server/. The API used for getting temperature information for current and past temperartures was the weatherbit API.

Database::
------------------------------------------------------------------------------------------------------------- 
sqllite database is used for the project since its easy to setup and does not require much settings to get it up and running. The table contained in the database is weatherapp_subscribers table which contains the following fields :: email, location, longitude, latitude, created_date.   

Summary about logic for sending email with personalisation for location of the user::
------------------------------------------------------------------------------------------------------------- 
In order to calculate the state of weather of user's location based on historical weather forecast, I calculated the average temperarture of the location. This was done by fetching the last 5 day temperature from the  current day and calculating their average. After getting the average, I compared it with the current temperarture. Based on this I built personalised emails using this criteria. Hence if current temperature was less than 5 degrees from the average temperature mail corresponding to cold weather is built. If current temperature was more than 5 degrees from the average temperature mail corresponding to warm weather is built. If current temperature was within 5 degrees from the average temperature mail corresponding to normal weather is built.

Scalability::
------------------------------------------------------------------------------------------------------------- 
One of the bottlenecks which I identified early on in the application was the fetch requests to the weather bit API to obtain the temperature. Since the API limits to getting temperature of only one day per request I had to send 6 requests to the weatherbit for a particular location to calculate the average and current temperature. Hence to reduce the number of requests sent to the API a map was used which stored location as key with corressponding email message object value. If a location whose temperatures have been fetched already from the API came again, then the email object previously built is got from the map, hence eliminating the refetch requests to the API for the same location. Another optimization technique used was to calculate the distance between the previously obtained location and current location. If the distance between the two location is within 50km range then the already calculated email object of the closest location is obtained. The assumption for this technique to be used was two location which are close to each other have the same temperatures. In order to calculate the distance, the longitude and latitude of the two location have been used.

Another bottleneck observed was creating the smtp connections for each email sent for an emailId. To eliminate recreation of SMTP connection which is a expensive process, the smtp connection is created once and using the same connection multiple emails are sent. Also to send emails in bulk the send_messages function is used which takes in a list of email objects and sends it together using the same smtp connection.

Re-usability:
------------------------------------------------------------------------------------------------------------- 
In the front end, components have been created for different parts of the UI. For example: Location component, success message, error message, titlebar has been made into a separate component which makes it very easy to remove or add (plug and play) to different parts of the ui without requiring modification to existing layout. Constants file containing the error messages have been placed making it very easy for the developer to only requiring to look into this file to change any verbiage in the validation messages. The post request to the django server has been placed in service folder, to create separtion of concerns between views which only deals with presentation and data fetchs which deals fetching the data. 

In the back end, Django framework itself tries to enforce reusability as it makes the developer modularise the code into MVC architecture. Additionally, I have added utils file which contains reusable functions like calculation of average temperarture and current temperarture, distance between two location. I have also added apiurlconstants file which contains urlconstants defined. I have further created a emailclass folder which contains the email class. This class deals with email related concerns. It creates an email with subject and body personalised according to temperature, creates the emailobject with image embedded.

Re-Inventing the Wheel?
-------------------------------------------------------------------------------------------------------------
In the frontend I have used the react-places-autocomplete library to implement the location population leveraging autocompletion for hinted location selection. I have used Material ui extensively which gives components of shelf making it easier to build. To validate email in the front end I have used email-validator library which provides a function to validate email saving me the trouble to write logic for it.

In the back end I have used validators for valiadating email saving the effort to write validation logic. I have also used python-decouple library for creating and using environment variables making it easy to use and implement. 

Security::
------------------------------------------------------------------------------------------------------------- 
In order to prevent malicious inputs to be added, checks for valid email address, valid location and correct request method(POST only) have been added in the both server and client side code. CORS mechanism has also been using django-cors-headers. I have also added loggers for identifing the state of the program. Additionally I have added all the security specific variables like passwords, API_KEY, usernames, email_host, passwords in a .env file to prevent the passwords to be exposed in the code making it a lot secure.

Usability
-------------------------------------------------------------------------------------------------------------
To make it easier to run the email_trigger program, django management command has been used which requires only a simple command to be executed to send emails to the user. The command is -> python manage.py email_trigger. To make the user not have to install all the dependencies themselves requirements.txt file has been created which contains all the dependencies for the project. Just uisng the command pip install -r requirements.txt adds all teh dependencies fo them. Additionally, Mysqllite database has been used for the project further making it easier for the user to not have the additional overhead of taking care of database connection settings.

Appropriate validations have been given to the user to tell him whether an emailid already exists or is valid and location is valid. If entry has been successfully posted or not, the user is notified of it.
For the emails I have added images/gif to emails sent which pertain to thier current state of the temperature. For example if the temperature is colder than the average temperature I have added a cold image in the email.

