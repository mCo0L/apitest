import requests
import pytest

def test_post_location():
    url = 'http://127.0.0.1:8000/post_location'
    headers = {'Content-type': 'text/plain'}
    data = ["28.6333+77.2167+IN/110001+Connaught Place+New Delhi","28.491+77.284+IN/121009+Lal Kua+Haryana",]
    print("\n--------API 1 /post_location--------\n")
    for el in data:
        response = requests.post(url, data=el,headers=headers)
        print(response.text)
        if response.text[:16] not in ['Location already','A Nearby/Same Lo','---Location adde']:
            assert response


def test_get_using_postgress():
    url = 'http://127.0.0.1:8000/get_using_postgres'
    headers = {'Content-type': 'text/plain'}
    data = ["28.609+77.223","28.640+77.062"]
    print("\n--------API 2 /get_using_postgres--------\n")
    for el in data:
        response = requests.get(url, data=el,headers=headers)
        print(response.text)
        if response.text[:16] not in ["Places in 5KM Ra", "No Place found i"]:
            assert response

def test_get_self():
    url = 'http://127.0.0.1:8000/get_using_self'
    data = ["28.609+77.223","28.640+77.062"]
    headers = {'Content-type': 'text/plain'}
    print("\n--------API 3 /get_using_self--------\n")
    for el in data:
        response = requests.get(url, data=el,headers=headers)
        print(response.text)
        if response.text[:16] not in ["Places in 5KM Ra", "No Place found i"]:
            assert response

def test_get_city_name():
    url = 'http://127.0.0.1:8000/get_city_name'
    data = ["28.609+77.223","28.640+77.062"]
    headers = {'Content-type': 'text/plain'}
    print("\n--------API 4 /get_city_name--------\n")
    for i in data:
        response = requests.get(url, data=i,headers=headers)
        print(response.text)
        if response.text[:8] != "Location":
            assert response

test_post_location()
test_get_using_postgress()
test_get_self()
test_get_city_name()
