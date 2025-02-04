from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from medicos.models import Agenda, Especialidade
from .models import Cliente, Consulta




class ClienteCreateView(LoginRequiredMixin ,CreateView):
    
    model = Cliente
    template_name = 'clientes/cadastro.html'
    fields = ['sexo', 'telefone', 'cpf']
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ClienteUpdateView(LoginRequiredMixin, UpdateView):

    model = Cliente
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/update_user.html'
    fields = ['sexo', 'telefone', 'cpf']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        user = self.request.user
        try:
            return Cliente.objects.get(user=user)
        except Cliente.DoesNotExist:
            return None
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        

class ConsultaCreateView(LoginRequiredMixin, CreateView):
    model = Consulta
    login_url = 'accounts:login'
    template_name = 'clientes/cadastro.html'
    fields = ['agenda']
    success_url = reverse_lazy('clientes:minhas_consultas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona as especialidades ao contexto
        context['especialidades'] = Especialidade.objects.all()
        return context

    def form_valid(self, form):
        try:
            form.instance.cliente = Cliente.objects.get(user=self.request.user)
            form.save()
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in e.args[0]:
                messages.warning(self.request, 'Você não pode marcar esta consulta')
                return HttpResponseRedirect(reverse_lazy('clientes:consulta_create'))
        except Cliente.DoesNotExist:
            messages.warning(self.request, 'Complete seu cadastro')
            return HttpResponseRedirect(reverse_lazy('clientes:cliente_cadastro'))
        messages.info(self.request, 'Consulta marcada com sucesso!')
        return HttpResponseRedirect(reverse_lazy('clientes:minhas_consultas'))

    
class ConsultaUpdateView(LoginRequiredMixin, UpdateView):

    model = Consulta
    login_url = 'accounts:login'
    template_name = 'clientes/cadastro.html'
    fields = ['agenda']
    success_url = reverse_lazy('medicos:minhas_consultas')

    def get_queryset(self):
    #Permite edição apenas se a consulta pertence ao usuário logado.
        return Consulta.objects.filter(cliente__user=self.request.user)
    
    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(user=self.request.user)
        return super().form_valid(form)
    
class ConsultaDeleteView(LoginRequiredMixin, DeleteView):
    model = Consulta
    success_url = reverse_lazy('clientes:minhas_consultas')
    template_name = 'form_delete.html'

    def get_queryset(self):
        #Permite exclusão apenas se a consulta pertence ao usuário logado.
        return Consulta.objects.filter(cliente__user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Consulta excluída com sucesso!")
        return reverse_lazy('clientes:minhas_consultas')



class ConsultaListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    template_name = 'clientes/consulta_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        consultas = Consulta.objects.all().order_by('-pk')  # Agora traz todas as consultas

        # Aplica o filtro de especialidade, se fornecido
        especialidade_filtrada = self.request.GET.get('especialidade')
        if especialidade_filtrada:
            consultas = consultas.filter(agenda__medico__especialidade_id=especialidade_filtrada)

        return consultas
    

class MinhasConsultasListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    template_name = 'clientes/minhas_consultas.html'  # Pode ser um template diferente
    context_object_name = 'consultas'

    def get_queryset(self):
        user = self.request.user
        try:
            cliente = Cliente.objects.get(user=user)
        except Cliente.DoesNotExist:
            messages.warning(self.request, 'Crie uma consulta primeiro.')
            return Consulta.objects.none()  # Retorna vazio se o cliente não existir

        return Consulta.objects.filter(cliente=cliente).select_related('agenda', 'agenda__medico', 'agenda__medico__especialidade').order_by('-pk')



def get_agendas(request):
    especialidade_nome = request.GET.get("especialidade_nome")  # Recebendo o nome da especialidade
    
    if especialidade_nome:
        agendas = Agenda.objects.filter(medico__especialidade__nome=especialidade_nome)
    else:
        agendas = Agenda.objects.none()  # Retorna vazio se não houver especialidade

    # Criando a resposta JSON com os horários disponíveis
    data = [{"id": agenda.id, "nome": f"{agenda.medico.nome} - {agenda.medico.especialidade} - {agenda.dia.strftime('%d/%m/%Y')} - {agenda.get_horario_display()}"} for agenda in agendas]

    return JsonResponse(data, safe=False)


cliente_cadastro = ClienteCreateView.as_view()
cliente_atualizar = ClienteUpdateView.as_view()
consulta_lista = ConsultaListView.as_view()
consulta_cadastro = ConsultaCreateView.as_view()
consulta_atualizar = ConsultaUpdateView.as_view()
consulta_excluir = ConsultaDeleteView.as_view()