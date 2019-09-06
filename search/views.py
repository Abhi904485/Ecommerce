from django.db.models import Q

# Create your views here.
from django.views.generic import ListView

from products.models import Products


class SearchProductListView(ListView):
    model = Products
    extra_context = {'title': 'Search', 'query': None}
    template_name = 'search_form.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('query', None)
        if query:
            self.extra_context['query'] = query
            return Products.objects.search(query)
        return Products.objects.all()
