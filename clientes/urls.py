from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('registro/', views.cliente_cadastro, name='cliente_cadastro'),
    path('atualizar/', views.cliente_atualizar, name='cliente_atualizar'),
    path('consultas/', views.consulta_lista, name='consulta_list'),
    path('minhas-consultas/', views.MinhasConsultasListView.as_view(), name='minhas_consultas'),  # Lista apenas as do usuário
    path('consultas/criar/', views.consulta_cadastro, name='consulta_create'),
    path("get_agendas/", views.get_agendas, name="get_agendas"),
    path('consultas/editar/<int:pk>/', views.consulta_atualizar, name='consulta_update'),
    path('consultas/excluir/<int:pk>/', views.consulta_excluir, name='consulta_delete'),
]