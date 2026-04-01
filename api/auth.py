class AuthAPI:
    def __init__(self,client):
        self.client = client
    def login(self, login, password):
        response = self.client.post(
            "/login",
            json={"login": login, "password": password}
        )    
        return response
        