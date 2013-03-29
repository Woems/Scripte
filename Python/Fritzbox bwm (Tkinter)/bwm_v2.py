#!/usr/bin/python
######################################################
# Bandbreitenmonitor fuer die Fritzbox
#    ...und mein erstes Programm in Python
#
# D.Ahlgrimm 03.2012
# Conky -Edition von Bob 05.2012
######################################################
#http://www.ip-phone-forum.de/showthread.php?t=246673

from Tkinter import *        # python-tk-2.7.2-7.1.3.i586 oder python-tk-2.7.2-7.5.1.x86_64
from SOAPpy import SOAPProxy # python-soappy-0.12.0-11.1.noarch
import time
import sys
import os


######################################################
#        Konfiguration und Optionen 
######################################################

# IP der Fritzbox
routerIP = 'fritz.box'

#### Asgabe-Methode 1, 2, 3 oder 4 waehlen
style = 1

## Methode 1: grafische Ausgabe der Werte in einem kleinen Fenster
## Das Original von D.Ahlgrimm

## Methode 2: komplette Ausgabe der Werte mit Balken in Textform - schnell, simpel und retro :)
"""Die folgende Zeile gehoert in die Conky-Konfigurationsdatei
${exec ~/.conky/router_traffic.py}
"""
## Methode 3: direkte Auswertung des Python-Skripts in Conky - relativ langsam, Skript muss jeweils fuer jede Variable durchlaufen
"""Die folgenden vier Zeilen gehoeren in die Conky-Konfigurationsdatei
Down: ${exec ~/.conky/router_traffic.py | sed -n 1p}
${execbar ~/.conky/router_traffic.py | sed -n 3p}
Up: ${exec ~/.conky/router_traffic.py | sed -n 2p}
${execbar ~/.conky/router_traffic.py | sed -n 4p}
"""
## Methode 4: schnelle, stabile Auswertung - Umweg ueber eine "Vermittlungs-Datei", Python-Skript schreibt die Werte in eine Textdatei, Conky liest die Werte aus
"""Die folgenden fuenf Zeilen gehoeren in die Conky-Konfigurationsdatei
${exec ~/.conky/router_traffic.py}
Down: ${exec cat ~/.conky/router_traffic_tmp | sed -n 1p}
${execbar cat ~/.conky/router_traffic_tmp | sed -n 3p}
Up: ${exec cat ~/.conky/router_traffic_tmp | sed -n 2p}
${execbar cat ~/.conky/router_traffic_tmp | sed -n 4p}
"""
#### *optional: Nur fuer die Asgabe-Methode Nr. 1
fillmode = 1		# auf 1 fuer ausgefuellte Kurven, 0 fuer einfache Kurven
splitmode = 1		# auf 1 fuer zwei einzelne Kurven, 0 fuer ueberlagerte Kurven
window_width = 350	# Breite des Fensters
window_height = 110 	# Hoehe des Fensters
position_x = 1200 	# Z.B.1200 und 1050 fuer unten links bei 1600x1200
position_y = 1050
update_interval = 1000 	# Graph wird alle 1000 ms aktualisiert
gui_downl_color = 'blue' # Download-Graph-Farbe
gui_upl_color = 'red' 	# Upload-Graph-Farbe
gui_bg = '#1C1C1C' 	# Hintergrund-Farbe
split_dl = 75 		# Prozentwert des Teiles fuer den Download-Graphen
split_up = 25 		# Prozentwert des Teiles fuer den Upload-Graphen
show_gui_max_values = True # Max-Bandbreiten-Werte zeigen (True oder False)
show_gui_traffic_values = True # Traffic zeigen (True oder False)
gui_grid_color = '#777777' # Farbe der stylischen Hintergrund-Linien
grid_lines_x = 6 	# Hintergrund-Linien-Aufteilung: Horizontale Unterteilung, ein Segment entspricht 10 Sekunden. 
grid_lines_y = 4 	# Vertikale Unterteilung. Ein viertel ist immer gut, und siegt auch gut aus


#### IP-Adresse ausgeben (True oder False)
showIP = True
## bei Methode 1: IP wird als Fenstertitel angezeigt
## Conky:
"""Die Zeile gehoert in die Conky-Konfigurationsdatei
## bei Methode 2: 
WAN IP: ${exec ~/.conky/router_traffic.py | sed -n 5p}
## bei Methode 3: 
WAN IP: ${exec cat ~/.conky/router_traffic_tmp | sed -n 5p}
"""

