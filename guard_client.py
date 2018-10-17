# -*-coding: utf-8-*-

# System imports:
import os
import sys

# Third Party Imports
from omniORB import CORBA, PortableServer
import CosNaming, Sino

# Initialise the ORB 
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Tenta conectar ao servidor Bell e retorna seu obj._narrow
def bind():
    try:
        obj = orb.resolve_initial_references("NameService")
        rootContext = obj._narrow(CosNaming.NamingContext)

        name = [CosNaming.NameComponent("Bell Server", "context"),
                CosNaming.NameComponent("Bell", "Object")]
        
        obj = rootContext.resolve(name)
        obj = obj._narrow(Sino.Bell)
        
        if obj is None:
            print("Object reference is not an Sino::Bell")
            sys.exit(1)

        print("Binded succesfully")
        return obj
        
    except CosNaming.NamingContext.NotFound, ex:
        print("Name not found")
        sys.exit(1)

# Chama a função para conectar ao Bell e invoca o método de tocar o sino
def ring_bell():
    obj = bind()
    obj.ring_bell()
