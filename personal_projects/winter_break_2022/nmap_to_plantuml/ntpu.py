#!/usr/bin/python3

# Imports (might cleanup in future, like just get the needed imports from argparse/nmap/requests)
import argparse
import nmap
import requests
from zlib import compress
from base64 import b64encode



def main():
    """
    Main function to run everything
    :return: None
    """
    # Gather args into a variable
    arguments = args()

    print(f"[Running nmap scan against {arguments.TargetIPAddress}]")
    # Run NMAP, returns list (0=scan,1=scan_time)
    nmap_output = runnmap(arguments)

    print(f"[Converting scan into UML]")
    # Run planuml conversion
    toplanuml(nmap_output[0],nmap_output[1],arguments)

    pass



def args():
    """
    A function to gather arguments for parsing
    :return: args: Populated namespace of argument values
    """
    # Setup basic parser
    arg_parser = argparse.ArgumentParser(
        prog="ntpu",
        description="NmapToPlanUml (NTPU) is a command line program that runs nmap to create visual diagrams of a network via PlanUML"
    )

    # Add arguments
    arg_parser.add_argument(
     "-I","--OutputUML",
     help="Filename to store UML code"
    )

    arg_parser.add_argument(
     "-S","--Server",
     help="HTTP/s address of self hosted PlanUML server, Example: http://localhost:8080 (MUST CONTAIN NO '/' AT THE END)"
    )


    arg_parser.add_argument(
        "-O","--OutputAscii",
        action="store_true",
        help="Enable sending UML code to PlanUML servers and return ASCII art of scanned computers"
    )

    arg_parser.add_argument(
        "TargetIPAddress",
        metavar="IP",
        nargs="+",
        help="The IP address/es of the host/s you wish to scan. Input separated with a space, and can make use of input ranges from NMAP ('-' and CIDR notation). Example: 192.168.0.1 192.168.0.2 192.168.0.5-10 192.168.0.1/23"
        )

    # Parse the arguments then return objects
    args = arg_parser.parse_args()

    return args



def runnmap(args):
    """
    A function that runs nmap
    :param: Populated namespace of argument values
    :return: Json formatted results of nmap
    """
    # Take the list of target ips from arguments and join them
    ipaddrs = " ".join(args.TargetIPAddress)
    nm = nmap.PortScanner()
    # Scan the results, clean them, then return
    scan_results = cleanscan(nm.scan(hosts=ipaddrs))

    return scan_results



def cleanscan(scan):
    """
    A function to cleanup nmap scan results with default nmap console settings
    :param: scan: Dict of raw nmap scan results
    :return: results: List with clean nmap scan results/scan timers
    """
    # Parse the scan and gather values from certain keys for planuml formatting
    clean_results = scan['scan']
    scan_time = scan['nmap']['scanstats']

    results = [clean_results,scan_time]

    return results