#### *optional:  Progress-Balken-Optionen - Dies sind die Balken aus Methode Nr. 2
# mehr Infos unter http://code.activestate.com/recipes/577871/
custom_options = {
    'end': 100,		# Max. Prozentwert
    'width': 37,	# Breite
    'fill': '-',	# Fuellungs-Zeichen
    'blank': '.',	# Leer-Stellen-Zeichen
    'format': '[%(fill)s|%(blank)s]' # Augabemuster
    }

#### *optional: Pfad zum home-Verzeichnis des Benutzers. Nur fuer die Asgabe-Methode Nr. 4
homefolder = os.path.expanduser('~')
conky_path = '.conky' # Conky Verzeichnis im Benutzerordner
temp_file_name = 'router_traffic_tmp' # Name der "Vermittlungs-Textdatei"


#### Methode zur Berechnung des Traffics. Nur aendern, falls man keine Werte erhaelt
# 1 = schnelle Methode
# 2 = langsame Methode
traffic_method = 1

#### Textbausteine fuer moegliche Uebersetzung
text_download = "Down:\t"
text_upload = "Up:\t"
text_WAN_IP = "WAN IP:"
text_kibs = "KiBs"
text_mibs = "MiBs"
text_max_dl = "Max"
text_max_ul = "Max"
gui_title="FritzBox Bandbreitenmonitor"
text_debug1 = "OK"
text_debug2 = "Error: Your Computer is connected with the router.\nBut can't connect to the web.\nMaybe some problems with your bad ISP or with hardware/cable?"
text_debug3 = "Error: Oh noo! No connection to the router... Check the IP settings!"
######################################################
#        Ende der Konfiguration und Optionen
######################################################


# Liefert die maximale Empfangs-Bandbreite der Fritzbox
# z.B.   1275000   fuer ca. 138 KB/s ( (1275000/1024) /9 )
def getMaxRec():
   d=SOAPProxy(proxy='http://' + routerIP + ':49000/upnp/control/WANCommonIFC1', 
               namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 
               soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetCommonLinkProperties',
               noroot=True).GetCommonLinkProperties()
   return long(d.NewLayer1DownstreamMaxBitRate)

# Liefert die maximale Sende-Bandbreite der Fritzbox
# z.B.   222000   fuer ca. 24 KB/s ( (222000/1024) /9 )
def getMaxSnd():
   d=SOAPProxy(proxy='http://' + routerIP + ':49000/upnp/control/WANCommonIFC1', 
               namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 
               soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetCommonLinkProperties',
               noroot=True).GetCommonLinkProperties()
   return long(d.NewLayer1UpstreamMaxBitRate)

# Liefert den Betrag der bisher empfangenen Bytes von der Fritzbox
def getRec():
    return long(SOAPProxy(proxy='http://' + routerIP + ':49000/upnp/control/WANCommonIFC1',
    namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1',
    soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetTotalBytesReceived',
    noroot=True).GetTotalBytesReceived())

# Liefert den Betrag der bisher gesendeten Bytes von der Fritzbox
def getSnd():
    return long(SOAPProxy(proxy='http://' + routerIP + ':49000/upnp/control/WANCommonIFC1',
    namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1',
    soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetTotalBytesSent',
    noroot=True).GetTotalBytesSent())

# Liefert die Down- und Up-Empfangsrate in Bytes
def getTrafficAI():
    d=SOAPProxy(proxy='http://' + routerIP + ':49000/upnp/control/WANCommonIFC1',
    namespace='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1',
    soapaction='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetAddonInfos',
    noroot=True).GetAddonInfos()
    return (d.NewByteReceiveRate,d.NewByteSendRate)
    #getTraffic()[0] ist Download,  getTraffic()[1] ist Upload

# externe IP auslesen
def getExternalIP():
    return str(SOAPProxy(proxy='http://' + routerIP + ':49000/upnp/control/WANCommonIFC1',
	      namespace='urn:schemas-upnp-org:service:WANIPConnection:1',
	      soapaction='urn:schemas-upnp-org:service:WANIPConnection:1#GetExternalIPAddress',
	      noroot=True).GetExternalIPAddress())

# Verbindungs-Status
def getStatus():
	d=SOAPProxy(proxy='http://' + routerIP + ':49000/upnp/control/WANDSLLinkC1',
	namespace='urn:schemas-upnp-org:service:WANDSLLinkConfig:1',
	soapaction='urn:schemas-upnp-org:service:WANDSLLinkConfig:1#GetDSLLinkInfo',
	noroot=True).GetDSLLinkInfo()
	return d.NewLinkStatus

