py_dar_backup
=============================

This script allows you to backup selective directories to CD/DVD using (Disk Archiver)[http://dar.linux.free.fr/]. It works by creating a custom dar command, executing the command and burning each dar file to CD / DVD. It allows you to selectively ignore directories that contain a file (by default it looks for a file called .nobackup), which is helpful if you have some large files in selective directories that you dont wish to backup.

