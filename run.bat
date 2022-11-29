::script that runs the scraper -> sitgen


::checking if the environment is activated
set virtual_loc=venv\Scripts\activate
@echo off
if "%VIRTUAL_ENV%"=="%VIRTUAL_ENV%" (%virtual_loc%) 

::executing program
python scraper\wscrap.py
C:\DEV\livesl\out\build\x64-Debug\out\generator.exe