# Verbindungs-Status pruefen
def checkConnection():
    if getStatus() == 'Up' or 'Down' or 'Initializing':
	status = 1
	debug = text_debug1 # 'OK'
    elif getStatus() == 'Unavailable':
	status = 2
	debug = text_debug2 # 'maybe some router/hardware problems?'
    elif getStatus() !=  'Up' or 'Down' or 'Initializing' or 'Unavailable':
	status = 3
	debug = text_debug3 # 'check IP settings!'
    return status, debug

    
# Traffic auslesen und errechnen
def getTraffic():
    if traffic_method == 1:
	return getTrafficAI()
	#getTraffic()[0] ist Download,  getTraffic()[1] ist Upload
	  
    else:
	# Alternative Methode zur Berechnung des Traffics
	def getTraffic():
    
	    # aktuell uebertragene Bytes holen
	    rec1=getRec()
	    snd1=getSnd()
	    
	    time.sleep(1)  # Delay in Sekunden
	    
	    # neuere uebertragene Bytes holen
	    rec2=getRec() # Wert2 liegt zeitlich eine Sekunde nach Wert1
	    snd2=getSnd()
	    
	    # Differenz zwischen dem alten Messwert u.d. neuen Messwert = aktueller Traffic
	    tr_down = (rec2-rec1)
	    tr_up = (snd2-snd1)
	    return tr_down, tr_up # Werte in Tupling und Bytes
	    #getTraffic()[0] ist Download,  getTraffic()[1] ist Upload
	return getTraffic()


## {{{ http://code.activestate.com/recipes/577871/ (r1)
class ProgressBar(object):
    """ProgressBar class holds the options of the progress bar.
    The options are:
        start   State from which start the progress. For example, if start is 
                5 and the end is 10, the progress of this state is 50%
        end     State in which the progress has terminated.
        width   --
        fill    String to use for "filled" used to represent the progress
        blank   String to use for "filled" used to represent remaining space.
        format  Format
        incremental
    """
    def __init__(self, start=0, end=10, width=12, fill='=', blank='.', format='[%(fill)s>%(blank)s] %(progress)s%%', incremental=True):
        super(ProgressBar, self).__init__()

        self.start = start
        self.end = end
        self.width = width
        self.fill = fill
        self.blank = blank
        self.format = format
        self.incremental = incremental
        self.step = 100 / float(width) #fix
        self.reset()

    def __add__(self, increment):
        increment = self._get_progress(increment)
        if 100 > self.progress + increment:
            self.progress += increment
        else:
            self.progress = 100
        return self

    def __str__(self):
        progressed = int(self.progress / self.step) #fix
        fill = progressed * self.fill
        blank = (self.width - progressed) * self.blank
        return self.format % {'fill': fill, 'blank': blank, 'progress': int(self.progress)}

    __repr__ = __str__

    def _get_progress(self, increment):
        return float(increment * 100) / self.end

    def reset(self):
        """Resets the current progress to the start point"""
        self.progress = self._get_progress(self.start)
        return self


# Maximalwerte holen
maxRec=getMaxRec()/9 # "Bit/Sek" zu "Kibibyte/Sek"
maxSnd=getMaxSnd()/9


# Werte automatisch in Kibibyte/Sek oder Mebibyte/Sek
def kbmb(x):
    x = int(x)
    if x < 900*1024: # ab 900 Kibibyte wird in Mebibyte angezeigt
      value = x/1024 # Umrechnung Bytes in Kibibyte
      value_suffix = text_kibs
    else:
      value = (float(x))/1048576 # Umrechnung Bytes in Mebibyte
      value_suffix = text_mibs
      value=round(value, 2) # Runden auf zwei Nachkomma-Stellen
    return value, value_suffix
    #kbmb()[0] entspricht dem Augabewert
    #kbmb()[1] ist der Suffix KiBs / MiBs


# Ausgabewahl
def Output(method):
    if method == 1:
	guiOutput()
    elif method == 2:
	retroOutput()
    elif method == 3:
	compactOutput()
    elif method == 4:
	fileOutput()


