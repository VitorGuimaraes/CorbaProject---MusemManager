# -*-coding: utf-8-*-

# System imports:
import sys
import os

# Third party imports:
from omniORB import CORBA, PortableServer
import CosNaming, Sino, Sino__POA
import pygame as pg 

pg.init()

bell_sound = pg.mixer.Sound("bell_ring.ogg")

class Bell(Sino__POA.Bell):

    def ring_bell(self):
        bell_sound.play()
  

# Inicializa o ORB e procura o root POA
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

# Cria uma instância de Bell e uma referência da instância
ei = Bell()
eo = ei._this()

# Obtém uma referência para o root Naming Service
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print("Failed to narrow the root naming context")
    sys.exit(1)


# Os parâmetros podem ser qualquer string. Sugere-se identificar com o nome 
# da classe
name = [CosNaming.NameComponent("Bell Server", "context")]
# Vincula o contexto ao root context
try:
    context = rootContext.bind_new_context(name)
    print("New context bounded: Bell Server")

except CosNaming.NamingContext.AlreadyBound, ex:
    obj = rootContext.resolve(name)
    context = obj._narrow(CosNaming.NamingContext)
    
    if context is None:
        print("Context exists but is not a NamingContext")
        sys.exit(1)

# Vincula o objeto da linha 26 ao contexto
try:
    name = [CosNaming.NameComponent("Bell", "Object")]
    context.bind(name, eo)

except CosNaming.NamingContext.AlreadyBound:
    context.rebind(name, eo)

# Ativa o POA
poaManager = poa._get_the_POAManager()
poaManager.activate()

# Bloqueia o processo infinitamente (ou até o ORB ser desligado)
orb.run()