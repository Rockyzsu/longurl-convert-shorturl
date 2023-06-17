import random
import string
from django.conf import settings

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Count
from django.http import HttpResponseRedirect
from typing import Type

from .serializers import UrlShortenerSerializer
from .models import UrlShortener


class MakeshortUrl(generics.CreateAPIView):
    serializer_class = UrlShortenerSerializer

    def post(self, request: Response) -> Response:
        print('======================')

        hash = string.ascii_uppercase + string.ascii_lowercase + string.digits
        print(hash)
        print(request.data)
        longurl = request.data.get('longurl')
        print(longurl)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        long_url_obj = UrlShortener.objects.filter(longurl=longurl, user_ip_address=ip)

        if long_url_obj.exists():
            long_url_obj = long_url_obj.get()
            return Response({'longurl': long_url_obj.longurl, 'shorturl': settings.HOST_URL + long_url_obj.shorturl})

        shorturl = ''.join(random.sample(hash, 8))
        while UrlShortener.objects.filter(shorturl=shorturl).exists():
            shorturl = ''.join(random.sample(hash, 8))

        url_pair = UrlShortener()
        url_pair.longurl = longurl
        url_pair.shorturl = shorturl
        url_pair.user_ip_address = ip
        url_pair.save()
        shorturl = settings.HOST_URL + shorturl

        return Response({'longurl': longurl, 'shorturl': shorturl})


class RedirectUrl(View):
    def get(self, request: Response, shorturl: str) -> HttpResponseRedirect:
        redirect_link = UrlShortener.objects.filter(shorturl=shorturl).values('longurl').first()['longurl']
        return redirect(redirect_link)


class TheMostPopularUrl(generics.ListAPIView):
    serializer_class = UrlShortenerSerializer

    def get_queryset(self) -> Type[UrlShortener]:
        return UrlShortener.objects.values("longurl").annotate(count=Count('longurl')).order_by("-count")


def get_count_all_shortened_url(request: Response) -> JsonResponse:
    data = UrlShortener.objects.all().count()
    return JsonResponse({'count': data})
