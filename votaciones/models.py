from django.db import models

from django.contrib.auth.models import User
from jurados.models import Jurado
from participantes.models import Participante, Foto

class Voto(models.Model):

	jurado 			= models.ForeignKey(User)
	participante 	= models.ForeignKey(Participante)
	foto			= models.ForeignKey(Foto)

	criterio_1 		= models.CharField(max_length=10)
	criterio_2 		= models.CharField(max_length=10)
	criterio_3 		= models.CharField(max_length=10)
	criterio_4 		= models.CharField(max_length=10)

	promedio 		= models.CharField(max_length=10)

	finalista 		= models.BooleanField(default=False)
	criterio_5 		= models.CharField(max_length=10)