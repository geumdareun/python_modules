#The object lexicographically iterates all MAC addresses of the form 'OUI:NIC' for NIC in the inclusive range [NIC_START, 'FF:FF:FF'].

class mac_address_iterator:
    
    # OUI = Organizationally Unique Identifier
    # NIC = Network Interface Controller
    
    def __init__(self, OUI = "84:25:3f", NIC_START = "00:00:00"):
        self.prev_index = sum([int(NIC_START.split(":")[k],16)<<(8*(2-k)) for k in range(3)]) - 1
        self.OUI = OUI
    
    def has_next(self):
        return self.prev_index < 0xFFFFFF

    def next(self):
        self.prev_index+=1
        return "%s:%s"%(self.OUI,":".join(["%02x"%((self.prev_index>>(8*(2-k)))&0xFF) for k in range(3)]))

def change_mac_address(interface, mac_address):
    os.system("sudo ifconfig %s down" % (interface))
    os.system("sudo ifconfig %s hw ether %s" % (interface, mac_address))
    os.system("sudo ifconfig %s up" % (interface))

