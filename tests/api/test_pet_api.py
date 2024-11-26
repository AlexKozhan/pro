import allure
from playwright.sync_api import APIRequestContext

from api.service import PetsApiService
from fixture.test_services_fixture import ID, NAME



@allure.title("Adding new animal test")
@allure.description("This test adds animals to the cart and checks if they have been added")
def test_add_pet(api_request_context: APIRequestContext):
    pets_api = PetsApiService(api_request_context)
    id = ID
    name = NAME

    new_pet = pets_api.add_pet(id=id, name=name)
    assert new_pet.ok, f'Response status code is not ok'

    response = pets_api.get_pet_by_id(id=id)
    pet = response.json()

    actual_result = {'id': pet.get('id'), 'name': pet.get('name')}
    expected_result = {'id': id, 'name': name}
    assert response.ok, f'Response status code is not ok'
    assert actual_result == expected_result, \
        f'Response contains information about wrong pet. Expected {expected_result}, but was {actual_result}'
