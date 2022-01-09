# Quant Assessments

## For applicants
Please fork this repository and clone the specific branch we have specified for your assessment to start working. The prompt will be contained within. Once you have finished, we will have a way for you to submit your work (most likely google form) where you can send us your git repo. 

## For contributors
Please make sure to work on a new branch. Each new branch will be for a different assessment and name them accordingly, starting with the tech stack and then the implementation details.

Make a new folder (with the same name as the branch) and put all relevant files in the folder. Checkout the template for an outline of what it should look like.

**How this works:**

code is in project.py, data is in data folder

Libraries: pandas, flask, sqlalchemy, polygon:

Database is in PgAdmin4.
Accessing webserver using Postman.

I first get the data from Polygon and then write it into a CSV file. I then use that CSV file to create a database (in pgAdmin4). This data is the data suggested (APPL, 1 hour granularity from 12/01/2021 to 12/30/2021).

![image](https://user-images.githubusercontent.com/90427972/148665797-1a5cfff3-e303-4c03-ba5a-41c3a4b44c63.png)

For the webserver, I connected Flask with a separate database (can add to previous database by changing path). I can then post/get values into that database.

So in Postman, I run the POST method (using url + /list), which adds the information that I entered into the new database.

**URL generation**
![image](https://user-images.githubusercontent.com/90427972/148665838-135bdfb8-98e2-4f83-a43e-11b91fed4ecd.png)


**Webserver post**
![image](https://user-images.githubusercontent.com/90427972/148665723-056fa536-4baa-4512-8047-2d14d2013801.png)

**Webserver get**
So when I run GET, you can see that it displays the listing that I just added.

![image](https://user-images.githubusercontent.com/90427972/148665756-9c63bf12-845e-4dc8-b707-0248e7b26738.png)

**Updated database**
In the database, the values have been added into the "listings" database. (previous one was "prices" in which we pulled APPL with 1 hour granularity from 12/01/2021 to 12/30/2021.

![image](https://user-images.githubusercontent.com/90427972/148665933-91a58a6d-3a84-4358-83bf-721c489a57d8.png)

