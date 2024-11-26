class PetRequestHelper:
    @staticmethod
    def generate_body(id, name, photoUrls=["string"]):
        return {
            "id": id,
            "name": name,
            "photoUrls": photoUrls
        }
