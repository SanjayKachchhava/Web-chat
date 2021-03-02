
# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views import generic
from django.template.context_processors import csrf
from firstdbtest.models import Student

def getstudentinfo(request):
	c = {}
	c.update(csrf(request))
	return render(None,'addstudentinfo.html', c)

def addstudentinfo(request):
	sname = request.POST.get('studentname', '12344')
	sdate = request.POST.get('birthdate', '')
	s = Student(student_name = sname,student_dob=sdate))
	s.save()
	return HttpResponseRedirect('/firstdb/addsuccess/')

def addsuccess(request):
	return render(None,'addrecord.html')

class StudentListView(generic.ListView):
	model = Student