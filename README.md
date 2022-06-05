# Developers_Search_Django_Project
This project is part of a Udemy course by [Dennis Ivy](https://www.udemy.com/course/python-django-2021-complete-course/)

>This project is in form of a website designed to search for developers with their various skill sets and reviews.
> A new developer can login, register an account, create skills and profile, review projects, send messages etc.
> The application sends an email to welcome a newly registered user.
> The project also includes an **API** created using the djangorestframework

### Screenshots

#### Project homepage
![Website homepage](https://github.com/Pinchez25/Developers_Search_Django_Project/blob/main/screenshots/homepage.png)

#### Projects page
![Website Products](https://github.com/Pinchez25/Developers_Search_Django_Project/blob/main/screenshots/products.png)

> **To run the project, create a virtual environment and pip install the requirements.txt dependencies or just pip install.**
 
 ```shell
    pip install -r requirements.txt
  ```
  
  >> **Edit the email settings in the settings.py file to include your own credentials (EMAIL_HOST_USER & EMAIL_HOST_PASSWORD).**
  
    
       EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
       EMAIL_HOST = "smtp.gmail.com"
       EMAIL_PORT = 587
       EMAIL_USE_TLS = True
       EMAIL_HOST_USER = ''
       EMAIL_HOST_PASSWORD = ''
  
  >> **Create a superuser to enable you access to admin site**

    python manage.py createsuperuser
  
  > **start the server by running the following command**
  
      python manage.py runserver
    
   
   
    
  
