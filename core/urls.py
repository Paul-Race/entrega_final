from django.urls import path, include
from .views import v_admin, v_colab, v_cliente, v_users, v_advertencia, v_api, v_cliente_api
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tecnica', v_api.TecnicaViewset)
router.register('obra', v_api.ObraViewset)

urlpatterns = [
    path('infoColab', v_admin.infoColab, name="infoColab"),
    path('obrasColab/<id>/', v_admin.obrasColab, name="obrasColab"),
    path('peticiones', v_admin.peticiones, name="peticiones"),
    path('eliminar/<id>/', v_admin.eliminar, name='eliminar'),
    path('rechazar/<id>/', v_admin.rechazar, name='rechazar'),
    path('estadisticas/', v_admin.estadisticas, name='estadisticas'),
    path('RObras', v_colab.RObras, name="RObras"),
    path('CObras', v_colab.CObras, name="CObras"),
    path('UDObras/<id>/', v_colab.UDObras, name="UDObras"),
    path('aprobarObra/<id>/', v_admin.aprobarObra, name="aprobarObra"),
    path('DObras/<id>/', v_colab.DObras, name="DObras"),
    path('msjLeido/<id>/', v_colab.msjLeido, name="msjLeido"),
    path('pagar/<id>/', v_cliente.pagar, name="pagar"),
    path('index/', v_cliente.homeCli, name="homeCli"),
    path('verCarrito/', v_cliente.verCarrito, name="verCarrito"),
    path('misCompras/', v_cliente.misCompras, name="misCompras"),
    path('agregarCarrito/<id>/', v_cliente.agregarCarrito, name="agregarCarrito"),
    path('eliminarCarrito/<id>/', v_cliente.eliminarCarrito, name="eliminarCarrito"),
    path('pagarCarrito/<total>/', v_cliente.pagarCarrito, name="pagarCarrito"),
    path('homeCliAPI/', v_cliente_api.homeCliAPI, name="homeCliAPI"),
    path('verObra/<id>/', v_cliente.verObra, name="verObra"),
    path('login_view/', v_users.login_view ,name="login_view" ),
    path('register/', v_users.register, name="register"),
    path('bloqueado_por_ip/', v_users.bloqueado_por_ip, name="bloqueado_por_ip"),
    path('advertencia/', v_advertencia.advertencia, name="advertencia"),
    path('compras/<int:compra_id>/pdf/', v_cliente.generar_pdf, name='generar_pdf'),
    path('', v_users.toLogin, name=""),
    path('api/', include(router.urls)),
]