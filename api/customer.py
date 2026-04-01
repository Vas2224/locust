import random
class CustomerAPI:
    def __init__(self,client,token):
        self.client = client
        self.headers = {"authToken": token}
    def postCustomer(self):
        return self.client.post(
            "/customer/postCustomer",
            json={"name": "abc",
                  "phone": random.randint(100000000, 99999999999),
                  "additionalParameters":{
                      "string": "string"
                  }},
            headers=self.headers      
        )    
    def get_Customer_by_id(self, customer_id):
        return self.client.get(
            "/customer/getCustomerById",
            params={"customerId": customer_id},
            headers=self.headers
        )    
    def findByPhoneNumber(self, token):
        xml_body = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <ns3:Envelope xmlns:ns2="soap" xmlns:ns3="http://schemas.xmlsoap.org/soap/envelope">
        <ns2:Header>
            <authToken>{token}</authToken>
        </ns2:Header>
        <ns2:Body>
            <phoneNumber>79281326346</phoneNumber>
        </ns2:Body>
    </ns3:Envelope>""".format(token = token)
        return self.client.post(
            "/customer/findByPhoneNumber",
            data = xml_body,
            headers={**self.headers, "Content-Type":"application/xml"}
        )

        