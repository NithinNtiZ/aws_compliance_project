import boto3
from datetime import datetime, timezone, timedelta
import sys , time, threading
import pyfiglet
import mysql.connector

instance_id = None
current_time = datetime.now(timezone.utc)

db_name = "grafana_aws"
db_table_name = "instance_data"


lenth = list(enumerate(sys.argv))
try:
    for index, argument in lenth:
        if argument == "-i":
            instance_id = sys.argv[index+1]
        if argument == "-d":
            extend_days= int(sys.argv[index+1])
except Exception as e:
    print(e)
    sys.exit()


# Replace with your desired VPC settings
region = 'ap-southeast-1'

# Create a Boto3 client for EC2
ec2 = boto3.client('ec2', region_name=region)

# Get a list of all AWS regions
ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

def Script_header():
    t = "INFOBLOX SUPPORT LAB"
    ASCII_art_1 = pyfiglet.figlet_format( t )
    print(ASCII_art_1)

def wait ():
    class colors:
        RED = '\033[91m'
        END = '\033[0m'
    i = 0
    while True:
        if i % 2 == 0:
            print(colors.RED + "Please Wait. . ." + colors.END, end='\r')
        else:
            print("Please Wait. . .", end='\r')
        time.sleep(0.5)  # Sleep for a short duration to visualize the effect
        i += 1



def db_con ():    
    return mysql.connector.connect(
    host="54.183.115.2",
    user="root",
    password="password",
        )


# Loop through each region
def instance_region ():
    try:
        for region1 in ec2_regions:
            ec2 = boto3.client('ec2', region_name=region1)
            describe = ec2.describe_instances()
            for reservation in describe['Reservations']:
                for instance in reservation['Instances']:
                    if instance['InstanceId'] == instance_id:
                        return region1
    except Exception as e:
        print(e)
        sys.exit()




def update_date(instance_id, Instance_region,extend_days):
    ec2 = boto3.client('ec2', region_name=Instance_region)
    describe = ec2.describe_instances(InstanceIds=[instance_id],)
    for reservation in describe['Reservations']:
        for instance in reservation['Instances']:
            Created_date = instance['UsageOperationUpdateTime']
            new_date = Created_date + timedelta(days=extend_days)
            return new_date.strftime('%Y-%m-%d')




def update_tag(instance_id, Instance_region, tags):
     ec2 = boto3.client('ec2', region_name=Instance_region)
     ec2.create_tags(Resources=[instance_id], Tags=tags)
     print("Instance Tag Updated")




def update_db(extend_hours, instance_id):
    update_query = f"""
                UPDATE {db_name}.{db_table_name}
                SET Lease_Duration = %s
                WHERE Instance_ID = %s
                """
    update_data = (extend_hours, instance_id)
    
    conn = db_con()
    cursor = conn.cursor()
    cursor.execute(update_query, update_data)
    conn.commit()
    conn.close()
    print("Lease Extension Completed")



def main():

    if instance_id is None:
        print ("PLEASE PASS INTANCE ID AS ARGUMENT.....")
    else:
        Script_header()
        th = threading.Thread(target=wait, daemon=True)
        th.start()
        extend_hours = extend_days * 24
        Instance_region = instance_region()
        New_extended_data = update_date(instance_id, Instance_region, extend_days)
        tags = [
        {"Key": "LeaseDuration", "Value": New_extended_data},
        {"Key": "ExtendedLeaseDuration", "Value": str(extend_days)}
        ]
        update_tag(instance_id, Instance_region, tags)
        update_db(extend_hours, instance_id)



if __name__ == "__main__":


    main()



