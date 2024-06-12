from ansible_runner import run
from celery import shared_task
import logging,json
from datetime import datetime,timedelta
import logging
from cis.models import HostConfig
from django.conf import settings
from cis.utils import convert_json_to_csv
from django.conf import settings
import os
from django.db import transaction

from cis.sendmail import send_mail



def fetch_latest_json_file(ip_address,scan_type):
    host_lication=settings.ANISBLE_PLAYBOOK_AUDIT_DIR+'/'+ip_address+'/'
    list_of_files=os.listdir(host_lication)
    list_of_files = [i for i in list_of_files if (scan_type in i and i.endswith(".json"))]
    list_of_files.sort(reverse=True)
    return list_of_files[0]

@shared_task
def anisblerunner(host_id,operation,playbook_path,private_data_dir,**karags):
    host_obj=HostConfig.objects.get(id=host_id)
    if operation == 1:
        scan_type = 'pre_scan'
    elif operation == 2:
        scan_type = 'post_scan'

    inventory = {
                "targets": {
                    "hosts": {
                    host_obj.ip_address: {
                        "ansible_user": host_obj.username,
                        "ansible_ssh_pass": host_obj.password,
                        "ansible_host": host_obj.ip_address
                    }
                }
            }
        }
    
    extravars={
        "ansible_user": host_obj.username,
        "ansible_ssh_pass": host_obj.password,
    }
    
    options = {
        'playbook': playbook_path, ## PLayBook Path
        'private_data_dir': private_data_dir,   ## Artifiact Holder
        'rotate_artifacts': 1,  
        'inventory':inventory,              ## Inventory Path
        'extravars':extravars
    }
    r = run(**options)
    print("status of playbook:",r.status)
    if r.status in ['successful']:
        file_name=fetch_latest_json_file(ip_address=host_obj.ip_address,scan_type=scan_type)
        csv_file_name = file_name.replace('json','csv')
        json_path=settings.ANISBLE_PLAYBOOK_AUDIT_DIR+'/'+host_obj.ip_address+'/'+file_name
        csv_path=settings.ANISBLE_PLAYBOOK_AUDIT_DIR+'/'+host_obj.ip_address+'/'+csv_file_name
        field_names = ["title","skipped","summary-line","successful","err"]
        convert_json_to_csv(json_path=json_path,csv_path=csv_path,field_names=field_names)
        send_mail(host_obj.created_by.email,host_obj.created_by.username,csv_path,csv_file_name)
        host_obj.status = HostConfig.COMPLETED
        host_obj.save()
        return True
    else:
        host_obj.status = HostConfig.FAILED
        host_obj.save()
        return

    


# host_id=5
# playbook_path = './cis_playbook.yml'
# private_data_dir = '../cis'
# inventory_path = './inventory.ini'

# anisblerunner(host_id,playbook_path,inventory_path,private_data_dir)
