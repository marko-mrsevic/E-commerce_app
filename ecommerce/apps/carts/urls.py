from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'carts', views.CartViewSet)

urlpatterns = router.urls
