import csv

# Assigning the respective names to the protocol numbers
protocol_names = {"1":"icmp", "6":"tcp", "17": "udp"} 

# Adding the contents of the lookup_table.csv into a dictionary
lookup_table = {}

with open ("lookup_table.csv", "r") as lookup_file:
    read = csv.DictReader(lookup_file)

    for row in read:
        dstport = row["dstport"].strip()  #removing extra spaces using strip function
        protocol = row["protocol"].strip() #removing extra spaces using strip function
        tag = row.get("tag")
        if tag is not None:
            tag = tag.strip() #removing extra spaces using strip function
        else:
            tag = ""  # empty string if tag is missing
        lookup_table[(dstport, protocol)] = tag #using (dstport, protocol) as key and tag as the value

counts_tag = {} # storing key as the tag and value as the count of their occurence

dstport_protocol_counts = {} # storing key as (dstport, protocol) and value as the count of their occurence

untagged = 0 # counting logs with no matching tags

with open("sample_flow_logs.txt", "r") as flow_log_file:
    
    for line in flow_log_file:
        parts = line.strip().split() # breaking the entire line into smaller parts
        if len(parts) < 8:
            continue # skipping the line that do not have enough fields
        
        dstport = parts[5] # we have the dstport at index 5
        protocol_num = parts[7] # we have the protocol at index 7
        protocol = protocol_names.get(protocol_num, "") # we map the protocol number to the respective name

        if protocol == "":
            continue # skipping this line if the protocol is  not supported

        key = (dstport, protocol)

        # counting the occurence of each port and protocol
        if key in dstport_protocol_counts:
            dstport_protocol_counts[key] += 1
        else: 
            dstport_protocol_counts[key] = 1

        # checking we get a combination with matching tag
        if key in lookup_table:
            tag = lookup_table[key]
            if tag in counts_tag:
                counts_tag[tag] += 1
            else: 
                counts_tag[tag] = 1
        else:
            untagged += 1 # incrementing the count of untagged variable if no tag is found

# writing the results into an output file named output.txt        
with open("output.txt", "w") as output_file:
    output_file.write("Tag Counts:\n")
    output_file.write("Tag, Count\n")
    for tag, count in counts_tag.items():
        output_file.write(f"{tag}, {count}\n")
    output_file.write(f"Untagged,{untagged}\n")

    output_file.write("\nPort/Protocol Combination Counts:\n") #we add a blank line before usin \n at the beginning
    output_file.write("Port, Protocol, Count\n")
    for (port, protocol), count in dstport_protocol_counts.items():
        output_file.write(f"{port},{protocol},{count}\n")