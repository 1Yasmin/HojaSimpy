#Simulador de procesos con Simpy
#Yasmin Chavez 16101
#Samantha Duarte 16256
#28/02/2017

import random
import simpy
import time

t0 = time.clock()

def esteProceso (nombre, env, CPU, espacioRAM):
    
    velocidadProc = 1
    numInstrucc = 3
    valida = True
    instruccPorRealizar = random.expovariate(0.1/10)
    memoriaActual = random.randint(1,10)
    while (valida):
        if capacidadMemoria.level >= memoriaActual:
            yield capacidadMemoria.get(memoriaActual)
            print ('%s ya entro a memoria RAM' % nombre)
            valida = False
        else:
            print('%s esta esperando RAM' % nombre)
            yield env.timeout(1)
            
    #Verificar que hayan procesos faltantes
    while (instruccPorRealizar > 1):
        print ('%s ya esta ready' % nombre)
        with CPU.request() as turno:
                yield turno
                print ('%s ya entro al procesador' % nombre)
                for i in range(numInstrucc):
                    yield env.timeout(velocidadProc)
                    if (instruccPorRealizar <= 1):
                        break
                    else:
                        instruccPorRealizar = instruccPorRealizar - 1
                print ('%s ya ha salido del procesador' % nombre)
        if (instruccPorRealizar > 1):
            num = random.randint(1,2)
            if (num == 1):
                print ('%s entro a waiting' % nombre)
                yield env.timeout(1)
    
    print ('%s Terminated' % nombre)
    print ('memoria RAM: %d' %memoriaActual)
    yield capacidadMemoria.put(memoriaActual)
    
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
capacidadMemoria = simpy.Container(env, 100, init=10)
random.seed(10)

for i in range (10):
    env.process(esteProceso('Proceso %d' % i, env, CPU , capacidadMemoria))
env.run()

print time.clock()-t0
