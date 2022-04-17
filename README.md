# Intranet

## How to install

For the books section a shared folder to the nas drive is required. The following sets this up (but need to replace
the local path with the correct path)

```bash
sudo apt update
sudo apt install nfs-common

mkdir /home/pi/Intra-Site/SiteDocuments/

sudo mount 192.168.0.5:/volume1/SiteDocuments /home/pi/Intra-Site/SiteDocuments/
```

## TODO

### Monzo
Reimplement Monzo integration.

## Development tools

### Watcham

Watchman is a manual install, instructions can be found [HERE](https://facebook.github.io/watchman/docs/install.html)

on top of this, pywatchman is required and can be installed using the dev requirements

### Django Debug toolbar

Installation instructions can be found [HERE](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

### Git Pre Commit

Git pre commit runs tests prior to a commit occurring, this helps reduce CICD failures. To set this up
the following commands can be carried out:

```bash
pip install pre-commit
pre-commit install
```
