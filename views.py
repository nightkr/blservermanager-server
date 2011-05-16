from django.http import Http404
from django.shortcuts import render_to_response, redirect
from blmanager.forms import AdminKeyInputForm
from blmanager import models

def details(request, key):
	if key not in models.servers_and_webclients:
		raise Http404()
	return render_to_response("blmanager/details.html.haml", {"key": key})

def index(request):
	form = AdminKeyInputForm()
	if "key" in request.GET:
		form = AdminKeyInputForm(request.GET)
		if form.is_valid():
			return redirect(details, key=request.GET["key"])
	return render_to_response("blmanager/index.html.haml", {"form": form})
