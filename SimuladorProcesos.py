#Simulador de procesos con Simpy
#Yasmin Chavez 16101
#Samantha Duarte 16256
#28/02/2017

import random
import simpy
import time

#t0 = time.clock()

def esteProceso (nombre, env, CPU, espacioRAM):
    global totalDia
    
    velocidadProc = 1
    numInstrucc = 6
    valida = True
    instruccPorRealizar = random.expovariate(0.1/1)
    memoriaActual = random.randint(1,10)
    
    
    while (valida):
        if capacidadMemoria.level >= memoriaActual:
            yield capacidadMemoria.get(memoriaActual)
            print ('%s ya entro a memoria RAM' % nombre)
            valida = False
        else:
            print('%s esta esperando RAM' % nombre)
            valida = False
            
    #Verificar que hayan procesos faltantes
    
    inicio = env.now
    print ('%s ya esta ready' % nombre)
    with CPU.request() as turno:
        yield turno
        print ('%s ya entro al procesador' % nombre)
        while(instruccPorRealizar >= numInstrucc):
            yield env.timeout(velocidadProc)
            instruccPorRealizar = instruccPorRealizar - numInstrucc
            if (instruccPorRealizar > 1):
                num = random.randint(1,2)
            else:
                break
            if (num == 1):
                print ('%s entro a waiting' % nombre)
                yield env.timeout(velocidadProc)
            print ('%s ya esta ready' % nombre)
        print ('%s ya ha salido del procesador' % nombre)
            
        tiempoTotal = env.now - inicio
        totalDia = totalDia + tiempoTotal
        print inicio
        print ('%s Terminated' % nombre)
        print ('memoria RAM: %d' %memoriaActual)
        yield capacidadMemoria.put(memoriaActual)
    
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
capacidadMemoria = simpy.Container(env, 200, init=10)
random.seed(10)
 
totalDia = 0
for i in range (200):
    env.process(esteProceso('Proceso %d' % i, env, CPU , capacidadMemoria))

env.run()

print ("Tiempo promedio es: "), totalDia/200
