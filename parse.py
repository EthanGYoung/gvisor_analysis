import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import json
import csv
import os
import re

output_data = open('./result.csv', 'w')
output_writer = csv.writer(output_data)

test_env = ["bare","runc","runsc_ptrace","runsc_kvm"]
#email_list = ["pzhu6@wisc.edu","eyoung8@wisc.edu"]
email_list = ["eyoung8@wisc.edu"]
def write_csv_import_spinup(curr_queue,current_dir, lines, start_index):
    output_writer.writerow([])
    output_writer.writerow(['Parsing file: %s' % current_dir])
    output_writer.writerow([])
    test_env_index = start_index;
    output_writer.writerow([test_env[test_env_index]])
    for i in range(0, len(lines)):
        line = lines[i]
        if "LOG_OUTPUT: " in line:
            curr_time = re.findall(r"[-+]?\d*\.\d+|\d+", line)[0]
            curr_queue.append(curr_time)
        if line.isspace() and curr_queue:
            output_writer.writerow(curr_queue)
            curr_queue = []
            output_writer.writerow([])
            test_env_index = test_env_index + 1
            if test_env_index <=3:
                output_writer.writerow([test_env[test_env_index]])

def write_csv_execute_lifecycle(curr_queue,current_dir, lines):
    output_writer.writerow([])
    output_writer.writerow(['Parsing file: %s' % current_dir])
    output_writer.writerow([])
    for i in range(0, len(lines)):
        line = lines[i]
        if "Executing: " in line:
            output_writer.writerow([line.rstrip("\n")+" in seconds"])
        if "LOG_OUTPUT: " in line:
            num_array = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            curr_time = num_array[len(num_array)-1]
            curr_queue.append(curr_time)
        if line.isspace() and curr_queue:
            output_writer.writerow(curr_queue)
            curr_queue = []
            output_writer.writerow([])

# Parsing
rootDir = 'logs/'
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        current_dir = dirName+"/"+fname
        curr_queue = []
        with open(current_dir) as f:
            lines = f.readlines()

            # Import
            if "import" in current_dir:
                write_csv_import_spinup(curr_queue,current_dir,lines,0,)
                continue
            # Spinup
            if "spinup" in current_dir:
                write_csv_import_spinup(curr_queue,current_dir,lines,1)
                continue

            write_csv_execute_lifecycle(curr_queue,current_dir,lines)

output_data.close()

# Create multipart msg object
msg = MIMEMultipart()
msg['Subject'] = 'The contents of result.csv'
fp = open("result.csv", 'r')
ctype, encoding = mimetypes.guess_type("result.csv")
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)
attachment = MIMEBase(maintype, subtype)
attachment.set_payload(fp.read())
fp.close()
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename="result.csv")
msg.attach(attachment)

# Send the message via our own SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login("gvisoranalysis@gmail.com", "gvisoranalysis123")
server.sendmail("gvisoranalysis@gmail.com", email_list, msg.as_string())
server.quit()
