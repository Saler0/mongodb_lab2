from pymongo import MongoClient
from datetime import datetime
import time

class Querys:
    def preview(self, results, label):
        print(f"\n{label} (Mostrando hasta 5 resultados):")
        for i, doc in enumerate(results):
            if i >= 5:
                print("... (resultados truncados)")
                break
            print(doc)

    def querys(self, modelo):
        client = MongoClient("127.0.0.1:27017")
        db = client["test"]
        cutoff_date = datetime(1988, 1, 1)

        if modelo == 1:
            print("\n--- Ejecutando queries para Model 1 ---")

            # Q1
            start = time.time()
            result = db.Person.aggregate([
                {"$lookup": {
                    "from": "Company", # Colección externa a la que haremos join
                    "localField": "works_in", # Campo en el documento actual
                    "foreignField": "domain", # Campo en la otra colección que debe coincidir
                    "as": "company_info" # Nombre del nuevo campo que tendrá la info embebida (como un array)
                }},
                {"$unwind": "$company_info"},
                {"$project": {
                    "fullName": 1,
                    "companyName": "$company_info.name"
                }}
            ])
            result = list(result)
            print(f"Q1 M1 Tiempo: {time.time() - start:.4f} segundos")
            self.preview(result, "Q1 Result")

            # Q2
            start = time.time()
            result = db.Person.aggregate([
                {"$group": {
                    "_id": "$works_in",
                    "employeeCount": {"$sum": 1}
                }},
                {"$lookup": {
                    "from": "Company",
                    "localField": "_id",
                    "foreignField": "domain",
                    "as": "company_info"
                }},
                {"$unwind": "$company_info"},
                {"$project": {
                    "companyName": "$company_info.name",
                    "employeeCount": 1
                }}
            ])
            result = list(result)
            print(f"Q2 M1 Tiempo: {time.time() - start:.4f} segundos")
            self.preview(result, "Q2 Result")

            # Q3
            start = time.time()
            result = db.Person.update_many(
                {"dateofBirh": {"$lt": cutoff_date}},
                {"$set": {"age": 30}}
            )
            print(f"Q3 M1 Tiempo: {time.time() - start:.4f} segundos")
            print(f"Documentos modificados: {result.modified_count}")

            # Q4
            start = time.time()
            companies = db.Company.find({})
            modified = 0
            for c in companies:
                db.Company.update_one({"_id": c["_id"]}, {"$set": {"name": c["name"] + " Company"}})
                modified += 1
            print(f"Q4 M1 Tiempo: {time.time() - start:.4f} segundos")
            print(f"Empresas actualizadas: {modified}")

        elif modelo == 2:
            print("\n--- Ejecutando queries para Model 2 ---")

            # Q1
            start = time.time()
            result = db.Person_CompanyEmbebed.find({}, {"fullName": 1, "works_in.name": 1})
            result = list(result)
            print(f"Q1 M2 Tiempo: {time.time() - start:.4f} segundos")
            self.preview(result, "Q1 Result")

            # Q2
            start = time.time()
            result = db.Person_CompanyEmbebed.aggregate([
                {"$group": {
                    "_id": "$works_in.domain",
                    "companyName": {"$first": "$works_in.name"},
                    "employeeCount": {"$sum": 1}
                }}
            ])
            result = list(result)
            print(f"Q2 M2 Tiempo: {time.time() - start:.4f} segundos")
            self.preview(result, "Q2 Result")

            # Q3
            start = time.time()
            result = db.Person_CompanyEmbebed.update_many(
                {"dateofBirh": {"$lt": cutoff_date}},
                {"$set": {"age": 30}}
            )
            print(f"Q3 M2 Tiempo: {time.time() - start:.4f} segundos")
            print(f"Documentos modificados: {result.modified_count}")

            # Q4
            start = time.time()
            people = db.Person_CompanyEmbebed.find({})
            modified = 0
            for p in people:
                updated = p["works_in"]
                updated["name"] += " Company"
                db.Person_CompanyEmbebed.update_one({"_id": p["_id"]}, {"$set": {"works_in": updated}})
                modified += 1
            print(f"Q4 M2 Tiempo: {time.time() - start:.4f} segundos")
            print(f"Documentos actualizados: {modified}")

        elif modelo == 3:
            print("\n--- Ejecutando queries para Model 3 ---")

            # Q1
            start = time.time()
            result = db.Company_PersonEmbebed.aggregate([
                {"$unwind": "$employees"},
                {"$project": {
                    "fullName": "$employees.fullName",
                    "companyName": "$name"
                }}
            ])
            result = list(result)
            print(f"Q1 M3 Tiempo: {time.time() - start:.4f} segundos")
            self.preview(result, "Q1 Result")

            # Q2
            start = time.time()
            result = db.Company_PersonEmbebed.aggregate([
                {"$project": {
                    "companyName": "$name",
                    "employeeCount": {"$size": "$employees"}
                }}
            ])
            result = list(result)
            print(f"Q2 M3 Tiempo: {time.time() - start:.4f} segundos")
            self.preview(result, "Q2 Result")

            # Q3
            start = time.time()
            result = db.Company_PersonEmbebed.update_many(
                {"employees.dateofBirth": {"$lt": cutoff_date}},
                {"$set": {"employees.$[elem].age": 30}},
                array_filters=[{"elem.dateofBirth": {"$lt": cutoff_date}}]
            )
            print(f"Q3 M3 Tiempo: {time.time() - start:.4f} segundos")
            print(f"Documentos modificados: {result.modified_count}")

            # Q4
            start = time.time()
            companies = db.Company_PersonEmbebed.find({})
            modified = 0
            for c in companies:
                db.Company_PersonEmbebed.update_one({"_id": c["_id"]}, {"$set": {"name": c["name"] + " Company"}})
                modified += 1
            print(f"Q4 M3 Tiempo: {time.time() - start:.4f} segundos")
            print(f"Empresas actualizadas: {modified}")

        else:
            print("Modelo no reconocido")

        client.close()
