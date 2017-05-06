from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .models import Team

import json, requests

def index(request):
    client_id = settings.SLACK_CLIENT_ID
    return render(request, 'landing.html', {'client_id': client_id})


def slack_oauth(request):
    code = request.GET.get('code')

    params = {
        'code': code,
        'client_id': settings.SLACK_CLIENT_ID,
        'client_secret': settings.SLACK_CLIENT_SECRET
    }
    url = 'https://slack.com/api/oauth.access'
    json_request = requests.get(url, params)
    json_response = json.loads(json_request.text)
    Team.objects.create(
        name=json_response['team_name'],
        team_id=json_response['team_id'],
        bot_user_id=json_response['bot']['bot_user_id'],
        bot_access_token=json_response['bot']['bot_access_token']
    )
    return HttpResponse('Bot added to your Slack team!')