# Asgabe-Methode 1
def guiOutput():
    global werte_r, werte_s
    global lnr, lns, dltr, ultr
    
    werte_r=[] # Messwert-Liste initialisieren
    werte_s=[]
    for a in range(window_width):
	werte_r.append(0)
	werte_s.append(0)

    # Maximalwerte holen
    maxRecK=maxRec/1024 #"KiloByte/Sek"
    maxSndK=maxSnd/1024

    root = Tk()
    if showIP == True:
	gui_title=text_WAN_IP + ' ' + getExternalIP()
    root.title(gui_title)
    c = Canvas(width=window_width, height=window_height, bg=gui_bg)
    c.pack()
    
    split_height_dl=int((window_height*split_dl)/100) # Prozentwerte fuer optionale Split-Teilbereiche werden uebergeben
    split_height_ul=int((window_height*split_up)/100)
    
    # Die stylischen Hintergrund-Linien werden gezeichnet, was waere das Programm nur ohne dieres Linien ;)
    for xx in range(0, window_height, window_height/grid_lines_y):
	a = c.create_line(0, xx, window_width, xx, fill=gui_grid_color)
    for xx in range(window_width, 0, window_width/grid_lines_x*-1):
	a = c.create_line(xx, 0, xx, window_height, fill=gui_grid_color)
 
    if show_gui_max_values == True:
	# Textausgabe im GUI mit Max-Werten
	gui_text_max_dl_x=45
	gui_text_max_dl_y=10
	gui_text_max_ul_x=45
	gui_text_max_ul_y=10
	gui_text_max_ul_split_x=45
	gui_text_max_ul_split_y=split_height_dl+10
	
	c.create_text(gui_text_max_dl_x, gui_text_max_dl_y, fill=gui_downl_color, text=text_max_dl + ' '+ str(kbmb(maxRec)[0]) + str(kbmb(maxRec)[1]))
	if splitmode==1:
	    c.create_text(gui_text_max_ul_split_x, gui_text_max_ul_split_y, fill=gui_upl_color, text=text_max_ul + ' '+ str(kbmb(maxSnd)[0]) + str(kbmb(maxSnd)[1]))
	else:
	    c.create_text(gui_text_max_ul_x, gui_text_max_ul_y, fill=gui_upl_color, text=text_max_ul + ' '+ str(kbmb(maxSnd)[0]) + str(kbmb(maxSnd)[1]))


    def sek(): # ruft sich im bestimmten Intervall auf
      global werte_r, werte_s
      global lnr, lns, dltr, ultr

      # Traffic-Werte holen
      traffic = getTraffic()  # traffic[0] ist Download,  traffic[1] ist Upload
      nvr=int(traffic[0])/1024 # Download in KiB
      nvs=int(traffic[1])/1024 # Upload in KiB
      
      # Messwerte der Liste hinzufuegen
      werte_r.pop(0)
      werte_r.append(nvr)	
      werte_s.pop(0)
      werte_s.append(nvs)
      
      c.delete(lnr) # alte Kurve loeschen
      c.delete(lns)
      c.delete(dltr,ultr)
      
      arr_r=[]
      arr_s=[]
      for xx in range(window_width): # neue Kurve aufbauen
	  arr_r.append(xx)
	  if splitmode==1:
	    arr_r.append(split_height_dl-((werte_r[xx]*split_height_dl)/maxRecK))
	  else:
	    arr_r.append(window_height-((werte_r[xx]*window_height)/maxRecK)) # der Y-Wert wird gemaess maximaler Bandbreite skaliert
	  if fillmode==1:
	    arr_r.append(xx)
	    if splitmode==1:
		arr_r.append(split_height_dl)
	    else:
		arr_r.append(window_height)
	  arr_s.append(xx)
	  if splitmode==1:
	    arr_s.append(window_height-((werte_s[xx]*split_height_ul)/maxSndK))
	  else:
	    arr_s.append(window_height-((werte_s[xx]*window_height)/maxSndK))
	  if fillmode==1:
	    arr_s.append(xx)
	    arr_s.append(window_height)

      lnr=c.create_line(arr_r, fill=gui_downl_color) # neue Kurve darstellen
      lns=c.create_line(arr_s, fill=gui_upl_color)
      
      # Textausgabe der Traffic-Werte
      show_text_dl = str(kbmb(traffic[0])[0]) + ' ' + str(kbmb(traffic[0])[1]) # Textteile zusammenbacken
      show_text_ul = str(kbmb(traffic[1])[0]) + ' ' + str(kbmb(traffic[1])[1])
      # Textausgabe der Traffic-Werte im GUI 
      if show_gui_traffic_values == True: 
	  # Koordinaten fuer Textausgabe im GUI
	  gui_text_dl_x=window_width-50
	  gui_text_dl_y=10
	  gui_text_ul_x=window_width-60
	  gui_text_ul_y=10
	  gui_text_ul_split_x=window_width-50
	  gui_text_ul_split_y=split_height_dl+10
	  dltr=c.create_text(gui_text_dl_x, gui_text_dl_y, fill=gui_downl_color, text=show_text_dl)
	  if splitmode==1:
	      ultr=c.create_text(gui_text_ul_split_x, gui_text_ul_split_y, fill=gui_upl_color, text=show_text_ul)
	  else:
	      ultr=c.create_text(gui_text_ul_x, gui_text_ul_y, fill=gui_upl_color, text=show_text_ul)
	
      # Textausgabe der Traffic-Werte im Terminal
      #print "Empfang:", nvr, "KB/Sek      Senden:", nvs, "KB/Sek"
      print text_download, show_text_dl, '\t\t',text_upload, show_text_ul # Augabewert in KiBs/MiBs mit Suffix     
      c.update()
      root.after(update_interval, sek)

    lnr=c.create_line(1, 1, 1, 1, fill='black') # anlegen, um es in sek() delete'n zu koennen
    lns=c.create_line(1, 1, 1, 1, fill='black')
    dltr=c.create_text(1, 1, fill=gui_upl_color, text=' ')
    ultr=c.create_text(1, 1, fill=gui_upl_color, text=' ')

    root.after(1, sek)
    window_size = str(window_width) + 'x' + str(window_height) + '+' + str(position_x) + '+' + str(position_y) # Werte fuer Fenstergroesse werden uebergeben
    root.geometry(window_size)
    root.mainloop()


