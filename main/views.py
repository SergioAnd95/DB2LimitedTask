from django.views.generic import ListView

from blog.models import Post
from blog.forms import PostSearchForm
# Create your views here.


class MainView(ListView):
    model = Post
    paginate_by = 6
    template_name = 'main.html'
    search_form_class = PostSearchForm
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        self.search_form = self.search_form_class(self.request.GET)
        return self.search_form.search()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = self.search_form

        return ctx