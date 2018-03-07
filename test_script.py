import pytest
import script

@pytest.fixture()
def client():
    app = script.app
    app.testing = True
    client = app.test_client()
    return client

@pytest.mark.parametrize("test_input",
                         [
                             "28.699+77.111+IN/110085+Rohini+Delhi",
                             "28.699+77.111+IN/110985+Rohini+Delhi",
                             "28.494+77.878+IN/121010+Faridabad+Haryana",
                          ])
def test_post_location(client, test_input):
    result = client.post("/post_location",data=test_input, content_type='text/plain')
    assert result.status_code ==  200
    print('/post_location : result - '+str(result.data))

@pytest.mark.parametrize("test_input",
                         [
                             "28.610+77.223",
                             "28.584+77.359",
                             "28.631+77.163",
                          ])
def test_get_using_postgres(client, test_input, request):
    result = client.get("/get_using_postgres",data=test_input, content_type='text/plain')
    assert result.status_code == 200
    print('/get_using_postgres : result - '+str(result.data))

@pytest.mark.parametrize("test_input",
                         [
                             "28.610+77.223",
                             "28.584+77.359",
                             "28.631+77.163",
                          ])
def test_get_using_self(client, test_input):
    result = client.get("/get_using_self", data=test_input, content_type='text/plain')
    assert result.status_code == 200
    print('/get_using_self : result - '+str(result.data))

@pytest.mark.parametrize("test_input",
                         [
                             "28.610+77.223",
                             "28.584+77.359",
                             "28.631+77.163",
                             "28.595+77.225",
                             "28.726+77.168",
                             "28.489+77.025",
                             "28.442+77.315",
                             "28.153+77.319"
                          ])

def test_get_city_name(client, test_input):
    result = client.get("/get_city_name", data=test_input, content_type='text/plain')
    assert result.status_code == 200
    print('/get_using_self : result - '+str(result.data))
