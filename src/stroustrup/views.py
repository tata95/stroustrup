from django.views import generic
from django.shortcuts import redirect


class HomePage(generic.TemplateView):
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('books:list')

        return super(HomePage, self).dispatch(request, *args, **kwargs)


class AboutPage(generic.TemplateView):
    template_name = "about.html"
