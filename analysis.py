#!/usr/bin/env python3
# coding: utf-8

import telebot
TOKEN = "5250015281:AAFTBzBg88RzREeIFgD98RmvYP-sN7WOwqI"
CHAT_ID = "5184387598"



import numpy as np
import scipy.interpolate as interpolate
from scipy.optimize import curve_fit
import os, sys
import subprocess
import matplotlib.pyplot as plt

# Метка, чтобы отправлять результаты в телеграмм
TG = False
if len(sys.argv)>1:
    if sys.argv[1]=='--telegram':
        TG = True
        bot = telebot.TeleBot(TOKEN)
        bot.send_message(CHAT_ID, "Скрипт постпроцессинга:")


def sendImage(name):
    global TG
    if TG:
        bot.send_photo(CHAT_ID, open(name, 'rb'))

def sendText(string, value=None, dim=""):
    if value == None:
        valueStr = ""
    else:
        valueStr = " "+str(value)+" "+dim
    
    global TG
    if TG:
        bot.send_message(CHAT_ID, str(string)+valueStr)
    else:
        print(str(string)+valueStr)
        




#volume = 2.968174e-04
#rho_init = 1.029018851
#methanC = 0.0549
#methanMass = methanC * rho_init * volume
#print(methanMass)
#Qall = methanMass * Hu

#dT = Qall/(1000*1.510786e+01 * volume)

#print(dT)



# Загрузка результатов постпроцессинга опенфоам

raw = np.loadtxt('postProcessing/spark/0/volFieldValue.dat', skiprows = 4, encoding = 'utf8')

t = raw[:,0]
T = raw[:,1]
CH4 = raw[:,2]



raw = np.loadtxt('postProcessing/cylinder/0/volFieldValue.dat', skiprows = 4, encoding = 'utf8')

p_c = raw[:,1]
T_c = raw[:,2]
CH4_c = raw[:,3] 
CO_c = raw[:,4]
k_c = raw[:,5]
omega_c = raw[:,6]

raw = np.loadtxt('postProcessing/probes/0/p', skiprows = 5, encoding = 'utf8')

p1 = raw[:,1]
p2 = raw[:,2]
p3 = raw[:,3]
p4 = raw[:,4]

#print(np.diff(p1)/np.diff(t))

raw = np.loadtxt('postProcessing/probes/0/T', skiprows = 5, encoding = 'utf8')

T1 = raw[:,1]
T2 = raw[:,2]
T3 = raw[:,3]
T4 = raw[:,4]


raw = np.loadtxt('postProcessing/integr/0/volFieldValue.dat', skiprows = 4, encoding = 'utf8')

M = raw[:,1] # кг
H = raw[:,2] # Дж
CH4mass = raw[:,3] # кг

# Вычисление кривой тепловыделения
Hu = 50.1e6
xi = 1
x = (H - H[0])/( xi * Hu * CH4mass[0] )
# Вычисление производной
w = np.empty(len(t))
w.fill(1)
w[0] = 30
w[-1] = 30
xSpline  = interpolate.UnivariateSpline(t, x, w=w, s=0.1, ext='const')
dxdt = xSpline.derivative()
# Апроксимация по вибе
def x_Vibe(t, Kc, tz, m, dt):
    return 1 - np.exp(- Kc * (np.maximum(t-dt,0)/tz)**(m+1))
def dx_Vibe(t, Kc, tz, m, dt):
    return  - np.exp(- Kc * (np.maximum(t-dt,0)/tz)**(m+1)) * ( - Kc *(m+1)* (np.maximum(t-dt,0)/tz)**(m+1-1) ) /tz

popt, pcov = curve_fit(x_Vibe, t, x, bounds=([6, 0, 1, 0], [8, 1, 10, 0.1]))
sendText("Апроксимация параметров по Вибе (Kc, tz, m, dt)")
print(   "===============================")
sendText(str(popt))


# Построение графиков

fig, axs = plt.subplots(3)
fig.set_size_inches(5, 8, forward=True)
fig.suptitle('Зона искры')
axs[0].set_ylabel('Шаг по времени, с')
axs[0].plot(t[:-1], np.diff(t), color ="pink")
axs[1].set_ylabel('Температура, К')
axs[1].plot(t[:-1], T[:-1], color ="red")
axs[2].set_ylabel('Концентрация метана, - ')
axs[2].plot(t[:-1], CH4[:-1], color ="blue")
fig.savefig("result1.png")
sendImage("result1.png")

