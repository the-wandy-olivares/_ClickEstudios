from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden, HttpResponseBadRequest
from Estudios import views

class ForceErrorHandlersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if settings.DEBUG:
            if response.status_code == 404:
                return views.error_redirect_view(request, exception=None)
            elif response.status_code == 500:
                return views.error_redirect_view(request)
            elif response.status_code == 403:
                return views.error_redirect_view(request, exception=None)
            elif response.status_code == 400:
                return views.error_redirect_view(request, exception=None)

        return response