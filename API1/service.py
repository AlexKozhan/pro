from api.helpers import PetRequestHelper


class PetsApiService:

    def __init__(self, api_request_context):
        self.api_request_context = api_request_context

    def add_pet(self, id, name, photoUrls=["string"]):
        body = PetRequestHelper.generate_body(id=id, name=name, photoUrls=photoUrls)
        new_pet = self.api_request_context.post(url="v2/pet", data=body)
        return new_pet

    def get_pet_by_id(self, id):
        response = self.api_request_context.get(url=f"v2/pet/{id}")
        return response
