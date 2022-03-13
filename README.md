# How to install

For the books section a shared folder to the nas drive is required. The following sets this up (but need to replace
the local path with the correct path)

```bash
sudo apt update
sudo apt install nfs-common

mkdir /home/pi/Intra-Site/downloads/

sudo mount 192.168.0.5:/volume1/Web/ebooks /home/pi/Intra-Site/downloads/books
sudo mount 192.168.0.5:/volume1/Web/event-tickets /home/pi/Intra-Site/downloads/event-tickets
sudo mount 192.168.0.5:/volume1/Web/travel-tickets /home/pi/Intra-Site/downloads/travel-tickets
sudo mount 192.168.0.5:/volume1/Web/documents /home/pi/Intra-Site/downloads/documents
```

## TODO

### Stop duplicate records

When adding a new . record it creates a new one instead of updating the existing

### Slow DNS

Updating DNS on the fly is slow, probably better to add a task queue

### Books

When a book is deleted the file should be deleted
When clear is selected on a model it should delete the file
If a file exists and the ISBN changes the filename should change
If a file uses the title if the title changes it should change the filename

## Development tools

### Watcham

Watchman is a manual install, instructions can be found [HERE](https://facebook.github.io/watchman/docs/install.html)

on top of this, pywatchman is required and can be installed using the dev requirements

### Django Debug toolbar

Installation instructions can be found [HERE](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

### Git Pre Commit

Git pre commit runs tests prior to a commit occuring, this helps reduce CICD failures. To set this up
the following commands can be carried out:

```bash
pip install pre-commit
pre-commit install
```
