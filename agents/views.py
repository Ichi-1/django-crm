import random
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import (
    ListView, CreateView, DeleteView,
    UpdateView, DetailView
)
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorLoginRequiredMixin


class AgentListView(OrganisorLoginRequiredMixin, ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDetailView(OrganisorLoginRequiredMixin, DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorLoginRequiredMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f'{random.randint(0, 100000000)}')
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject='You are invited to be a an agent',
            message='You were adder as an agent on DjangoCRM. '
            'Please, come login to start working',
            from_email='admin@test.com',
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(OrganisorLoginRequiredMixin, UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_queryset(self):
        return Agent.objects.all()

    def get_success_url(self):
        return reverse('agents:agent-list')


class AgentDeleteView(OrganisorLoginRequiredMixin, DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agent-list')
