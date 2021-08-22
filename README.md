# Intra Site

This is a basic intranet site that I have that will have the following functionality:

## Network Topology

A topology of my network including hostnames, IP's and the connections between devices.

## Finances

A breakdown of my finances, these include monthly bills and outstanding debts.
The debts also include a run down of how many payments will be required (currently assumes
a monthly payment)

## Service Links

Links too services that I run on the local network

# Install Requirements

## Settings

### CLOUDFLARE_API_KEY

This is the API key for the Cloudflare API. The user requires read access on the zone and read/write on the DNS.

### ZABBIX_URL

The full URL that Zabbix monitoring platform is hosted on

### ZABBIX_USERNAME

API user for Zabbix, this requires admin rights

### ZABBIX_PASSWORD

Password for the API user

### SNMP_USERNAME

Shared SNMP username that will be used by all devices

### SNMP_PASSWORD

Shared SNMP password that will be used by all devices

## Zabbix Templates

### 

This enables the monitoring of the Asustor NAS drive, there are pitfalls (such as fetching system temperature in 
fahrenheit but reporting it as celsius) and will require replacing

[Template SNMP Asustor NAS](https://share.zabbix.com/unsorted/template-snmp-asustor-nas)
