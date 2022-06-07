from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, 
    CreateView, UpdateView, DeleteView
)
from .models import Lead
from .forms import  LeadModelForm, CustomCreationForm


class SignUpView(CreateView):
    template_name = 'registration/sign_up.html'
    form_class = CustomCreationForm
    
    def get_success_url(self):
        return reverse('login')


class LandingPageView(TemplateView):
    template_name = 'landing.html'


class LeadListView(ListView):
    template_name = 'lead_list.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'


class LeadDetailView(DetailView):
    template_name = 'lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


class LeadCreateView(CreateView):
    template_name = 'lead_create.html'
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def form_valid(self, form):
        send_mail(
            subject='A lead has been created',
            message='Go to the site to see the new lead',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(UpdateView):
    template_name = 'lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadDeleteView(DeleteView):
    template_name = 'lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')