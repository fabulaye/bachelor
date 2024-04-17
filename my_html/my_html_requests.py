import requests

def text_request(url):
    request=requests.get(url)
    html_text=request.text
    if request.status_code==200:   
        return html_text
    else: print(f"{request.status_code} problem with request")   