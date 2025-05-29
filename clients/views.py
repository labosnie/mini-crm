from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import ClientForm


class ClientListViews(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Client.objects.filter(utilisateur=self.request.user)
    

class ClientDetailViews(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateViews(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'ville', 'code_postal', 'pays']
    template_name = 'clients/client_form.html'
    
    def form_valid(self, form):
        form.instance.utilisateur = self.request.user
        return super().form_valid(form)

class ClientUpdateViews(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'ville', 'code_postal', 'pays']
    template_name = 'clients/client_form.html'


class ClientDeleteViews(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:client_list')

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/client_detail.html', {'client': client})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, 'Client créé avec succès.')
            return redirect('clients:client_detail', pk=client.pk)
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})

@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client mis à jour avec succès.')
            return redirect('clients:client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form, 'client': client})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé avec succès.')
        return redirect('clients:client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})
