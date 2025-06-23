import pytest
from app import app, db, Plant

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed a test plant
            plant = Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_patch_plant(client):
    response = client.patch('/plants/1', json={"is_in_stock": False})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == "Aloe"
    assert data['image'] == "./images/aloe.jpg"
    assert data['price'] == 11.50
    assert data['is_in_stock'] == False
    with app.app_context():
        plant = db.session.get(Plant, 1)
        assert plant.is_in_stock == False

def test_delete_plant(client):
    response = client.delete('/plants/1')
    assert response.status_code == 204
    assert response.data == b''
    with app.app_context():
        plant = db.session.get(Plant, 1)
        assert plant is None

def test_patch_plant_not_found(client):
    response = client.patch('/plants/999', json={"is_in_stock": False})
    assert response.status_code == 404

def test_delete_plant_not_found(client):
    response = client.delete('/plants/999')
    assert response.status_code == 404