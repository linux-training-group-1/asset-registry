import itertools
import random

"""
Create dummy data for the asset application
"""
asset_names = ["Cisco ", "Samsung ", "Asuz ", "Dialog "]
descriptions = ["2 integrated 10/100/1000 Ethernet ports",
                "2 enhanced High-Speed WAN Interface Card slots that can host 2 single wide or 1 double wide and 1 "
                "Single wide (e)HWIC",
                "1 Internal Services1 Internal Services Module slot",
                "Fully integrated power distribution to modules supporting 802.3af Power over Ethernet (PoE) and "
                "Cisco Enhanced PoE",
                "Security Embedded hardware-accelerated VPN encryption",
                "Secure collaborative communications with Group Encrypted Transport VPN, Dynamic Multipoint VPN, "
                "Enhanced Easy VPN",
                "Integrated threat control using Cisco IOS Firewall, Cisco IOS Zone-Based Firewall, Cisco IOS IPS, "
                "Cisco IOS Content Filtering",
                "Identity management that uses authentication, authorization, and accounting (AAA), and public key "
                "infrastructure something"]
owners = ["Bob", "Kamala", "Saman", "Alice", "John"]
locations = ["1st floor", "corner office", "2nd floor", "basement", "rooftop"]
criticality = ['Critical', 'Medium', 'Low']

string = "INSERT INTO asset_db.asset (name, owner, description, location, criticality) values "
for combination in itertools.product(owners, descriptions, locations, criticality):
    new_ins = str(combination) + "," + "\n"
    new_ins = new_ins[:1] + "'" + random.choice(asset_names) + str(int(random.random() * 1000000)) + "', " + new_ins[1:]
    string += new_ins
string = string[:-2]
string += ";"
# print(string)
file = open("inserts.sql", "w")
file.write(string)