def toplanuml(nmap_json,scan_time,args):
    """
    A function to convert Dict formmatted results of nmap into planuml
    :param: nmap_json: Dict formmatted nmap scan results
    :param: scan_time: Dict of formmated nmap scan time results
    :param: args: Populated namespace of argument values
    :return: None
    """

    # Create a string of beginning uml code
    uml_code=f"""@startuml
!define osaPuml https://raw.githubusercontent.com/Crashedmind/PlantUML-opensecurityarchitecture2-icons/master
!include osaPuml/Common.puml
!include osaPuml/User/all.puml
!include osaPuml/Hardware/all.puml
!include osaPuml/Misc/all.puml
!include osaPuml/Server/all.puml
!include osaPuml/Site/all.puml
allowmixing

title Scan results:
legend
Scanned IPs: {scan_time['totalhosts']} in {scan_time['elapsed']} seconds
| Uphosts: {scan_time['uphosts']}, Downhosts: {scan_time['downhosts']}, Totalhosts: {scan_time['totalhosts']}|
end legend

left footer {scan_time['timestr']}

object self {{
    <$osa_desktop>
}}
frame "Uphosts" {{\n"""

    # For each host in the json
    for num, host in enumerate(nmap_json.keys()):
        # Determine hostname (whether or not nmap collected one)
        if nmap_json[host]['hostnames'][0]['name'] != '':
            hostname = nmap_json[host]['hostnames'][0]['name']
        else:
            hostname = host
        ###
        
        # Handling ports
        total_ports = []
        open_ports = []
        
        # Append each port with its port and name in a certain format to a list, if it is also open, append that to another list
        try:
            # Need this in try and except as if the system has no tcp ports open, will yield error
            for port in nmap_json[host]['tcp'].keys():
                total_ports.append(f"{port}/{nmap_json[host]['tcp'][port]['name']}")

                if nmap_json[host]['tcp'][port]['state'] == 'open':
                    open_ports.append(f"{port}")
        except Exception:
            pass
        ###

        # From data above, generate a object with information collected from nmap (ports are the joining of the entire list with commas)
        uml_code += f"""object "{hostname}" as {num} {{
                <$osa_server>
                status = {nmap_json[host]['status']['state']}\n
                IPs = {nmap_json[host]['addresses']}
                total_ports/services = {','.join(total_ports)}
                open_ports = {','.join(open_ports)}
                }}
                self <--> {num}\n"""

    # Standard end of formatting
    uml_code += f"@enduml"
    
    # Compress the uml code
    compressed_uml = planuml_encode(uml_code)


    # Argument selection stuff
    # If outputuml has value, then record uml code to file
    if args.OutputUML:
        try:
            with open(args.OutputUML, "w") as output_file:
                output_file.write(uml_code)
            print(f"Output saved in: {args.OutputUML}")
        except Exception as e:
            print(e)
    
    # If self hosted option is selected, set the uml_link to whatever it is, if not, default to plantuml.com
    if args.Server:
        uml_link = f"{args.Server}"
    else:
        uml_link = f"https://www.plantuml.com/plantuml"

    # If outputascii flag is set, output generated ascii art
    if args.OutputAscii:
        # r = requests.get(f"https://www.plantuml.com/plantuml/txt/~h{compressed_uml}")
        # r = requests.get(f"https://www.plantuml.com/plantuml/txt/{compressed_uml}")
        r = requests.get(f"{uml_link}/txt/{compressed_uml}")
        print(r.text)
    
    # print(f"Link to the generated scan on PlanUML: https://www.plantuml.com/plantuml/uml/~h{compressed_uml}")
    # print(f"Link to the generated scan on PlanUML: https://www.plantuml.com/plantuml/uml/{compressed_uml}")
    print(f"Link to the generated scan on PlanUML: {uml_link}/uml/{compressed_uml}")



def planuml_encode(planuml_data):
    """
    A function to encode planuml data, heavily inspired by https://github.com/dougn/python-plantuml/blob/master/plantuml.py
    :param: planuml_data: String of planuml input
    :return: String of compressed values
    """
    # Take UML, encode with UTF-8, convert bytes to hex
    # encoded_uml = planuml_data.encode('utf-8').hex()

    # Establish base64 and planuml character mapping encoded in utf-8
    b64_mapping = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".encode('utf-8')
    planuml_mapping = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_".encode('utf-8')

    # Compress the data, encode in utf-8, strip headers and checksum
    compressed_uml = compress(planuml_data.encode('utf-8'))[2:-4]

    # Create a mapping table of replacing b64 with planuml
    b64_planuml_mapping = compressed_uml.maketrans(b64_mapping, planuml_mapping)

    # Encode the compression with base64, translate it with the mapping, decode the utf-8
    encoded_uml = b64encode(compressed_uml).translate(b64_planuml_mapping).decode('utf-8')

    # Return compressed UML
    return encoded_uml

# Check whether importing (__name__ will equal import name) or run itself (will have "__main__" value)
if __name__ == "__main__":
    main()
