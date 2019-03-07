from django.http import JsonResponse, HttpResponseBadRequest
from django.http import HttpResponse
import logging
# Custom Imports
from weatherapp.models import Subscribers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

logger = logging.getLogger(__name__)

import json


def post_subscriber(request):
    if request.method == 'POST':
        response_object = json.loads(request.body.decode('utf-8'))

        email_id = response_object["email"]
        location = response_object["location"]
        latitude = response_object["latitude"]
        longitude = response_object["longitude"]

        json_response = check_validations(email_id, location, latitude, longitude)
        if json_response is not None:
            return json_response

        # To check if entry has been created in the db
        try:
            Subscribers.objects.get(emailId=email_id)
            response_json = {"isEmailPresent": True}
            logger.info("Email Id already present in database in post subscriber request.")
            return JsonResponse(response_json)
        except Subscribers.DoesNotExist:
            pass
        except Subscribers.MultipleObjectsReturned:
            response_json = {"isEmailPresent": True}
            logger.error("Multiple objects present for emailid in database in post subscriber request.")
            return JsonResponse(response_json)

        try:
            email_object = Subscribers.objects.create(emailId=email_id,
                                                      location=location,
                                                      latitude=latitude,
                                                      longitude=longitude)
        except Exception as err:
            logger.error("{} raised."
                         " Error creating record in Subscribers during post subscriber request.".format(err.code))
            return HttpResponse(status=204)

        if email_object:
            logger.info("Record successfully created in Subscribers.")
            response_json = {"success": True}
            return JsonResponse(response_json)
    else:
        logger.error("Request made to post subscriber is not a post request.")
        return HttpResponseBadRequest


def check_validations(email_id, location, latitude, longitude):
    if not valid_email(email_id):
        logger.error("Invalid Email Id obtained in post subscriber request.")
        response_json = {"isEmailInvalid": True}
        return JsonResponse(response_json)
    elif not valid_location(location, latitude, longitude):
        logger.error("Invalid location obtained in post subscriber request.")
        response_json = {"isLocationInvalid": True}
        return JsonResponse(response_json)

def valid_email(email_id):
    try:
        validate_email(email_id)
        return True
    except ValidationError:
        return False


def valid_location(location, latitude, longitude):
    if not location or not latitude or not longitude or\
            (latitude < -90 or latitude > 90) or (longitude < -180 or longitude > 180):
        return False
    else:
        return True


def get_all_subscribers(request):
    if request.method == 'GET':
        try:
            logger.info("Querying all records from Subscribers Table in getallsubscribers request.")
            all_email_entries = list(Subscribers.objects.values())
            return JsonResponse({'results': list(all_email_entries)})
        except Exception as err:
            logger.error("{} raised. Error querying for all records from EmailCredentials in getallsubscribers request."
                         .format(err.code))
            return HttpResponse(status=204)
    else:
        logger.error("Request made to getallsubscribers is not a get request.")
        return HttpResponseBadRequest
