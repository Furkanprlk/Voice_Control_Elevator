import time
from multiprocessing import Process


import listener



def listenRes(res):
    print(res)
    kat=0
    kilit=False
    tamamla=False
    for veri in res:
        print(veri)
        if kilit==False:
            if veri=="zemin":
                kat=0
                kilit=True
                print("zemin")
            if veri=="birinci":
                kat+=1
                kilit=True
                print("birinci")
            if veri=="ikinci":
                kat+=2
                kilit=True
                print("ikinci")
            if veri=="üçüncü":
                kat+=3
                kilit=True
                print("üçüncü")
            if veri=="dördüncü":
                kat+=4
                kilit=True
                print("dördüncü")
            if veri=="beşinci":
                kat+=5
                kilit=True
                print("beşinci")
            if veri=="altıncı":
                kat+=6
                kilit=True
                print("altıncı")
            if veri=="yedinci":
                kat+=7
                kilit=True
                print("yedinci")
            if veri=="sekizinci":
                kat+=8
                kilit=True
                print("sekizinci")
            if veri=="dokuzuncu":
                kat+=9
                kilit=True
                print("dokuzuncu")
        if veri=="on":
            kat+=10
            print("on")
        if veri=="yirmi":
            kat+=20
            print("yirmi")
        if veri=="otuz":
            kat+=30
            print("otuz")
        if veri=="kırk":
            kat+=40
            print("kırk")
        if veri=="elli":
            kat+=50
            print("elli")
        if veri=="atmış" or veri=="altmış":
            kat+=60
            print("altmış")
        if veri=="yetmiş":
            kat+=70
            print("yetmiş")
        if veri=="seksen":
            kat+=80
            print("seksen")
        if veri=="doksan":
            kat+=90
            print("doksan")
        if veri=="kat" or "kaç":
            tamamla=True
        if tamamla and kilit:
            print("Seçilen Kat:" + str(kat))

if __name__=="__main__":
    procs = []
    proc = Process(target=listener.listen, args=(listenRes,))  # instantiating without any argument
    procs.append(proc)
    proc.start()
    count=0
    