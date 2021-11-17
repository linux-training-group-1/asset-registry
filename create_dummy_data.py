import itertools

asset_names = ["Cisco 3000", "Cisco 5000", "Cisco 7000", "Cisco 8000"]
descriptions = ["2 integrated 10/100/1000 Ethernet ports",
                "2 enhanced High-Speed WAN Interface Card slots that can host 2 single wide or 1 double wide and 1 "
                "single wide (e)HWIC",
                "1 Internal Services1 Internal Services Module slot",
                "Fully integrated power distribution to modules supporting 802.3af Power over Ethernet (PoE) and "
                "Cisco Enhanced PoE",
                "Security Embedded hardware-accelerated VPN encryption",
                "Secure collaborative communications with Group Encrypted Transport VPN, Dynamic Multipoint VPN, "
                "or Enhanced Easy VPN",
                "Integrated threat control using Cisco IOS Firewall, Cisco IOS Zone-Based Firewall, Cisco IOS IPS, "
                "and Cisco IOS Content Filtering",
                "Identity management that uses authentication, authorization, and accounting (AAA), and public key "
                "infrastructure"]
owners = ["Nimal", "Kamala", "Saman", "Alice", "Jhon"]
locations = ["1st floor", "corner office", "2nd floor", "basement", "rooftop"]
criticality = ['Critical', 'Medium', 'Low']

string = "INSERT INTO asset_app.asset (name, owner, description, location, criticality) values "
for combination in itertools.product(asset_names, owners, descriptions, locations, criticality):
    # print(combination)
    string += str(combination)+"," + "\n"
string = string[:-2]
string += ";"
file = open("inserts.sql", "w")
file.write(string)
