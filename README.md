# **Data jobs trends** 

The data used in this project has been gathered through a survey. 
The survey has been taken place in different countries and ask about the educational level of differente subjects. 
All this data is saved in a SQLite database and enriched with information from an API ('http://api.dataatwork.org/v1/jobs') and from a web ('https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes').
Then it is applied an ETL using Python and the data final data is visualized using the library seaborn.

Here we can find the architecture of the solution:

 ![Alt text](./../../../../Imágenes/arquitectura.png?raw=true "Title") 


### Expected Results:

The user of the script can select a country to visualized the top data jobs or by default the script shows the top data jobs worldwide.

We found and example of the top data jobs worldwide.

 ![Alt text](./../../../../Imágenes/Datos.png?raw=true "Title") 
 