# Asgabe-Methode 2
def retroOutput():
    traffic = getTraffic()  # traffic[0] ist Download,  traffic[1] ist Upload
    
    # Prozentwert des Traffics
    dwn_percent=int((float(traffic[0])/maxRec)*100)
    up_percent=int((float(traffic[1])/maxSnd)*100)

    if (dwn_percent or up_percent) > 100: # pruefen ob Wert ueber 100%
	return retroOutput()        
    else: 
	dwn_bar = ProgressBar(**custom_options) + dwn_percent # Download-Progress-Balken
	up_bar = ProgressBar(**custom_options) + up_percent # Upload-Progress-Balken

	print text_download, kbmb(traffic[0])[0], kbmb(traffic[0])[1]	 # Augabewert KiBs/MiBs mit Suffix
	print dwn_bar, int(dwn_percent),"\b%" # Download-Progress-Balken und Prozentwert
	print text_upload, kbmb(traffic[1])[0], kbmb(traffic[1])[1] # Augabewert KiBs/MiBs mit Suffix
	print up_bar, int(up_percent),"\b%" # Upload-Progress-Balken und Prozentwert
	if showIP == True:
	    print text_WAN_IP, getExternalIP()


# Asgabe-Methode 3
def compactOutput():
    traffic = getTraffic()  # traffic[0] ist Download,  traffic[1] ist Upload
    
    # Prozentwert des Traffics
    dwn_percent=int((float(traffic[0])/maxRec)*100)
    up_percent=int((float(traffic[1])/maxSnd)*100)

    if (dwn_percent or up_percent) > 100: # pruefen ob Wert ueber 100%
	return compactOutput()        
    else:
	print kbmb(traffic[0])[0], kbmb(traffic[0])[1] # Download-Traffic
	print kbmb(traffic[1])[0], kbmb(traffic[1])[1] # Upload-Traffic
	print dwn_percent # Download-Prozent
	print up_percent # Upload-Prozent
	if showIP == True:
	    print getExternalIP()


# Asgabe-Methode 4
def fileOutput():
    tr_temp_file_path = homefolder + '/' + conky_path + '/' + temp_file_name # Pfad zur der Textdatei wird gebildet
    
    traffic = getTraffic()  # traffic[0] ist Download,  traffic[1] ist Upload

    # Prozentwert des Traffics
    dwn_percent=int((float(traffic[0])/maxRec)*100)
    up_percent=int((float(traffic[1])/maxSnd)*100)

    if (dwn_percent or up_percent) > 100: # pruefen ob Wert ueber 100%
	return fileOutput()        
    else:
	fobj = open(tr_temp_file_path, "w")
	# Download-Traffic
	# Upload-Traffic
	# Download-Prozent
	# Upload-Prozent
	print >> fobj, kbmb(traffic[0])[0], kbmb(traffic[0])[1]
	print >> fobj, kbmb(traffic[1])[0], kbmb(traffic[1])[1]
	print >> fobj, dwn_percent
	print >> fobj, up_percent
	if showIP == True:
	    print >> fobj,  getExternalIP()
	fobj.close()

    
# Ausgabe-Start
if checkConnection()[0] == 1:
    Output(style)
else:
    print checkConnection()[1]