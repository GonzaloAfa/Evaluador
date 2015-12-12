from django.contrib import admin
from votaciones.models import Voto, Finalistas, Final

admin.site.register(Voto)
admin.site.register(Finalistas)
admin.site.register(Final)