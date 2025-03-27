# coding=utf-8
import datetime
import time
import json
from pymongo import MongoClient
from faker import Faker


class Model3:
	def data_generator(self, np, nc):
		# Connect to MongoDB - Note: Change connection string as needed
		client = MongoClient('127.0.0.1:27017')
		db = client['test']

		# delete collection data if exists
		db.drop_collection("Company_PersonEmbebed")

	
        # create and obtain collection
		collection4 = db.create_collection('Company_PersonEmbebed')
		fake = Faker(['it_IT', 'en_US'])

        # Empleados por compañía (repartición)
		empleados_por_compania = np // nc
		restante = np % nc  # Por si no es divisible exacto

		empleados_generados = 0

		for i in range(nc):
			num_empleados = empleados_por_compania + (1 if i < restante else 0)

			empleados = []
			for _ in range(num_empleados):
				persona = {
                    "age": fake.random_int(min=18, max=99),
                    "companyEmail": fake.company_email(),
                    "dateofBirth": datetime.datetime.combine(
                        fake.date_of_birth(minimum_age=18, maximum_age=99), 
                        datetime.datetime.min.time()
                    ),
                    "email": fake.email(),
                    "firstName": fake.first_name(),
                    "fullName": fake.name(),
                    "sex": fake.random_element(elements=("M", "F")),
                }
				empleados.append(persona)
				empleados_generados += 1

			company_doc = {
                "name": fake.company(),
                "domain": fake.domain_name(),
                "email": fake.company_email(),
                "url": fake.url(),
                "vatNumber": fake.random_int(min=100000000, max=9999999999),
                "employees": empleados
            }

			collection4.insert_one(company_doc)
			print(f"{i+1}. Compañía insertada con {num_empleados} empleados")
		client.close()
		return
