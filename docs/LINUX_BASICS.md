# 📚 Linux Basics Cheatsheet

## Essential Commands

### Navigation
```bash
pwd                 # Print Working Directory - where am I?
ls                  # List files and directories
cd <path>          # Change Directory
cd ..              # Go to parent directory
cd ~               # Go to home directory
ls -la             # List all files including hidden (starts with .)
ls -lh             # List with human-readable sizes
find / -name "file"  # Find file anywhere
```

### File Operations
```bash
cat <file>         # Print file contents
less <file>        # View file with pagination
head -n 10 <file>  # First 10 lines
tail -f <file>     # Last lines (follow = watch in real-time)
cp <source> <dest> # Copy
mv <source> <dest> # Move/Rename
rm <file>          # Delete file
rm -r <dir>        # Delete directory recursively
touch <file>       # Create empty file
mkdir <dir>        # Create directory
mkdir -p a/b/c     # Create nested directories
```

### Viewing & Searching
```bash
grep "text" <file>      # Search for text in file
grep -r "text" .        # Search recursively
grep -i "text" <file>   # Case-insensitive search
wc -l <file>            # Count lines
sort <file>             # Sort lines
uniq <file>             # Remove duplicates (must be sorted first)
diff file1 file2        # Show differences
```

### File Permissions
```bash
ls -l                    # Show permissions
chmod 755 script.sh      # Change permissions (755 = rwxr-xr-x)
chmod +x script.sh       # Make executable
chmod -x script.sh       # Remove executable
chown user:group file    # Change owner
chown -R user:group dir  # Change owner recursively

# Permission reference:
# r (read)    = 4
# w (write)   = 2
# x (execute) = 1
# So: 755 = 7(4+2+1 owner) 5(4+1 group) 5(4+1 others)
```

### Users & Permissions
```bash
whoami                          # Current user
id                              # User ID and groups
sudo <command>                  # Run as superuser
sudo su                         # Become superuser (root)
sudo useradd <username>         # Add user
sudo userdel <username>         # Delete user
sudo passwd <username>          # Change password
groups <username>               # Show user's groups
sudo usermod -aG docker $USER   # Add user to group
```

### System Information
```bash
uname -a                # System information
lsb_release -a         # Linux distribution
df -h                  # Disk space usage
du -sh .               # Current directory size
free -h                # Memory usage
top                    # Running processes (interactive)
ps aux                 # List all processes
ps aux | grep python   # Find specific process
htop                   # Better version of top (install first)
```

### Networking
```bash
ifconfig               # Network interfaces (deprecated, use ip)
ip addr                # Show IP addresses
ping google.com        # Test connectivity
curl http://example.com    # Make HTTP request
wget http://example.com/file  # Download file
netstat -tuln          # Show listening ports
ss -tuln               # Modern version of netstat
ssh user@host          # SSH into remote server
scp file user@host:/path  # Copy file over SSH
```

### Process Management
```bash
ps aux                 # List processes
kill <PID>            # Terminate process
kill -9 <PID>         # Force kill process
pkill -f "process_name"  # Kill by name
fg                    # Bring background job to foreground
bg                    # Continue process in background
jobs                  # List background jobs
nohup command &       # Run command immune to hangups
```

## Advanced Operations

### Pipes & Redirection
```bash
>                    # Redirect output to file (overwrite)
>>                   # Append output to file
<                    # Redirect input from file
|                    # Pipe output to another command
2>                   # Redirect errors
&>                   # Redirect both output and errors
```

### Examples
```bash
ls -la > output.txt               # Save listing to file
cat file1 file2 > combined.txt    # Combine files
grep "error" logfile >> errors.log # Append errors
ls -la | grep ".txt"              # Find .txt files
cat file | head -20 | tail -10    # Lines 11-20
```

### Text Processing
```bash
sed 's/old/new/g' file           # Replace text (s = substitute)
sed '1,5d' file                  # Delete lines 1-5
awk '{print $1}' file            # Print first column
awk -F: '{print $1}' /etc/passwd # Print first field (: separator)
cut -d: -f1 /etc/passwd          # Cut fields
tr 'a-z' 'A-Z' < file            # Convert to uppercase
```

### Archiving
```bash
tar -czf archive.tar.gz folder/    # Create gzipped tar
tar -xzf archive.tar.gz             # Extract
zip -r archive.zip folder/          # Create zip
unzip archive.zip                   # Extract zip
```

## Essential Directories

```bash
/home/<user>        # User home directory
/root               # Root user's home
/home/<user>/.ssh   # SSH keys location
/etc                # Configuration files
/var/log            # Log files
/tmp                # Temporary files
/opt                # Optional software
/usr/local/bin      # User-installed executables
/opt/docker         # Docker installation
```

## Practical Examples

### Check if service is running
```bash
ps aux | grep nginx
# or
systemctl status nginx
```

### Show real-time log
```bash
tail -f /var/log/syslog
```

### Find large files
```bash
find / -type f -size +100M -exec ls -lh {} \;
```

### Count files
```bash
find . -type f | wc -l
```

### Monitor system in real-time
```bash
watch -n 1 'free -h && df -h'
```

### Create user with specific shell
```bash
sudo useradd -m -s /bin/bash newuser
```

### List open ports
```bash
sudo netstat -tlnp
# or
sudo ss -tlnp
```

---

**📖 Next**: Learn Bash scripting in `BASH_GUIDE.md`