fig2, axs2 = plt.subplots(7)
fig2.set_size_inches(5, 15, forward=True)
fig2.suptitle('Цилиндр')
axs2[0].set_ylabel('Давление, Па')
axs2[0].plot(t, p_c, color ="green")
axs2[1].set_ylabel('Температура, К')
axs2[1].plot(t, T_c, color ="red")
axs2[2].set_ylabel('Концентрация метана (неправильная), - ')
axs2[2].plot(t, CH4_c, color ="blue")
axs2[2].set_ylim(0, 0.06)
axs2[3].set_ylabel('Концентрация CO (неправильная), - ')
axs2[3].plot(t, CO_c, color ="red")
axs2[4].set_ylabel('Кин.энерг.турб')
axs2[4].plot(t, k_c, color ="red")
axs2[5].set_ylabel('Омега')
axs2[5].plot(t, omega_c, color ="red")
axs2[6].set_ylabel('Среднепотолочная u`')
axs2[6].plot(t, np.sqrt(2*k_c), color ="magenta")

fig2.savefig("result2.png")
sendImage("result2.png")


fig3, axs3 = plt.subplots(3)
fig3.set_size_inches(5, 8, forward=True)
fig3.suptitle('Датчики')
axs3[0].set_ylabel('Давление, Па')
axs3[0].plot(t, p1, t, p2, t, p3, t, p4, color ="green")
axs3[1].set_ylabel('Температура, К')
axs3[1].plot(t, T1, t, T2, t, T3, t, T4, color ="red")
axs3[2].set_ylabel('Производная температуры, К/с')
axs3[2].plot(t[:-1], np.diff(T1)/np.diff(t), 
             t[:-1], np.diff(T2)/np.diff(t), 
             t[:-1], np.diff(T3)/np.diff(t), 
             t[:-1], np.diff(T4)/np.diff(t), 
             color ="aqua")

fig3.savefig("result3.png")
sendImage("result3.png")



fig4, axs4 = plt.subplots(3)
fig4.set_size_inches(5, 9, forward=True)
fig4.suptitle('Тепловыделение')
axs4[0].set_ylabel('x, -')
axs4[0].plot(t, x, color ="purple", label="raw")
axs4[0].plot(t, xSpline(t), color ="red", label="spline")
axs4[0].plot(t, x_Vibe(t, *popt),'g--', color ="black", label="vibe")
axs4[0].legend()
axs4[1].set_ylabel('dx/dt, -')
axs4[1].plot(t[:-1], np.diff(x)/np.diff(t), color ="purple", label="rawdiff")
axs4[1].plot(t, dxdt(t), color ="red", label="splinediff")
axs4[1].plot(t, dx_Vibe(t, *popt),'g--', color ="black", label="vibe")
axs4[1].legend()
axs4[2].set_ylabel('CH4, кг')
axs4[2].set_ylim(0, CH4mass[0]*1.2)
axs4[2].plot(t, CH4mass, color ="purple")


fig4.savefig("result4.png")
sendImage("result4.png")



# Постпроцессинг

sendText( "Изменение массы в процессе расчета", 100*(np.max(M) - np.min(M))/M[0], "%" )

sendText("Определение скоростей распространения пламени")
print("=============================================")

L_between_probes = np.sqrt(0.015**2 + 0.00336**2)
print("Растояние между соседними датчиками "+str(L_between_probes))

t1_front = t[np.argmax(np.diff(T1)/np.diff(t))]
t2_front = t[np.argmax(np.diff(T2)/np.diff(t))]
t3_front = t[np.argmax(np.diff(T3)/np.diff(t))]
t4_front = t[np.argmax(np.diff(T4)/np.diff(t))]

print("Проход фронта температуры через первый датчик "+str(t1_front))
print("Проход фронта температуры через второй датчик "+str(t2_front))
print("Проход фронта температуры через третий датчик "+str(t3_front))
print("Проход фронта температуры через чтвртй датчик "+str(t4_front))

sendText("Скорости по соседним датчикам 1-2, 2-3, 3-4:")
sendText(L_between_probes/(t2_front-t1_front))
sendText(L_between_probes/(t3_front-t2_front))
sendText(L_between_probes/(t4_front-t3_front))
sendText("Скорость от подачи искры до 1 датчика:", L_between_probes/(t1_front-1e-05), "м/с")
sendText("Скорость от подачи искры до 4 датчика:", 4*L_between_probes/(t4_front-1e-05), "м/с")
sendText("(Примечание. Согласно Agrawal1981 ламинарная скорость пламени в стехиометрическом метане при исходных 1 атм 323 К составляет 0,3290 - 0,3359 м/с)")
sendText("(Примечание. Согласно Shy2000 турбулентная скорость пламени в стехиометрическом метане при исходных 298 К составляет 2,3 м/с при пульсациях 1 м/с; 4 м/с при пульсациях 4 м/с и далее не растет)")

if not(TG):
    plt.show()
