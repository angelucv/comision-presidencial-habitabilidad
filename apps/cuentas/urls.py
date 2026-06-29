from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy


app_name = "cuentas"


class LoginCoordinadorView(auth_views.LoginView):
    template_name = "cuentas/login.html"

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy("capacitacion:panel_inicio")
        return reverse_lazy("core:home")


urlpatterns = [
    path("login/", LoginCoordinadorView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
