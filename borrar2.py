from socket import *
import sqlite3
from datetime import datetime

DB = "medidor.db"

CREAR_TABLA = (
    "CREATE TABLE MEDICIONES ( "
    "DATE TIMESTAMP NOT NULL ," 
    "SUBDEVID VARCHAR(128) NOT NULL, "
    "OUTLET INTEGER NOT NULL, "
    "CURRENT NUMBER NOT NULL, "
    "VOLTAGE NUMBER NOT NULL, "
    "ACTPOW NUMBER NOT NULL, "
    "REACTPOW NUMBER NOT NULL, "
    "APPARENTPOW NUMBER NOT NULL"
    ");"
)
INSERT_MEDICION = (
    "INSERT INTO MEDICIONES ( "
    "DATE, SUBDEVID, OUTLET, CURRENT, VOLTAGE, "
    "ACTPOW, REACTPOW, APPARENTPOW) VALUES " 
    "(?,?,?,?,?,?,?,?)"
)

def create_db():
    """Crea la base de datos donde se almacenan los datos capturados"""
    try:
        con = sqlite3.connect(DB)
        con.execute(CREAR_TABLA)
    except Exception as err:
        print(err)
    con.commit()
    con.close()

def cargar_medicion(data):
    """Decodifica el mensaje enviado por spm y lo carga en a base de datos"""
    mediciones = eval(data.split("\r\n")[-1])
    dt = datetime.now()
    date = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    try:
        con = sqlite3.connect(DB)
        con.execute(
            INSERT_MEDICION,
            (date, mediciones["subDevId"], mediciones["outlet"], 
             mediciones["current"]/100, mediciones["voltage"]/100, 
             mediciones["actPow"]/100, mediciones["reactPow"]/100,
             mediciones["apparentPow"]/100) 
        )
    except Exception as err:
        print(err)
    con.commit()
    con.close()



def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        serversocket.bind(("192.168.2.105", 9000))
        serversocket.listen(8)
        while(True):
            clientsocket, address = serversocket.accept()
            #import pdb;pdb.set_trace()
            rd = clientsocket.recv(5000).decode()
            cargar_medicion(rd)
            print (rd)
            print ()
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html: charset=utf-8\r\n"
            data += "\r\n"
            data += "<html><body>OK</body></html>\r\n\r\n"
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)
    
    except KeyboardInterrupt:
        print ("Cerrando servidor")
        pass
    except Exception as err:
        print (err)
    
    serversocket.close()

if __name__ == "__main__":
    create_db()
    createServer()
