from django.shortcuts import render
from django.conf import settings

import json

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
    json_response = request.GET.get(url, params)
    data = json.loads(json_response)
    Team.objects.create(
        name=data['name'],
        team_id=data['team_id'],
        bot_user_id=data['bot']['bot_user_id'],
        bot_access_token=data['bot']['bot_access_token']
    )
    return HttpResponse('Bot added to your Slack team!')
