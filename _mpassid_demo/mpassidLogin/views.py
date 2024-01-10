from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from pathlib import Path
import environ
import os
import requests

# Initialization of environment variables

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env_file=str(BASE_DIR / 'mpassidLogin.env'))


# Views

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
        'code': code
        })

def exchange_code(code: str):
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    redirect_uri = os.environ.get("REDIRECT_URI")
    token_endpoint = os.environ.get("TOKEN_ENDPOINT")
    userinfo_endpoint = os.environ.get("USERINFO_ENDPOINT")
    
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_endpoint, data=data, headers=headers)
    credentials = response.json()

    #error checking access_token
    if 'access_token' not in credentials:
        return JsonResponse({'error': 'No access token provided.', 'credentials': credentials})
    
    access_token = credentials['access_token']
    
    response = requests.get(userinfo_endpoint, headers={'Authorization': f'Token {access_token}'})
    user = response.json()

    return user