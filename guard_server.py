# -*-coding: utf-8-*-

# System imports:
import os
import sys

# Third Party Imports
from omniORB import CORBA, PortableServer
import CosNaming, Guarda, Guarda__POA

# Local Imports
import guard_client

guard_client = guard_client.bind()

class Guard(Guarda__POA.Guard):
    visitors = 0

    def warns_guard(self, msg):
        if msg == "entered":
            self.visitors += 1

        elif msg == "exited":
            self.visitors -= 1

    def get_visitors(self):
        return self.visitors

    def is_night(self):
        if self.visitors > 0:
            guard_client.ring_bell()
        self.visitors = 0
    

# Inicializa o ORB e procura o root POA
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

# Cria uma instância de Guard e uma referência da instância
ei = Guard()
eo = ei._this()

# Obtém uma referência para o root Naming Service
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print("Failed to narrow the root naming context")
    sys.exit(1)

# Vincula o contexto ao root context
try:
    # Os parâmetros podem ser qualquer string, mas devem ser iguais em todas as 
    # implementações de servidores
    name = [CosNaming.NameComponent("Guard Server", "context")]
    context = rootContext.bind_new_context(name)
    print("New context bounded: Guard Server")

except CosNaming.NamingContext.AlreadyBound, ex:
    obj = rootContext.resolve(name)
    context = obj._narrow(CosNaming.NamingContext)
    
    if context is None:
        print("Context exists but is not a NamingContext")
        sys.exit(1)
    
# Vincula o objeto da linha 29 ao contexto
try:
    name = [CosNaming.NameComponent("Guard", "Object")]
    context.bind(name, eo)

except CosNaming.NamingContext.AlreadyBound:
    context.rebind(name, eo)

# Ativa o POA
poaManager = poa._get_the_POAManager()
poaManager.activate()

# Bloqueia o processo infinitamente (ou até o ORB ser desligado)
orb.run()