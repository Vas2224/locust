from locust import HttpUser, task, between, SequentialTaskSet
import random;

class yota_task(SequentialTaskSet):
    host = "http://localhost:8080"
    wait_time = between(1,3)
    def on_start(self):
        response = self.client.post(
            "/login",
            json={"login": "admin", "password": "password"}
        )
        if response.status_code != 200:
            print("Авторизация не работает")
            self.interrupt()
            return
        print(response.status_code)
        print(response.json())
        print(response.text)
        self.token = response.json()["token"]
        print(f"TOKEN:{self.token}")
    @task
    def simcards(self):
         response = self.client.get(
             "/simcards/getEmptyPhone",
             headers={"authToken":f"{self.token}"}
         )
         print(response.status_code)
         print(response.json())
    @task
    def customer(self):
        response = self.client.post(
            "/customer/postCustomer",
            json={
                "name": "asd",
                "phone": random.randint(10000000, 99999999),
                "additionalParameters":{
                    "string": "string"
                }
            },
            headers={"authToken": f"{self.token}"}
        )     
        print(response.json())
        print(response.status_code)
        print(response.text)
        self.id = response.json()["id"]
        print(f"ID:{self.id}")
    @task 
    def getCustomer(self):
        response = self.client.get(
            "/customer/getCustomerById",
            params={"customerId": f"{self.id}"},
            headers={"authToken":f"{self.token}"}
        )    
        print(response.json())
        print(response.status_code)
        print(response.text)
    @task
    def find_by_PhoneNumber(self):
        xml_body = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <ns3:Envelope xmlns:ns2="soap" xmlns:ns3="http://schemas.xmlsoap.org/soap/envelope">
        <ns2:Header>
            <authToken>{token}</authToken>
        </ns2:Header>
        <ns2:Body>
            <phoneNumber>79281326346</phoneNumber>
        </ns2:Body>
    </ns3:Envelope>""".format(token = self.token)
        response = self.client.post(
            "/customer/findByPhoneNumber",
            data=xml_body,
            headers={"authToken":f"{self.token}",
                    "Content-Type": "application/xml"}
        ) 
        print(response.json())
        print(response.status_code)
        print(response.text)   
        self.customerId=response.json()["customerId"]
    # @task
    # def changeCustomerStatus(self):
    #     self.client.post(
    #         "/customer/[customerId]/changeCustomerStatus",
    #         json={"status":"string"}
    #     )        
class setting(HttpUser):
    host = "http://localhost:8080"
    wait_time = between(1,3)
    tasks=[yota_task]
