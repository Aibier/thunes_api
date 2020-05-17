# Application Name: Thunes API
This api provides functionalities with jwt authentication, create account, topup account, view account balance, transfer from one account to another account.

### Technologues: Python, Django Rest Framework, CI/CD with Gitlab, Postgres

### To setup application:
1. Assuming you have installed pip, git and gitlab runner and docker, docker-compose.
2. Go to project root: create virtual env by running: ```virtualenv -p python3 venv```
3. To activate virtualenv: ```source venv/bin/activate```
4. Install pakages: ```pip install -r requirements.txt```
5. Create database. first login to postgres then run: ``` CREATE DATABASE thunes_db;```
6. Create role: ```CREATE ROLE thunes_user WITH LOGIN CREATEDB PASSWORD 'password@2020';```
7. Give access to db: ```GRANT ALL PRIVILEGES ON DATABASE thunes_db to thunes_user;```
8. Then exixt from postgres. 
9. Inside virtual env and project root run: ``` python manage.py migrate```
10: Run server: ```python manage.py runserver```
11. Run test: ```python manage.py test```
12. To run docker file locally type: ```docker-compose up -d --build```

### To view API docs
1. View from localhost: ```http://localhost:8000/api/docs/#```
2. View from server: ```http://thunes.globalpeacelove.com/api/docs/```
3. View Blog: http://taymas-technology.globalpeacelove.com/blogs/

### The tool to monitor API
1. Monitor tools: Untrends
2. Will provide credentials if needed, the screenshots will be in blog.


### Author: Tony Aizize
Read more about me at: http://taymas-technology.globalpeacelove.com/about-me
