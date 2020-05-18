from django.http import HttpResponse
from django.shortcuts import render

def base(request):
	context = {}
	# return HttpResponse("Hello world !")
	return render(request, 'base.html', context)



def hello(request):
	context = {}
	context['hello'] = 'hi ray'
	context['gender'] = True
	context['age'] = 36
	context['health'] = True
	context['companyList'] = ['yongyou', 'microduino', 'uniwisee']
	# return HttpResponse("Hello world !")
	return render(request, 'hello.html', context)




