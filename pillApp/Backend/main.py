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

pk_num = [1,2,3]
@app.get("/")
async def root():
    result = []
    for pk in pk_num:
        query = engine.execute(select(med).where(med.c.PK == pk)).fetchone()
        # print(query)
        info_query = engine.execute(select(info).where(info.c.PK == pk)).fetchone()

        shape = engine.execute(select(my).where(my.c.PK == query.MY)).fetchone()
        result.append({'PK':query.PK, 'NAME':info_query.NAME, 'MY':shape.MY, 'COLOR':query.COLOR, 'IMAGE':info_query.IMG, 'EFFECT':info_query.EFFECT, 'USAGE':info_query.USAGE})
    # select(info).where(info.c.PK == 0)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="172.30.1.51", port=8000, reload=True) # host : ipconfig해서 IPv4 주소로 변경