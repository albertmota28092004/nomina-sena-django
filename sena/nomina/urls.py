from django.urls import path

from . import views

app_name = 'nomina'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('index_fake/', views.index_fake, name='index_fake'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout, name="logout"),
    path('register/', views.register, name='register'),
    path('colaboradores/', views.colaboradores, name='colaboradores'),
    path('colaborador_guardar/', views.colaborador_guardar, name='colaborador_guardar'),
    path('contacto/', views.contacto, name='contacto'),
    path('documentacion/', views.documentacion, name='documentacion'),
    path('liquidaciones/', views.liquidaciones, name='liquidaciones'),
    path('nomina/', views.nomina, name='nomina'),
    path('nomina_listar/<int:id>/', views.nomina_listar, name='nomina_listar'),
    path('nomina_guardar/', views.nomina_guardar, name='nomina_guardar'),
    path('novedades_nomina/', views.novedades_nomina, name='novedades_nomina'),
    path("novedad_guardar/", views.novedad_guardar, name="novedad_guardar"),
    path('recibos/', views.recibos, name='recibos'),
    path('terminos/', views.terminos, name='terminos'),
    path("usuario_guardar/", views.usuario_guardar, name="usuario_guardar"),
    path('recibo/<int:nomina_id>/', views.recibo_view, name='recibo_view'),
    path('descargar/<int:nomina_id>/', views.descargar_recibo, name='descargar_recibo'),
]