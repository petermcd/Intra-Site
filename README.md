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

## .env File

A .env file is required in the root of the Django project with the following content.

```bash
DJANGO_SECRET_KEY=dummy
DJANGO_DEBUG=0
DJANGO_DATABASE_HOST=dummy
DJANGO_DATABASE_PORT=3306
DJANGO_DATABASE=dummy
DJANGO_DATABASE_USER=dummy
DJANGO_DATABASE_PASSWORD=dummy
```

## Settings

### CLOUDFLARE_API_KEY

This is the API key for the Cloudflare API. The user requires read access on the zone and read/write on the DNS.

### GOOGLE_BOOKS_API_URL

The base URL for the Google Books API

### GOOGLE_MAPS_KEY

The API key for the Google API

### SNMP_PASSWORD

Shared SNMP password that will be used by all devices

### SNMP_USERNAME

Shared SNMP username that will be used by all devices

### ZABBIX_PASSWORD

Password for the API user

### ZABBIX_URL

The full URL that Zabbix monitoring platform is hosted on

### ZABBIX_USERNAME

API user for Zabbix, this requires admin rights

Running the following command will create the necessary keys:

```bash
python manage.py loaddata settings
```

## Zabbix Templates

### 

This enables the monitoring of the Asustor NAS drive, there are pitfalls (such as fetching system temperature in 
fahrenheit but reporting it as celsius) and will require replacing

[Template SNMP Asustor NAS](https://share.zabbix.com/unsorted/template-snmp-asustor-nas)
