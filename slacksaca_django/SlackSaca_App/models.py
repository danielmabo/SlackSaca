from django.db import models
from django.utils import timezone #puede no ser necesario

class Team(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=20, primary_key=True)
    bot_user_id = models.CharField(max_length=20)
    bot_access_token = models.CharField(max_length=100)
"""
class User(models.Model):
    user_name = models.CharField(max_length=100, primary_key=True)
    knows = models.CharField(max_length=10000)
    in_team = models.ForeignKey('Team', primary_key=True) #Referencia a qué equipo pertenece (?)
    email = models.CharField(max_length=100)  #Contacto (puede ser anonimo)
    unique_together = (('user_name', 'in_team'),)

class Question(models.Model):
    question = models.CharField(max_length=400) #La pregunta
    subject = models.CharField(max_length=15) #Sobre qué tema (lenguaje)
    asked = models.ForeignKey('User') #Quién ha preguntado
    date_ask = models.DateField()    #Data de consulta

class Knowledge (models.Model):
    sabiduria = models.CharField(max_length=15, primary_key=True) #llenguatge
    username = models.ForeignKey('User', primary_key=True)
    inteam = models.ForeignKey('User', primary_key=True)
    unique_together =(('sabiduria', 'username', 'inteam'),)
"""
