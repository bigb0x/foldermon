""""
# foldermon

version: 1.0

Author: Mohamed Ali (https://twitter.com/MohamedNab1l)

foldermon.py will monitor the changes to pre-defined Linux directories for any changes and then sends an email alerts with the new changes. 

Feel free to contact me if you do have any questions or suggestions.
"""
import os
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# Email configurations
smtp_server = 'mail.yourserver.com'
smtp_port = 587
smtp_username = 'youremail@yourserver.com'
smtp_password = 'yourpassword'
sender_name = 'FolderMon'
sender_email = 'sender@yourserver.com'
receiver_email = 'youremail@yourserver.com'

# Linux folder to monitor
#folders = ['/path/to/folder1', '/path/to/folder2']
folders_to_monitor = ['/tmp/foldermon', '/tmp/foldermon2']

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def send_email(folder_path, prev_folder_size, curr_folder_size, latest_file, latest_mod_time):
    message = MIMEText("Folder " + folder_path + " has been modified\n\n" +
                           "Previous folder size: " + str(prev_folder_size) + "\n" +
                           "Current folder size: " + str(folder_size) + "\n" +
                           "Modified time: " + {latest_mod_time.strftime('%b %d, %Y %H:%M:%S')} + "\n" +
                           "Latest modified file: " + latest_file + "\n")
    


    message += f"The latest modified file is {latest_file}, modified on {latest_mod_time.strftime('%b %d, %Y %H:%M:%S')}."
    message['From'] = formataddr((sender_name, sender_email))
    message['To'] = receiver_email
    message['Subject'] = "Folder " + folder_path + " has been modified"
# Send email using SMTP
    try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully")
    except Exception as e:
            print("An error occurred while sending the email:", e)
    finally:
        try:
                server.quit()
        except:
            pass

prev_folder_sizes = {}

while True:
    for folder_path in folders_to_monitor:
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist.")
            continue
        if folder_path not in prev_folder_sizes:
            prev_folder_sizes[folder_path] = get_folder_size(folder_path)
            continue
        curr_folder_size = get_folder_size(folder_path)
        if curr_folder_size != prev_folder_sizes[folder_path]:
            latest_file = max(os.listdir(folder_path), key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
            latest_mod_time = time.localtime(os.path.getmtime(os.path.join(folder_path, latest_file)))
            send_email(folder_path, prev_folder_sizes[folder_path], curr_folder_size, latest_file, latest_mod_time)
            prev_folder_sizes[folder_path] = curr_folder_size
    time.sleep(60)
