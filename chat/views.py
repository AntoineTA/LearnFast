from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the last 10 messages and add them to the context
        messages = Message.objects.order_by('-timestamp')[:10]
        context['messages'] = messages

        return context