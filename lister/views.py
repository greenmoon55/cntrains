from django.views import generic

import datetime
import qn.qnutils

class IndexView(generic.ListView):
    template_name = 'lister/index.html'
    context_object_name = 'version_list'

    def get_queryset(self):
        files = qn.qnutils.list_all()
        for f in files:
            f['uploadTime'] = datetime.datetime.fromtimestamp(f['putTime'] / 1e7)
        return files

