from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from lister.models import Version

class IndexView(generic.ListView):
    template_name = 'lister/index.html'
    context_object_name = 'version_list'

    def get_queryset(self):
        return Version.objects.order_by('-release_date')
