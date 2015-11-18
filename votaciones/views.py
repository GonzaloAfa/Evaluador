from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.core import serializers


from participantes.models import Participante, Foto
from votaciones.models import Voto
from jurados.models import Jurado
from django.contrib.auth.models import User

#paginator
from django.core.paginator import Paginator, EmptyPage, InvalidPage


#listado de participantes
@login_required(login_url='/')
def participantes(request, page):

	context = dict()

	allParticipantes= Participante.objects.all()
	paginator 		= Paginator(allParticipantes, 10)

	try:
		pages = int(page)
	except:
		pages = 1

	try:
		context['participantes'] = paginator.page(pages)
	except (InvalidPage):
		context['participantes'] = paginator.page(paginator.num_pages)


	return render(request, 'participantes.html', context)


@login_required(login_url='/')
def fotografias(request, participante, foto):

	context = dict()
	fotos =	Foto.objects.filter(participante__participante = participante).filter(identificador=foto)


	if fotos:

		if fotos[0].id -1 < 1:
			backFoto = fotos[0]
		else:
			backFoto = Foto.objects.get(pk= fotos[0].id - 1)
	
		nextFoto = Foto.objects.get(pk= fotos[0].id + 1)

		voto = Voto.objects.filter(jurado = request.user).filter(participante=fotos[0].participante).filter(foto=fotos[0])

		
		context['fotos'] 		= fotos
		context['atrasFoto']  	= backFoto
		context['siguienteFoto']= nextFoto
		context['msg'] 			= ""

		if request.POST:
			originalidad 	= request.POST.get("option-originalidad")
			composicion 	= request.POST.get("option-composicion")
			tecnica 		= request.POST.get("option-tecnica")
			mensaje 		= request.POST.get("option-mensaje")


			if voto:
				voto = voto[0]		

				voto.criterio_1 = originalidad
				voto.criterio_2 = composicion
				voto.criterio_3 = tecnica
				voto.criterio_4 = mensaje
				voto.promedio 	= float((float(originalidad) + float(composicion) + float(tecnica) + float(mensaje))/4)

				voto.save()
				context["voto"] = voto
				context['msg'] = "Voto actualizado"

			else:				
				newVoto = Voto.objects.create(
					
					jurado = request.user,
					participante = fotos[0].participante,
					foto = fotos[0],

					criterio_1 = originalidad,
					criterio_2 = composicion,
					criterio_3 = tecnica,
					criterio_4 = mensaje,
					promedio = float((float(originalidad) + float(composicion) + float(tecnica) + float(mensaje))/4)
				)

				newVoto.save()
				context["voto"] = newVoto
				context['msg'] = "Voto guardado"
		else:
			if voto:
				context['voto'] = voto[0]


		return render(request, 'fotografias.html', context)	

	else:
		return HttpResponseRedirect('/')




## Sirve para consultar si la votacion ya fue realizada
def hasvote(request, participante, foto ):

	voto = Voto.objects.filter(participante__participante =participante).filter(foto__identificador = foto)

	if voto:
		data = {'status': True}
	else:
		data = {'status': False}

	return HttpResponse(json.dumps(data), content_type='application/json')
