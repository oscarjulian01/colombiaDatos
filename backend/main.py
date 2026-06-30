from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import os
from dotenv import load_dotenv

load_dotenv()  #Leer archivo .env
limiter = Limiter(key_func=get_remote_address) #inicializa slowapi, identifica usuario por direccion id para controlar peticiones que hace por min
app = FastAPI(title="Colombia Datos API", version="1.0") #crea web principal
app.state.limiter = Limiter

app.add_middleware(
    CORSMiddleware, #origen de seguridad
    allow_origins = [os.getenv("ALLOWED_ORIGINS", "")],# solo aceptar peticiones que provengan del frontend de React
    allow_methods = ["GET", "POST"], # el servidor permite consultar datos o enviar información, no borrar ni alteral
    allow_headers = ["Content-Type"] 
)

from routers import stats, chat, polls  #importar archivos de lógica (estadísticas, chats y encuestas) bajo el prefij api/v1
app.include_router(stats.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(polls.router, prefix="/api/v1")