# coding=utf-8
import datetime
import time
import json
import random
from pymongo import MongoClient
from faker import Faker


class Model2:
	def data_generator(self,  np, nc):
		# Connect to MongoDB - Note: Change connection string as needed
		client = MongoClient('127.0.0.1:27017')
		db = client['test']

		# delete collection data if exists
		db.drop_collection("Person_CompanyEmbebed")

	
        # create and obtain collection
		collection3 = db.create_collection('Person_CompanyEmbebed')

		fake = Faker(['it_IT', 'en_US'])

		# Diccionario para almacenar las empresas
		companies = {}
	
		for x in range(nc):
			empresa = {
                "domain": fake.domain_name(), 
                "email": fake.email(), 
                "name": fake.company(),
                "url": fake.url(),
                "vatNumber": fake.random_int(min=100000000, max=9999999999),
			}
			companies[x] = empresa  # Almacenar cada empresa en el diccionario
		
		for x in range(np):
			random_key = random.choice(list(companies.keys()))
			random_company = companies[random_key]
			Person_CompanyEmbebed = {
				"age": fake.random_int(min=18, max=99), 
				"campanyEmail": fake.company_email(), 
				"dateofBirh": datetime.datetime.combine(fake.date_of_birth(minimum_age = 18, maximum_age = 99), datetime.datetime.min.time()),
				"email": fake.email(),
				"firstName": fake.first_name(),
				"fullName": fake.name(),
				"sex": fake.random_element(elements = ("M","F")),
				"works_in": random_company 
			}
			collection3.insert_one(Person_CompanyEmbebed)
			print(str(x+1) + ". Document inserted")

		client.close()
		return
