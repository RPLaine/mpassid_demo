from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from pathlib import Path
import environ
import os
import requests
from requests_oauthlib import OAuth2Session


BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(env_file=str(BASE_DIR / '.env'))

def index(request):
    if request.method == 'POST' and 'mpassid_button' in request.POST:
        redirect_url = os.environ.get("REDIRECT_URL")
        return HttpResponseRedirect(redirect_url)
    
    return render(request, 'mpassidLogin/index.html')

def redirect(request):
    if request.GET.get('code'):
        code = request.GET.get('code')
    else:
        return JsonResponse({'error': 'No code provided.'})

    user = exchange_code(code)

    return JsonResponse({
        'user': user,
        })

def exchange_code(code: str):
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    token_endpoint = os.environ.get("TOKEN_ENDPOINT")
    userinfo_endpoint = os.environ.get("USERINFO_ENDPOINT")

    response = OAuth2Session.fetch_token(self=OAuth2Session(client_id=client_id), token_url=token_endpoint, code=code, client_secret=client_secret)

    access_token = response['access_token']
    
    response = requests.get(userinfo_endpoint, headers={'Authorization': f'Bearer {access_token}'})
    user = response.json()

    return user