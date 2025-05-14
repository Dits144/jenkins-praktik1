from app import app

def test_hello():
    # Membuat client untuk tes
    client = app.test_client()
    
    # Melakukan GET request ke endpoint utama '/'
    response = client.get('/')
    
    # Memastikan status code response adalah 200
    assert response.status_code == 200
    
    # Memastikan teks yang diharapkan ada dalam body response
    assert b"Hello from Jenkins Multibranch Pipeline!" in response.data
