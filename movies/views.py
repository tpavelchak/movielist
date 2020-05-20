from django.views import generic

from movies.importers import studio_ghibli


class IndexView(generic.TemplateView):
    template_name = "movies/index.html"

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['movies_data'] = studio_ghibli.get_movies_data()
        return ctx
