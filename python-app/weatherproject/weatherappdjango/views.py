from django.http import JsonResponse

from weatherappdjango.models import EmailCredentials
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import json


def postCredentials(request):
    responseobject = json.loads(request.body.decode('utf-8'))

    emailId = responseobject["credential"]["email"]
    try:
        validate_email(emailId)
    except ValidationError as e:
        responseJson = {"success": False, "isEmailPresent": False, "isEmailInvalid": False}
        return JsonResponse(responseJson)

    location = responseobject["credential"]["location"]
    latitude = responseobject["credential"]["latitude"]
    longitude = responseobject["credential"]["longitude"]

    if EmailCredentials.objects.filter(emailId=emailId).exists():
        responseJson = {"success": False, "isEmailPresent": True}
        return JsonResponse(responseJson)

    EmailCredentials.objects.create(emailId=emailId,
                                    location=location,
                                    latitude=latitude,
                                    longitude=longitude)

    # To check if entry has been created in the db
    try:
        EmailCredentials.objects.get(emailId=emailId)
        responseJson = {"success": True, "isEmailPresent": False, "isEmailInvalid": True}
        return JsonResponse(responseJson)
    except EmailCredentials.DoesNotExist:
        responseJson = {"success": False, "isEmailPresent": False, "isEmailInvalid": True}
        return JsonResponse(responseJson)


def getAllCredentials(request):
    allEmailEntries = list(EmailCredentials.objects.values())
    return JsonResponse({'results': list(allEmailEntries)})