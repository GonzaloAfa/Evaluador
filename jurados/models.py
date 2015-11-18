from django.db import models

class Jurado(models.Model):

	nombre 				= models.CharField(max_length=50)
	rut 				= models.CharField(max_length=50)
	clave 				= models.CharField(max_length=50)
	cargo 				= models.CharField(max_length=150)

	def __unicode__(self):
		return self.nombre
