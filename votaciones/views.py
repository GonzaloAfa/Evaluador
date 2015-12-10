from operator import itemgetter, attrgetter, methodcaller




import json

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.core import serializers


from participantes.models import Participante, Foto
from votaciones.models import Voto, Finalistas
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



#listado de participantes
@login_required(login_url='/')
def criterios(request):

	context = dict()

	return render(request, 'criterios.html', context)




@login_required(login_url='/')
def fotografias(request, participante, foto):

	context = dict()
	fotos =	Foto.objects.filter(participante__participante = participante).filter(identificador=foto)

	last_id_foto = Foto.objects.latest('id')

	if fotos:

		if fotos[0].id -1 < 1:
			backFoto = fotos[0]
		else:
			backFoto = Foto.objects.get(pk= fotos[0].id - 1)
		

		if fotos[0].id == last_id_foto.id:	
			nextFoto = fotos[0]
		else:
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
def hasvote(request, participante):

	fotos = Foto.objects.filter(participante__participante = participante)

	data = []

	for foto in fotos:

		voto = Voto.objects.filter(jurado = request.user).filter(participante__participante =participante).filter(foto=foto)

		if voto:
			data.append({
					'id'			: foto.identificador,
					'participante' 	: participante,
					'voto' 			: True})
		else:
			data.append({
					'id'			: foto.identificador,
					'participante' 	: participante,
					'voto' 			: False})

	return HttpResponse(json.dumps(data), content_type='application/json')


def listEvaluation(request):

	data = []

	fotos 	= Foto.objects.all()
	jurados	= User.objects.all()


	for foto in fotos:

		evaluaciones 	= []
		sumatoria		= 0


		for jurado in jurados:

			votos = Voto.objects.filter(foto = foto).filter(jurado=jurado)
			
			if votos:
				voto = votos[0]

				evaluaciones.append({
					"jurado" 	: jurado.username,
					"promedio"	: voto.promedio,
					})
				sumatoria = sumatoria + float(voto.promedio)

			else:
				evaluaciones.append({
					"jurado"	: jurado.username,
					"promedio"	: "1",
					})
				sumatoria = sumatoria + float(1)

		data.append({
			"fotografia" 	: foto.nombre,
			"participante" 	: foto.participante.participante,
			"id"			: foto.identificador,
			"evaluaciones"	: evaluaciones,
			"promedio"		: str(sumatoria/jurados.count()),
		})
			

	return HttpResponse(json.dumps(data), content_type='application/json')


def resumenEvaluation(request):

	data = []
	context = dict()
	
	fotos 	= Foto.objects.all()
	jurados	= User.objects.all()

	for foto in fotos:

		sumatoria	= 0
		faltantes 	= []

		votacion = []


		for jurado in jurados:

			votos = Voto.objects.filter(foto = foto).filter(jurado=jurado)
			
			if votos:
				voto = votos[0]
				sumatoria = sumatoria + float(voto.promedio)

				votacion.append({
					"voto" : voto.promedio
				})

			else:
				faltantes.append({
					"jurado"	: str(jurado.email)
					})

				votacion.append({
					"voto" : float(1)
				})
				
				sumatoria 	= sumatoria + float(1)

		data.append({
			"promedio"		: str(sumatoria/jurados.count()),
			"fotografia" 	: foto.nombre,
			"participante" 	: foto.participante.participante,
			"autor" 		: foto.participante.nombre,
			"id"			: foto.identificador,
			"votantes"		: Voto.objects.filter(foto = foto).count(),
			"faltantes"		: faltantes,
			"votacion"		: votacion,
		})

	context["data"] = sorted(data, key=lambda k: k['promedio'], reverse=True) 

	return render(request, 'resumen.html', context)	

@login_required(login_url='/')
def finalist(request):
	context = dict()

	finalist 	= Foto.objects.filter(finalista = True)
	vote 		= Finalistas.objects.filter(jurado = request.user)


	context['finalistas'] 	= finalist

	if vote:
		vote = vote[0]

		context['puedevotar'] 	= False
		context["photo_first"] 	= Foto.objects.get(pk=vote.primer)
		context["photo_second"] = Foto.objects.get(pk=vote.segundo)
		context["photo_third"] 	= Foto.objects.get(pk=vote.tercero)



	else:
		context['puedevotar'] 	= True


	return render(request, 'finalist.html', context)


def rateFinalist(request, first, second, third):

	context = dict()
	data 	= []

	first	= int(first)
	second 	= int(second)
	third	= int(third)

	photo_first 	= Foto.objects.get(pk=first)
	photo_second 	= Foto.objects.get(pk=second)
	photo_third 	= Foto.objects.get(pk=third)

	print request.user 

	vote = Finalistas.objects.filter(jurado = request.user)

	if vote:

		# ya voto
		data.append({
			'msg' : "Usted ya voto",
			'code': 'danger',
			})		
	else:
		if photo_first.finalista and photo_second.finalista and photo_third.finalista:
			
			newVote = Finalistas.objects.create(
				jurado = request.user,
				primer = first,
				segundo= second,
				tercero= third
			)

			newVote.save()

			data.append({
				'msg' : "Voto guardado con exito",
				'code': "success",
				})
		else:
			data.append({
				'msg' : "hay fotos que no son finalistas",
				'code': 'danger',
				})



	return HttpResponse(json.dumps(data), content_type='application/json')
