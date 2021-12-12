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
