from django.urls import path

from . import views

app_name = 'nomina'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('colaboradores/', views.colaboradores, name='colaboradores'),
    path('contacto/', views.contacto, name='contacto'),
    path('documentacion/', views.documentacion, name='documentacion'),
    path('liquidaciones/', views.liquidaciones, name='liquidaciones'),
    path('nomina/', views.nomina, name='nomina'),
    path('novedades_nomina/', views.novedades_nomina, name='novedades_nomina'),
    path('recibos/', views.recibos, name='recibos'),
    path('terminos/', views.terminos, name='terminos'),

]