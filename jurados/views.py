from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

#autentificacion
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

#usar name url para redireccionar
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf


@login_required(login_url='/')
def logout_session(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))


def login_session(request):

	if not request.user.is_anonymous():
		return HttpResponseRedirect(reverse('finalist' ))

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		access = authenticate(username=username, password=password)

		if access is not None:
			if access.is_active:

				login(request, access)
				return HttpResponseRedirect(reverse('finalist'))
			else:
				return HttpResponseRedirect(reverse('login'))
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponseRedirect(reverse('login'))

	else:
		return render_to_response('login.html', context_instance=RequestContext(request))

