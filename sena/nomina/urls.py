from django.urls import path

from . import views

app_name = 'nomina'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout, name="logout"),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('prueba/', views.prueba, name='prueba'),
    path('colaboradores/', views.colaboradores, name='colaboradores'),
    path('colaborador_guardar/', views.colaborador_guardar, name='colaborador_guardar'),
    path('colaborador_editar/<int:id>/', views.colaborador_editar, name='colaborador_editar'),
    path('colaborador_eliminar/<int:id>/', views.colaborador_eliminar, name='colaborador_eliminar'),
    path('nomina/', views.nomina, name='nomina'),
    # path('nomina_buscar/', views.nomina_buscar, name='nomina_buscar'),
    path('nomina/listar/<str:fecha_inicio>/<str:fecha_fin>/', views.nomina_listar, name='nomina_listar'),

    # path('nomina_listar/<int:id>/', views.nomina_listar, name='nomina_listar'),
    # path('nomina_guardar/', views.nomina_guardar, name='nomina_guardar'),
    path('novedades_nomina/', views.novedades_nomina, name='novedades_nomina'),
    path("novedad_guardar/", views.novedad_guardar, name="novedad_guardar"),
    path("novedad_editar/<int:id>/", views.novedad_editar, name="novedad_editar"),
    path("novedad_eliminar/<int:id>/", views.novedad_eliminar, name="novedad_eliminar"),
    path("usuario_guardar/", views.usuario_guardar, name="usuario_guardar"),
    path('recibo/<int:nomina_id>/', views.recibo_view, name='recibo_view'),
    path('descargar/<int:nomina_id>/', views.descargar_recibo, name='descargar_recibo'),
    path('parafiscales/<int:id>/', views.parafiscales, name="parafiscales"),
    path('provisiones/<int:id>/', views.provisiones, name="provisiones"),
    path('liquidacion/<int:id>/', views.liquidacion, name="liquidacion"),
    path('liquidacion-archivo/<int:id>/', views.liquidacion_view, name='liquidacion_view'),
    path('liquidar_colaborador/<int:id>/', views.liquidar_colaborador, name='liquidar_colaborador'),
    path('descargar-liquidacion/<int:id>/', views.descargar_liquidacion, name='descargar_liquidacion'),
]
