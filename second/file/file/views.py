from django.http import HttpResponse
from django.shortcuts import render


def index (request): 
    #prashanr = {'name': 'happy','place':'Mars'}
    return render (request,'index.html')

def analyze(request):
    # get the text from html
    djtext=request.POST.get('text','default')
    # check checkbox values
    removepunc=request.POST.get('removepunc','off')
    fullcaps=request.POST.get('fullcaps',  'off')
    newline=request.POST.get('newline','off')
    spaceremover=request.POST.get('spaceremover','off')
    chcounter=request.POST.get('chcounter','off')
    # check which checkbox in on
    # analyzed text
    if removepunc == "on":
        punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed= analyzed + char

        parmas={'purpose':'Removed punctuations','Analized_text':analyzed}
        djtext=analyzed
        
        # return render (request,'analizee.html',parmas)
        # analyzed the text
    if(fullcaps=="on"):
        analyzed= ""
        for char in djtext:
            analyzed = analyzed + char.upper()   
        parmas={'purpose':'changed to Uppercase','Analized_text':analyzed}
        djtext=analyzed
        # return render(request,'analizee.html', parmas)
    if(newline=="on"):
        analyzed =""
        for char in djtext:
            if char !="\n" and char !="\r":
                analyzed= analyzed +char
            else:
                print("no")
        print("pre",analyzed)        
        parmas={'purpose':'line remover','Analized_text':analyzed}
        print(parmas)
        djtext= analyzed
        # return render(request,'analizee.html',parmas)

    if(spaceremover=="on"):
        analyzed=" "
        for index, char in enumerate (djtext):
            if djtext[index]== " " and djtext[index+1]== " ":
                pass
            else:
                analyzed = analyzed + char

        parmas={'purpose':'spaceremover','Analized_text':analyzed} 
        djtext=analyzed
        # return render(request,'analizee.html',parmas)  

    if(chcounter=="on"):
        analyzed=""
        for char in djtext:
            analyze=analyzed+char.count()
        parmas={'purpose':'chcounter','Analized_text':analyzed}
        
    if(removepunc != "on" and fullcaps !="on" and newline !="on" and spaceremover !="on" and chcounter !="on"):
        return HttpResponse("<center><h1>Please select any operation and try again!</h1></center>")
            
            
            
            # return render(request,'analizee.html',parmas)      
    return render(request,'analizee.html',parmas)     
