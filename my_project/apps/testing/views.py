from django.shortcuts import render
from django.views.decorators.cache import cache_page, never_cache
# Create your views here.


# @cache_page(30)
def testHome(request):
    #  function to test caching
    return render(request, "testing/testhome.html")


# @never_cache
def contact(request):
    #  function to test caching
    return render(request, "testing/contact.html")