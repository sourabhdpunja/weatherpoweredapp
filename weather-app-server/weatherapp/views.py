from django.http import JsonResponse, HttpResponseBadRequest
from django.http import HttpResponse
import logging
import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
# Custom Imports
from weatherapp.models import Subscribers

logger = logging.getLogger(__name__)


@csrf_exempt
def post_subscriber(request):
    """
    Method intercepting post request to add subscriber if not already present.
    Parameter:
        request: Request containing the subscriber to be added.
    Return:
        Response containing the status of subscriber been added or not.
    """
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
    """ Checks if emailId and location is valid"""
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
    # latitude should be between -90 to 90 and longitude between -180 to 180
    if location and latitude and longitude and (-90 < latitude < 90) and (-180 < longitude < 180):
        return True
    else:
        return False
