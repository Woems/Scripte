#!/usr/bin/python
######################################################
# Bandbreitenmonitor fuer die Fritzbox
#    ...und mein erstes Programm in Python
#
# D.Ahlgrimm 03.2012
######################################################
from Tkinter import *        # python-tk-2.7.2-7.1.3.i586 oder python-tk-2.7.2-7.5.1.x86_64
from SOAPpy import SOAPProxy # python-soappy-0.12.0-11.1.noarch

fillmode=1                # auf 1 fuer ausgefuellte Kurven, 0 fuer einfache Kurven
splitmode=1               # auf 1 fuer zwei einzelne Kurven, 0 fuer ueberlagerte Kurven
fritzbox="fritz.box"  # IP der Fritzbox

werte_r=[] # Messwert-Liste initialisieren
werte_s=[]
for a in range(400):
   werte_r.append(0)
   werte_s.append(0)

# Liefert den Betrag der bisher empfangenen Bytes von der Fritzbox
def getRec():
   return long(SOAPProxy(proxy='http://' + fritzbox + ':49000/upnp/control/WANCommonIFC1', 
               namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 
               soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetTotalBytesReceived',
               noroot=True).GetTotalBytesReceived())

# Liefert den Betrag der bisher gesendeten Bytes von der Fritzbox
def getSnd():
   return long(SOAPProxy(proxy='http://' + fritzbox + ':49000/upnp/control/WANCommonIFC1',
               namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 
               soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetTotalBytesSent',
               noroot=True).GetTotalBytesSent())

# Liefert die maximale Empfangs-Bandbreite der Fritzbox
# z.B.   1275000   fuer ca. 138 KB/s ( (1275000/1024) /9 )
def getMaxRec():
   d=SOAPProxy(proxy='http://' + fritzbox + ':49000/upnp/control/WANCommonIFC1', 
               namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 
               soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetCommonLinkProperties',
               noroot=True).GetCommonLinkProperties()
   return long(d.NewLayer1DownstreamMaxBitRate)

# Liefert die maximale Sende-Bandbreite der Fritzbox
# z.B.   222000   fuer ca. 24 KB/s ( (222000/1024) /9 )
def getMaxSnd():
   d=SOAPProxy(proxy='http://' + fritzbox + ':49000/upnp/control/WANCommonIFC1', 
               namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 
               soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetCommonLinkProperties',
               noroot=True).GetCommonLinkProperties()
   return long(d.NewLayer1UpstreamMaxBitRate)


# Maximalwerte holen
maxRec=getMaxRec()/9216 # 9216=1024*9 also "Bit/Sek" zu "KiloByte/Sek"
maxSnd=getMaxSnd()/9216

# aktuell uertragene Bytes holen
rec1=getRec()
snd1=getSnd()

root = Tk()
root.title("FritzBox Bandbreitenmonitor")
c = Canvas(width=400, height=100, bg='#CCCCCC')
c.pack()
for xx in range(0, 100, 25):
   a = c.create_line(0, xx, 400, xx, fill='green')
for xx in range(400, 0, -60):
   a = c.create_line(xx, 0, xx, 100, fill='green')

c.create_text(20, 10, fill='blue', text=maxRec)
if splitmode==1:
   c.create_text(20, 85, fill='red', text=maxSnd)
else:
   c.create_text(20, 30, fill='red', text=maxSnd)


def sek(): # ruft sich 1x pro Sekunde auf
   global werte_r, werte_s
   global lnr, lns
   global rec1, rec2, snd1, snd2

   # aktuell uertragene Bytes holen
   rec2=getRec() # Wert2 liegt zeitlich eine Sekunde nach Wert1
   snd2=getSnd() # ... Wert2 - Wert1 ergibt also die in der letzten Sekunde uebertragenen Bytes

   # neuen Messwert an die letzten drei Werte angleichen und rechts in die Anzeige-Liste reinschieben
#   nvr=(werte_r[397] + werte_r[398] + werte_r[399] + ((rec2-rec1)/1024))/4
   nvr=(werte_r[399] + ((rec2-rec1)/1024))/2
   werte_r.pop(0)
   werte_r.append(nvr)
#   nvs=(werte_s[397] + werte_s[398] + werte_s[399] + ((snd2-snd1)/1024))/4
   nvs=(werte_s[399] + ((snd2-snd1)/1024))/2
   werte_s.pop(0)
   werte_s.append(nvs)
   print "Empfang:", nvr, "KB/Sek      Senden:", nvs, "KB/Sek"

   # umkopieren fuer den naechsten Durchlauf
   rec1=rec2
   snd1=snd2

   c.delete(lnr) # alte Kurve loeschen
   c.delete(lns)

   arr_r=[]
   arr_s=[]
   for xx in range(400): # neue Kurve aufbauen
      arr_r.append(xx)
      if splitmode==1:
         arr_r.append(75-((werte_r[xx]*75)/maxRec))
      else:
         arr_r.append(100-((werte_r[xx]*100)/maxRec)) # der Y-Wert wird gemaess maximaler Bandbreite skaliert
      if fillmode==1:
         arr_r.append(xx)
         if splitmode==1:
            arr_r.append(75)
         else:
            arr_r.append(100)
      arr_s.append(xx)
      if splitmode==1:
         arr_s.append(100-((werte_s[xx]*25)/maxSnd))
      else:
         arr_s.append(100-((werte_s[xx]*100)/maxSnd))
      if fillmode==1:
         arr_s.append(xx)
         arr_s.append(100)

   lnr=c.create_line(arr_r, fill='blue') # neue Kurve darstellen
   lns=c.create_line(arr_s, fill='red')

   c.update()
   root.after(1000, sek)


lnr=c.create_line(1, 1, 1, 1, fill='black') # anlegen, um es in sek() delete'n zu koennen
lns=c.create_line(1, 1, 1, 1, fill='black')

root.after(1, sek)
#root.geometry("400x100+1200+1050")  # unten links bei 1600x1200
root.geometry("400x100+3429+1045")  # unten links bei 1600x1200
root.mainloop()


