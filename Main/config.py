# config.py
import os
from helper.helper import Helper
from sparky_bc import Sparky

# Nota: Recordar ajustar el usuario (user_Lz) y la contraseña (password) a sus variables de entorno de la cuenta
hp = Helper(username=os.environ["user_Lz"], dsn='IMPALA_PROD', max_tries=5, log_path='C:/Users/santiagr/logs')
sp = Sparky(username=os.environ["user_Lz"], password=os.environ["password"], dsn='IMPALA_PROD', hostname="sbmdeblze003.bancolombia.corp")
