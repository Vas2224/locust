from locust import HttpUser, task, between, SequentialTaskSet
from api.auth import AuthAPI;
from api.customer import CustomerAPI;
from api.simcards import SimcardsAPI;

class yota_task(SequentialTaskSet):
  
    def on_start(self):
        response = AuthAPI(self.client).login("admin", "password")
        if response.status_code != 200:
            print("Авторизация не работает")
            self.interrupt()
            return
        self.token = response.json()["token"]
        print(f"TOKEN:{self.token}")
        self.simcards = SimcardsAPI(self.client, self.token)
        self.customer = CustomerAPI(self.client, self.token)
    @task
    def step1_simcards(self):
         response = self.simcards.get_empty_phone()
         if response.status_code != 200:
             self.interrupt()
             return
         print(response.json())

    @task
    def step2_customer(self):
        response = self.customer.postCustomer()
        if response.status_code != 200:
            self.interrupt()
            return
        self.id = response.json()["id"]
        print(f"ID:{self.id}")

    @task 
    def step3_get_customer(self):
        response = self.customer.get_Customer_by_id(self.id)
        print(response.json())

    @task
    def step4_find_by_PhoneNumber(self):
        response = self.customer.findByPhoneNumber(self.token)
        print(response.json())
  
    # @task
    # def changeCustomerStatus(self):
    #     self.client.post(
    #         "/customer/[customerId]/changeCustomerStatus",
    #         json={"status":"string"}
    #     )        
class setting(HttpUser):
    host = "http://localhost:8080"
    wait_time = between(1, 3)
    tasks=[yota_task]
