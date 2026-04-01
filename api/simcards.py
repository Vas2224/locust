class SimcardsAPI:
    def __init__(self,client,token):
        self.client = client
        self.headers = {"authToken": token}
    def get_empty_phone(self):
        return self.client.get(
            "/simcards/getEmptyPhone",
            headers=self.headers
        )    