from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import mysql.connector
import simplejson
import json
import hashlib
import datetime

@method_decorator(csrf_exempt)
def index(request):
        datas=json.loads(request.POST['params'])
        error=""
        user="nothing"
        etat='0'
        token=''
        try:
            con=mysql.connector.connect(user='root',password='root',host='127.0.0.1',database='snTech')
            cur=con.cursor()
            query="SELECT * FROM users WHERE email=%s AND password=%s"
            cur.execute(query,(str(datas['login']),datas['pwd'],))
            user=cur.fetchone()
            tab=[None,False,""]
            if(user in tab):
                error="okkkk"
            else:
                etat='1'
                token=hashlib.sha1(b"snTecksenegal").hexdigest()
        except:
            error="errrrrro"
        response = {
           'etat': etat,
           'token': token,
           'data': user
        }
        con.close()
        cur.close()
        data = simplejson.dumps(response)
        return HttpResponse(data,content_type='application/json')
@method_decorator(csrf_exempt)
def newUser(request):
    datas=json.loads(request.POST['params'])
    #donnee={'rep':datas}
    #return HttpResponse(simplejson.dumps(donnee),content_type='application/json')
    try:
        con=mysql.connector.connect(user='root',password='root',host='127.0.0.1',database='snTech')
        cur=con.cursor()
        query1="SELECT * FROM users WHERE email=%s || phone=%s"
        cur.execute(query1,(datas['email'],datas['phone'],))
        user=cur.fetchone()
        error=[False,None]
        donnee={}
        if user in error:
            query=("INSERT INTO users "
                    "(idImage,firstName,lastName,adresse,country,birthday,phone,email,password) "
                    " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            cur.execute(query,(1,datas['prenom'],datas['nom'],"mbour",datas['country'],"9/8/2008",datas['phone'],datas['email'],datas['pwd'],))
            con.commit()
            donnee={'etat':1}
        else:
            donnee={'etat':0}
        con.close()
        cur.close()
    except:
        donnee={'etat':0}
        return HttpResponse(simplejson.dumps(donnee),content_type='application/json')
    return HttpResponse(simplejson.dumps(donnee),content_type='application/json')
@method_decorator(csrf_exempt)
def Connexion():
    try:
        con=mysql.connector.connect(user='root',password='root',host='127.0.0.1',database='snTech')
        return con
    except:
        return ""


# Create your views here.
