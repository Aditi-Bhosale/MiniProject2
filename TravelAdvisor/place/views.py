from django.http.response import HttpResponse
from django.shortcuts import render
import requests
from django.shortcuts import render, get_object_or_404
import pandas as pd
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

    out1=run([sys.executable,"D:\\dev\\MiniProject2\\TravelAdvisor\\scrape.py",inp],shell=False,stdout=PIPE)
    print(out1)

    out2=run([sys.executable,"D:\\dev\\MiniProject2\\TravelAdvisor\\summary.py",inp],shell=False,stdout=PIPE)
    print(out2)
    ##########################################
    #done=request.POST.get('cin','default')
    #dtwo=request.POST.get('cout','default')
    #run([sys.executable,"D:\\dev\\MiniProject2\\TravelAdvisor\\sentiment_analysis.py"],shell=False,stdout=PIPE)
    url1='http://api.positionstack.com/v1/forward?access_key=f4c6c5799c5362425082bf1ff21cd04e&query='+inp
    r=requests.get(url1)
    data=r.json()
    #print(data)
    lat=str(data['data'][0]['latitude'])
    lng=str(data['data'][0]['longitude'])
    #print(lat,lng)


    url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/nearby"

    querystring = {"latitude":lat,"currency":"USD","longitude":lng,"checkout_date":"2022-04-27","sort_order":"STAR_RATING_HIGHEST_FIRST","checkin_date":"2022-04-26","adults_number":"1","locale":"en_US","guest_rating_min":"4","star_rating_ids":"3,4,5","children_ages":"4,0,15","page_number":"1","price_min":"10","accommodation_ids":"20,8,15,5,1","theme_ids":"14,27,25","price_max":"500","amenity_ids":"527,2063"}

    headers = {
        "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com",
        "X-RapidAPI-Key": "28d383febcmshb1a4fa9bba1166dp10980ejsne7722dfbaa3f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response=response.json()
    #print(response)
    temp=[]
    reviews=[]
    for i in range(5):
        temp.append([response['searchResults']['results'][i]['id'],response['searchResults']['results'][i]['name']])
    print(temp)
    for hotel_id in temp:
        url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/reviews"
        querystring = {"locale":"en_US","hotel_id":hotel_id[0],"page_number":"1"}
        headers = {
            "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com",
            "X-RapidAPI-Key": "28d383febcmshb1a4fa9bba1166dp10980ejsne7722dfbaa3f"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response=response.json()
        #print(response['groupReview'][0]['reviews'])
        
        t=[]
        #print(len(response['groupReview'][0]['reviews']))
        for ind in range(len(response['groupReview'][0]['reviews'])):
            t.append([response['groupReview'][0]['reviews'][ind]['summary']])
        reviews.append(t)
    #print(reviews)
    #print(len(reviews))
    import pickle
    model = pickle.load(open("sentiment_model.sav", "rb"))
    tfidf = pickle.load(open("tfidf.sav","rb"))
    d={}
    for i in range(5):
        pos=0
        neg=0
        df=pd.DataFrame(reviews[i],columns=['rev'])
        X=tfidf.transform(df['rev'])
        ans=model.predict(X)
        for j in ans:
            if j==1:
                pos+=1
            else:
                neg+=1
        d[temp[i][1]]=[pos,neg]
    print(d)

    '''data={}
    for i in range(5):
        data[temp[i][1]]=reviews[i]
    print(data)
    df=pd.DataFrame(data)
    ncsv=inp+".csv"
    df.to_csv(ncsv)'''
    #print(response.text)
    #print(response.text)

    ###########################################

    return render(request,'place/index.html',{'summ':out2.stdout.decode("utf-8"),'hotels':d,'test':"test"})