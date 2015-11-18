import xlrd
import httplib, urllib, urllib2, cStringIO, cookielib
from StringIO import StringIO

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.core import serializers


from participantes.models import Participante, Foto

urlSession 	= "https://ucampus.uchile.cl/?_LB=ucampus81-int&_sess=d295m4vr506oiqrc19607a8cc0"


def getDataXLS(request):

	book 	= xlrd.open_workbook("data/concurso.xls")
	sheet 	= book.sheet_by_index(0)
	data = []

	for row in range(1, sheet.nrows):

		data.append({
			"ID"				: int(sheet.cell_value(row, 0)),	
			"rut"				: sheet.cell_value(row, 1),	
			"nombre_completo"	: sheet.cell_value(row, 2),	
			"telefono"			: sheet.cell_value(row, 3),	
			"lugar"				: sheet.cell_value(row, 4),	
			"n_fotos"			: int(sheet.cell_value(row, 5)),	
			"foto_1_nombre"		: sheet.cell_value(row, 6),	
			"foto_1_lugar"		: sheet.cell_value(row, 7),	
			"foto_1_fecha"		: sheet.cell_value(row, 8),	
			"foto_2_nombre"		: sheet.cell_value(row, 9),	
			"foto_2_lugar"		: sheet.cell_value(row, 10),	
			"foto_2_fecha"		: sheet.cell_value(row, 11),	
			"foto_3_nombre"		: sheet.cell_value(row, 12),	
			"foto_3_lugar"		: sheet.cell_value(row, 13),	
			"foto_3_fecha"		: sheet.cell_value(row, 14),	
		})


	for element in data:

		participante = element["ID"]

		p = Participante.objects.filter(participante = participante)

		print "NEW "+str(participante)

		if p:
			print "EXIST "+str(participante)
		else:
			nuevoParticipante = Participante.objects.create(
				participante 	= element["ID"],
				rut 			= element["rut"],
				nombre 			= element["nombre_completo"],
				telefono 		= element["telefono"],
				lugar 			= element["lugar"],
				n_fotos 		= element["n_fotos"],
				)

			nuevoParticipante.save()


			if (element["foto_1_nombre"]):

				nuevaFoto1 = Foto.objects.create(
				participante 	= nuevoParticipante,
				nombre 			= element["foto_1_nombre"],
				lugar 			= element["foto_1_lugar"],
				fecha 			= element["foto_1_fecha"],
				identificador 	= "0",
				guardada 		= False,

				)
				nuevaFoto1.save()

			if (element["foto_2_nombre"]):

				nuevaFoto2 = Foto.objects.create(
					participante 	= nuevoParticipante,
					nombre 			= element["foto_2_nombre"],
					lugar 			= element["foto_2_lugar"],
					fecha 			= element["foto_2_fecha"],
					identificador 	= "1",
					guardada 		= False,
					)
				nuevaFoto2.save()

			if(element["foto_3_nombre"]):
				nuevaFoto3 = Foto.objects.create(
					participante 	= nuevoParticipante,
					nombre 			= element["foto_3_nombre"],
					lugar 			= element["foto_3_lugar"],
					fecha 			= element["foto_3_fecha"],
					identificador 	= "2",
					guardada 		= False,
					)
				nuevaFoto3.save()


	data = {'status' : 200}
	return HttpResponse(data, content_type='application/json')


def getPhotos(request):
	fotos = Foto.objects.all()
	data = {'status' : "200"}

	if fotos:

		for foto in fotos:

			if foto.guardada == False:

				status = getPhotoUCAMPUS(foto.participante.participante, foto.identificador)
				print "Photo status "+str(status)

				if status == "200":
					foto.guardada = True
					foto.save()
				else:
					data = {
						'status' 	: "501",
						'comment' 	: "Problemas de conexion",
						}
					return HttpResponse(data, content_type='application/json')
			
	else:
		data = {
			'status' 	: "500",
			'comment' 	: "No hay elementos en la base de datos",
			}


	return HttpResponse(data, content_type='application/json')



def getPhotoUCAMPUS(id, img):

	url 		= 'https://ucampus.uchile.cl/m/fcfm_concurso_fotografico/foto?id='+str(id)+'&img='+str(img)


	cj 			= cookielib.CookieJar()
	connection 	= urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	connection.open(urlSession, {})

	response 	= connection.open(url)

	print str(response.getcode()) + " - "+url

	if response.getcode() == 200:

		f = open("static_root/img/concurso_ID_"+str(id)+"_"+str(img)+".jpg", 'wb')
		f.write(response.read())
		f.close()

		connection.close()
		return "200"
	else:
		connection.close()
		return "404"
