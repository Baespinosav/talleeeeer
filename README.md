# Taller
 
python -m pip install --upgrade pip
----------------------------------
pip install --upgrade virtualenv
----------------------------------------
python -m venv "C:\ProyectosDjango\TiendaStark_venv"
---------------------------------------------------
call cd /D "C:\ProyectosDjango"
------------------------------------------------
call TiendaStark_venv\Scripts\activate.bat
----------------------------------------
python -m pip install --upgrade pip
----------------------------
pip install django
------------------------
pip install cx_oracle
---------------------
pip install pillow
---------------------------------
pip install djangorestframework
--------------------------
pip install transbank-sdk
----------------------------------------------
call django-admin startproject TiendaStark
----------------------------------------------
call cd TiendaStark
-----------------------------------------------
python manage.py startapp core
----------------------------------------------
python manage.py startapp apirest
--------------------------------------
pip freeze > requirements.txt
--------------------------------------------------
call code "C:\ProyectosDjango\TiendaStark"
