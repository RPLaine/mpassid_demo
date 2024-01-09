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
        print ('Mpassid button pressed.')
        redirect_url = os.environ.get("REDIRECT_URL")
        print ('Redirection to ' + redirect_url)
        return HttpResponseRedirect(redirect_url)
    
    return render(request, 'mpassidLogin/index.html')

def redirect(request):
    print('Getting code...')
    if request.GET.get('code'):
        print('Code received.')
        code = request.GET.get('code')
        print('Code: ', code, sep=': ')
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

    print('Environment variables loaded.')
    
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': 'profile'
    }

    print('Data', data, sep=': ')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_endpoint, data=data, headers=headers)
    credentials = response.json()
    print('Credentials:')
    print(credentials)
    access_token = credentials['access_token']
    print('Access token:')
    print(access_token)
    
    response = requests.get(userinfo_endpoint, headers={'Authorization': f'Token {access_token}'})
    user = response.json()
    print('User:')
    print(user)
    return user

def test(request):
    env_vars = dict(os.environ)
    return JsonResponse(env_vars)
