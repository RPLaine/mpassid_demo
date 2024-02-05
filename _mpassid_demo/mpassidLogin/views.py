from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from pathlib import Path
import environ
import os
import requests


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

    data = {
        'grant_type': 'authorization_code',
        'code': code,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    
    response = requests.post(token_endpoint, data=data, headers=headers, auth=auth)
    token = response.json().get('access_token')

    response = requests.get(userinfo_endpoint, headers={'Authorization': f'Bearer {token}'})
    user = response.json()

    return user