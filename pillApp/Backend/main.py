from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData, Table, Column, ForeignKey
import uvicorn

app = FastAPI()

engine = create_engine('sqlite:///pillm_3.db',connect_args={"check_same_thread": False})
meta = MetaData(engine)

my = Table('MY',meta,extend_existing=True,autoload=engine)
jh = Table('JH',meta,extend_existing=True,autoload=engine)
bh = Table('BH',meta,extend_existing=True,autoload=engine)
med = Table('MED',meta,extend_existing=True,autoload=engine)
info = Table('INFO',meta,extend_existing=True,autoload=engine)

pk_num = 5

@app.get("/")
async def root():
    query = engine.execute(select(med).where(med.c.PK == pk_num)).fetchone()
    info_query = engine.execute(select(info).where(info.c.PK == pk_num)).fetchone()

    shape = engine.execute(select(my).where(my.c.PK == query.MY)).fetchone()
    # select(info).where(info.c.PK == 0)
    result = [{'PK':query.PK, 'NAME':info_query.NAME, 'MY':shape.MY, 'COLOR':query.COLOR, 'IMAGE':info_query.IMG, 'EFFECT':info_query.EFFECT, 'USAGE':info_query.USAGE}]
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="172.30.1.20", port=8000, reload=True)