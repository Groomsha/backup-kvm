# backup-kvm

########################################################

Automatic launch of Backup via Cron (command: crontab -e) version Python 3.6.*

30 23 * * FRI    /root/backup/mainapp.py -setings_name_json=/root/backup/setings.json

setings.json:

"type": 1 - backup vm lvm, 2 - backup vm img, 3 - restore vm lvm, 4 - restore vm img,

"compression": compression .gz 1 or 9

"size_snap": default=2 is 512M Snapshot for VMs less than 16Gb

"number_archives": do not overwrite the latest 1 - 9 archives

########################################################