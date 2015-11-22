from django.db import models

class Participante(models.Model):

	participante 	= models.CharField(max_length=50)
	rut 			= models.CharField(max_length=50)
	nombre 			= models.CharField(max_length=50)
	telefono 		= models.CharField(max_length=12)
	lugar 			= models.CharField(max_length=150)
	n_fotos			= models.CharField(max_length=3)

	def __unicode__(self):
		return str(self.participante) +" - "+ self.nombre


class Foto(models.Model):

	participante 	= models.ForeignKey(Participante)
	nombre 			= models.CharField(max_length=150)
	lugar			= models.CharField(max_length=255)
	fecha 			= models.CharField(max_length=30)
	identificador 	= models.CharField(max_length=5)
	guardada		= models.BooleanField(default=None)
	finalista 		= models.BooleanField(default=False)

	def __unicode__(self):
		return self.nombre

