from requests.structures import CaseInsensitiveDict
import requests
from zeep import Client
import logging
logging.getLogger('zeep.wsdl.bindings.soap').setLevel(logging.ERROR)


import pandas as pd

headers = CaseInsensitiveDict()
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
headers["Accept"] = "application/json"
headers["apikey"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFwa3RnaXd6d2xtYWFha3l3aGVoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODM5MjAwNTgsImV4cCI6MTk5OTQ5NjA1OH0.BvmnwvNUcAnCXJTocXlX6kcSL44l5bgY4MGUFdEIKyw"
headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFwa3RnaXd6d2xtYWFha3l3aGVoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODM5MjAwNTgsImV4cCI6MTk5OTQ5NjA1OH0.BvmnwvNUcAnCXJTocXlX6kcSL44l5bgY4MGUFdEIKyw"
from zeep import Client
import logging
logging.getLogger('zeep.wsdl.bindings.soap').setLevel(logging.ERROR)
url = 'https://qpktgiwzwlmaaakywheh.supabase.co/rest/v1/consulta?select=*'

response = requests.get(url=url, headers=headers)
response_data = response.json()
print(response)
#print(response.json())
for item in response_data:
    cpf = item['cpf']
    cpf2 = str(cpf)
    

    try:
        

        
        username = 'vitor.helpvix'
        password = '70da6fe%'

        client = Client('https://ws1.bmgconsig.com.br/webservices/SaqueComplementar?wsdl')

        entrada = {
          'login': username,
          'senha': password,
          'codigoEntidade': 1581,
          'cpf': cpf2,


        }
        # Aqui você pode chamar as operações disponíveis no Web Service
        result = client.service.buscarCartoesDisponiveis(entrada)
        cartoesRetorno = result.cartoesRetorno

        for i in range(2):
            
            numeroContaInterna = cartoesRetorno[i]['numeroContaInterna']
            mensagemImpedimento = cartoesRetorno[i]['mensagemImpedimento']
            teste = mensagemImpedimento['_value_1']
            if teste == None:
                with client.settings(strict=False):
                    entrada = {
                        'login': username,
                        'senha': password,
                        'codigoEntidade': '1581',
                        'cpf': cpf2,
                        'numeroContaInterna': numeroContaInterna,
                        'tipoSaque': 1,
                        'cpfImpedidoComissionar': False
                    }
                    result = client.service.buscarLimiteSaque(entrada)
                    limiteDisponivel = result.limiteDisponivel
                    limiteDisponivel = str(limiteDisponivel).replace(".", ",")
                    print(cpf2, limiteDisponivel, 'RMC')
                    url = 'https://qpktgiwzwlmaaakywheh.supabase.co/rest/v1/saque'
                    user_data = {"saldo": limiteDisponivel, "cpf": cpf2}

                    response = requests.post(url=url, headers=headers, json=user_data)
                    print(response, response.json())
                    try:
                        url = f'https://qpktgiwzwlmaaakywheh.supabase.co/rest/v1/consulta?select=*&cpf=eq.{cpf2}'

                        
                        response = requests.delete(url=url, headers=headers)
                    except:
                        pass
            else:
                try:
                    url = f'https://qpktgiwzwlmaaakywheh.supabase.co/rest/v1/consulta?select=*&cpf=eq.{cpf2}'

                    
                    response = requests.delete(url=url, headers=headers)
                except:
                    pass
                pass
                
                
            
    except:
        try:
            url = f'https://qpktgiwzwlmaaakywheh.supabase.co/rest/v1/consulta?select=*&cpf=eq.{cpf2}'
    
            
            response = requests.delete(url=url, headers=headers)
        except:
            pass
        pass
    
