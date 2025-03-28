# Tarea MongoDB Milenko Espinoza

## Preparacion y ejecucion
activar entorno virtual: 
```bash
venv\Scripts\activate
```
Instalar librerias:
```bash
pip install -r requirements.txt
```

en windows para ejecutar:
```bash
python upcschool_mongolab.py
```

## Querys Modelo1
 
 * Q1: For each person, retrieve their full name and their company’s name

 * Q2: For each company, retrieve its name and the number of employees

* Q3: For each person born before 1988, update their age to 30

* Q4: For each company, update its name to include the word “Company

## Querys Modelo2

## Querys Modelo3

## Querys Modelo4

## Tiempos
|      | Q1          | Q2         |      Q3     | Q4          |
|------|-------------|------------|-------------|-------------|
| M1   | 121.199 seg | 4.5346 seg | 1.4002 seg  | 0.4972 seg  |
| M2   | 0.5463 seg  | 0.0482 seg | 1.7263 seg  | 11.8511 seg |
| M3   | 0.5226 seg  | 0.0230 seg | 0.1352 seg  | 0.8292 seg  |

## Preguntas

1. Order queries from best to worst for Q1. Which model performs best?
Why?

desempeño:
mejor > medio > peor
Q1.M3 > Q1.M2 > Q1.M1

Q1.M3 fue la mejor porque no necesita realizar joins entre colecciones
ya que los datos de los empleados están embebidos dentro del documento de la empresa.

2. Order queries from best to worst for Q2. Which model performs best?
Why?

desempeño:
mejor > medio > peor
Q2.M3 > Q2.M2 > Q2.M1

Q2.M3 fue le mejor  porque usa $size directamente sobre un array embebido, evitando agrupaciones y joins.

3. Order queries from worst to best for Q3. Which model performs
worst? Why?

desempeño:
peor > medio > mejor
Q3.M2 > Q3.M1 > Q3.M3

Q3.M2 fue la peor porque ya que al ser una actualizacion masiva en la que se esta obligado a hacer un scan entero de todos los documentos la peor es Q3.M2 ya que son mas numeros de documentos 48000.


4. Order queries from worst to best for Q4. Which model performs worst? Why?

desempeño:
peor > medio > mejor
Q4.M2 > Q4.M3 > Q4.M1

Q4.M2 fue el peor por que al tener que hacer una actualizacion masiva a todos las empresas Q4.M2 es el unico que no tiene acceso directo a las empresas por lo que se ve obligado a revisar todos los 48000 documentos.

5. What are your conclusions about denormalization or normalization of
data in MongoDB? In the case of updates, which offers better performance?

La desnormalización (embebido) ofrece mejor rendimiento en lecturas, especialmente cuando los datos relacionados se acceden juntos.

Sin embargo, para actualizaciones (como cambiar el nombre de una empresa o la edad de empleados), los modelos normalizados pueden ser más eficientes, porque no se requiere actualizar múltiples documentos que contienen los mismos datos embebidos.