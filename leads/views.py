from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorLoginRequiredMixin, PreventSingUpMixin
from django.urls import reverse
from django.views.generic import (
    CreateView, DetailView, DeleteView,
    FormView, ListView, TemplateView,
    UpdateView,
)
from .forms import (
    AssignAgentForm, CustomCreationForm, CategoryModelForm,
    LeadModelForm, LeadCategoryUpdateForm
)
from .models import Category, Lead


class LandingPageView(TemplateView):
    template_name = 'landing.html'


class SignUpView(PreventSingUpMixin, CreateView):
    template_name = 'registration/sign_up.html'
    form_class = CustomCreationForm
     

    def get_success_url(self):
        return reverse('login')


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        # * initial queryset of leads fot the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=False
            )
            # * filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                'unassigned_leads': queryset
            })
        return context


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user

        # * initial queryset of leads fot the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )
            # * filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset


class LeadCreateView(OrganisorLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject='A lead has been created',
            message='Go to the site to see the new lead',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadUpdateView(OrganisorLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # * initial queryset of leads fot the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadDeleteView(OrganisorLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        # * initial queryset of leads fot the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


class AssignedAgentView(OrganisorLoginRequiredMixin, FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignedAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignedAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:lead-list')


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects \
                .filter(organisation=user.agent.organisation) \
                .filter(agent__user=user) \

        return queryset

    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={"pk": self.get_object().id})


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            'unassigned_lead_count':
                queryset.filter(category__isnull=True).count(),
            'lead_count':
                queryset.filter(category__isnull=False).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # * initial queryset of leads fot the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        # * initial queryset of leads fot the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryCreateView(OrganisorLoginRequiredMixin, CreateView):
    template_name = 'category/category_create.html'
    form_class = CategoryModelForm

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('leads:category-list')


class CategoryUpdateView(OrganisorLoginRequiredMixin, UpdateView):
    template_name = 'category/category_update.html'
    form_class = CategoryModelForm

    def get_queryset(self):
        user = self.request.user
        # * initial queryset of leads fot the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

    def get_success_url(self):
        return reverse('leads:category-list')


class CategoryDeleteView(OrganisorLoginRequiredMixin, DeleteView):
    template_name = 'category/category_delete.html'

    def get_queryset(self):
        user = self.request.user
        # * initial queryset of leads fot the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

    def get_success_url(self):
        return reverse('leads:category-list')
