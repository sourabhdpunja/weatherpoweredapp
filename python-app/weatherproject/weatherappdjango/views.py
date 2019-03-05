from django.http import JsonResponse, HttpResponseBadRequest
from django.http import HttpResponse

from weatherappdjango.models import EmailCredentials
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import json

#TODO add log4j
#TODO corsIntegration
def post_credentials(request):

    if request.method == 'POST':
        response_object = json.loads(request.body.decode('utf-8'))

        email_id = response_object["email"]
        location = response_object["location"]
        latitude = response_object["latitude"]
        longitude = response_object["longitude"]

        if not valid_email(email_id):
            response_json = {"isEmailInvalid": True}
            return JsonResponse(response_json)
        elif not valid_location(location, latitude, longitude):
            response_json = {"isLocationInvalid": True}
            return JsonResponse(response_json)

        # To check if entry has been created in the db
        try:
            EmailCredentials.objects.get(emailId=email_id)
            response_json = {"isEmailPresent": True}
            return JsonResponse(response_json)
        except EmailCredentials.DoesNotExist:
            pass
        except EmailCredentials.MultipleObjectsReturned:
            response_json = {"isEmailPresent": True}
            return JsonResponse(response_json)

        try:
            email_object = EmailCredentials.objects.create(emailId=email_id,
                                                           location=location,
                                                           latitude=latitude,
                                                           longitude=longitude)
        except Exception as e:
            return HttpResponse(status=204)

        if email_object:
            response_json = {"success": True}
            return JsonResponse(response_json)
    else:
        return HttpResponseBadRequest


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


def get_all_credentials(request):
    all_email_entries = list(EmailCredentials.objects.values())
    return JsonResponse({'results': list(all_email_entries)})
