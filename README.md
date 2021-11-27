# How to install

For the books section a shared folder to the nas drive is required. The following sets this up (but need to replace
the local path with the correct path)

```bash
sudo apt update
sudo apt install nfs-common

sudo mount 192.168.0.5:/volume1/Web/ebooks /path/to/ebooks/folder
```

## TODO

### Books

When a book is deleted the file should be deleted
When clear is selected on a model it should delete the file
If a file exists and the ISBN changes the filename should change
If a file uses the title if the title changes it should change the filename
