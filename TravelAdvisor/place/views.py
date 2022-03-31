from django.http.response import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

import sys
from subprocess import run,PIPE

def home(request):
    # f = open('F:\Aditi\Semesters\SEM6\MiniProject2\TravelAdvisor/Mumbai.txt', 'r',encoding="utf-8")
    # file_content = f.read()
    # f.close()

    
    # places=[
    #     {
    #         'city':'Mumbai',
    #         'summary':file_content,
    #         'summary of sentimental analysis':'summary of sentimental analysis',
    #         'rating':'4.5'
    #     },
    #     {
    #         'city':'Jaipur',
    #         'summary':'summary of Jaipur',
    #         'summary of sentimental analysis':'summary of sentimental analysis',
    #         'rating':'4.5'

    #     },
    #     {
    #         'city':'Hyderabad',
    #         'summary':'summary of Hyderabad',
    #         'summary of sentimental analysis':'summary of sentimental analysis',
    #         'rating':'4.5'
    #     },
    #     {
    #         'city':'Ahmedabad',
    #         'summary':'summary of Ahmedabad',
    #         'summary of sentimental analysis':'summary of sentimental analysis',
    #         'rating':'4.5'
    #     },
    #     {
    #         'city':'New Delhi',
    #         'summary':'summary of New Delhi',
    #         'summary of sentimental analysis':'summary of sentimental analysis',
    #         'rating':'4.5'
    #     }


    # ]
    # context = {
    #     'places': places
    # }
    return render(request, 'place/index.html')#, context)



def about(request):
    return render(request, 'place/about.html', {'title': 'About'})


def location(request):
    inp=request.POST.get('param')

    out1=run([sys.executable,"F:\\Aditi\\Semesters\\SEM6\\MiniProject2\\TravelAdvisor\\scrape.py",inp],shell=False,stdout=PIPE)
    print(out1)

    out2=run([sys.executable,"F:\\Aditi\\Semesters\\SEM6\\MiniProject2\\TravelAdvisor\\summary.py",inp],shell=False,stdout=PIPE)
    print(out2)

    return render(request,'place/index.html',{'summ':out2.stdout.decode("utf-8")})