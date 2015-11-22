import xlrd
import httplib, urllib, urllib2, cStringIO, cookielib
from StringIO import StringIO

urlSession = "https://ucampus.uchile.cl/?_LB=ucampus82-int&_sess=6c2r1di4if8emdheqg4c16lp22"

def getPhoto(id, img):

	url 		= 'https://ucampus.uchile.cl/m/fcfm_concurso_fotografico/foto?id='+str(id)+'&img='+str(img)

	cj 			= cookielib.CookieJar()
	connection 	= urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	connection.open(urlSession, {})

	response 	= connection.open(url)

	print str(response.getcode()) + " - "+url


	if response.getcode() == 200:
		f = open("../img/concurso_ID_"+str(id)+"_"+str(img)+".jpg", 'wb')
		f.write(response.read())
		f.close()

	connection.close()
    
def getData():

	book 	= xlrd.open_workbook("concurso.xls")
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
		for nPhoto in range(0,element["n_fotos"]):
			print str(element["ID"]) +" - "+str(nPhoto);
			getPhoto(element["ID"], nPhoto)

getData()