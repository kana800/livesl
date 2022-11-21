::script that runs the scraper -> sitgen


::checking if the environment is activated
set virtual_loc=scraper\venv\Scripts\activate
@echo off
if "%VIRTUAL_ENV%"=="%VIRTUAL_ENV%" (%virtual_loc%) 

::executing program
python scraper\main.py
