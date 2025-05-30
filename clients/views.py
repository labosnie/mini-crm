from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

class ClientListViews(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        qs = Client.objects.all()
        q = self.request.GET.get('q', '').strip()
        statut = self.request.GET.get('statut', '').strip()

        if q:
            qs = qs.filter(
                Q(nom__icontains=q) |
                Q(email__icontains=q) |
                Q(prenom__icontains=q) |
                Q(ville__icontains=q) 
            )
        if statut:
            qs = qs.filter(statut=statut)
        return qs.order_by('-date_creation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['statut_filter'] = self.request.GET.get('statut', '')
        context['statut_choices'] = Client.STATUT_CHOICES
        return context

class ClientDetailViews(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'

class ClientCreateViews(LoginRequiredMixin, CreateView):
    model = Client
    fields = [
        'nom', 'prenom', 'email', 'telephone',
        'adresse', 'ville', 'code_postal', 'pays',
        'statut', 'notes'
    ]
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        messages.success(self.request, 'Client créé avec succès.')
        return super().form_valid(form)

class ClientUpdateViews(LoginRequiredMixin, UpdateView):
    model = Client
    fields = [
        'nom', 'prenom', 'email', 'telephone',
        'adresse', 'ville', 'code_postal', 'pays',
        'statut', 'notes'
    ]
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        messages.success(self.request, 'Client mis à jour avec succès.')
        return super().form_valid(form)

class ClientDeleteViews(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:client_list')
