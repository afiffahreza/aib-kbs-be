# API untuk Expert System RS Hasan Sadikin
# II4042 Kecerdasan Buatan untuk Bisnis

# 18219006 Marcelino Feihan
# 18219014 Zarfa Naida Pratista
# 18219058 Afif Fahreza

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from knowledge import *

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://frontend-kbs.netlify.app"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Tes"}


@app.get("/covid")
async def covid_check(suhu: float, pilek: str, batuk: str, dahak: str, sesak: str, lemas: str):
    engine = CovidCheck()
    engine.reset(suhu=suhu, pilek=pilek, batuk=batuk,
                 sesak=sesak, dahak=dahak, lemas=lemas)
    engine.run()
    return {"message": engine.COVID}
