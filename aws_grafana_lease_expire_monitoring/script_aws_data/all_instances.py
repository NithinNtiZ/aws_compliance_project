import boto3
from datetime import datetime, timedelta
from tabulate import tabulate
import threading, time, sys, os
import pyfiglet
from connection import db_con, boto_con

# supportlab.azurecr.io/supportlab-aws-multiregion-instance-data


current_time = datetime.now()
extend_days = 2
db_name = os.getenv('DB_NAME')
db_table_name = os.getenv('DB_TABLE_NAME')

region = 'us-west-1'


# db_name = os.getenv('DB_NAME')
# db_table_name = os.getenv('DB_TABLE_NAME')


# Create a Boto3 client for EC2
ec2 = boto_con('ec2',region)

# Get a list of all AWS regions
ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Script Header 
def Script_header():
    t = "AWS PROJECT LAB"
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
        global stop_th
        if stop_th:
            break

data = []
intances_id = []
Expire = None

def extended_lease_duration(instance_id):
    conn = db_con()
    cursor = conn.cursor()
    check_query = f"SELECT Lease_Duration FROM {db_name}.{db_table_name} WHERE Instance_ID = %s"
    cursor.execute(check_query, (instance_id,))
    existing_instance = cursor.fetchone()
    # for extended_lease_duration in existing_instance:
    if existing_instance is not None:
        for extended_lease_duration in existing_instance:
                return extended_lease_duration
    else:
        return 48
def multi_region_data(region):

     # Establishing a connection to MySQL
    conn = db_con()

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    ec2=boto_con('ec2',region)
    describe = ec2.describe_instances()
    for reservation in describe['Reservations']:
        for instance in reservation['Instances']:

                    instance_id = instance['InstanceId']
                    start_time = instance['UsageOperationUpdateTime'].replace(tzinfo=None)
                    Instance_type = instance['InstanceType'] 
                    instance_status : str = instance['State']['Name']
                    zone = instance['Placement']['AvailabilityZone']

                    found_extended_lease_duration = False 
                    for tags in instance['Tags']:
                        if tags['Key'] == 'ExtendedLeaseDuration':
                            extend_end_date = int(extended_lease_duration(instance_id))
                            found_extended_lease_duration = True
                            if tags['Value'] == '' or tags['Value'] == None:
                                for tags in instance['Tags']: 
                                    if tags['Key'] == 'Environment' and tags['Value'] != 'Production':
                                        default_end_date = (start_time + timedelta(hours=48))
                                    elif tags['Key'] == 'Environment' and tags['Value'] == 'Production':
                                        default_end_date = current_time
                            else:
                                for tags in instance['Tags']: 
                                    if tags['Key'] == 'Environment' and tags['Value'] != 'Production':
                                        default_end_date = (start_time + timedelta(hours=extend_end_date))
                                    elif tags['Key'] == 'Environment' and tags['Value'] == 'Production':
                                        default_end_date = (start_time + timedelta(hours=extend_end_date))
                                break
                    if not found_extended_lease_duration:
                            for tags in instance['Tags']: 
                                if tags['Key'] == 'Environment' and tags['Value'] != 'Production':
                                    default_end_date = (start_time + timedelta(hours=48))
                                elif tags['Key'] == 'Environment' and tags['Value'] == 'Production':
                                    default_end_date = current_time

                    delta_remaining = float((default_end_date - current_time).total_seconds()/3600)
                    
                    time_remaining = 0
                    if delta_remaining > 0:
                        time_remaining = delta_remaining



                    created_date = start_time 
                    today = (datetime.strptime((datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")) 

                    name = None
                    aws_id = None
                    remaining_days = None
                    extend_date = None


                    for tags in instance['Tags']:
                        if tags['Key'] == 'AwsID':
                            aws_id = tags['Value'] 
                        elif tags['Key'] == 'Environment': 
                            env_name = tags['Value'] 
                        elif tags['Key'] == 'Name':
                            name = tags['Value']
                        elif tags['Key'] == 'LeaseDuration': 
                            if tags['Value'] !='':
                                try:
                                    extend_date = (datetime.strptime(tags['Value'], "%Y-%m-%d")).replace(tzinfo=None)
                                except Exception as e:
                                    print (f"secound : {tags['Value']}, {instance_id}, {region} {type(tags['Value'])} {type(extend_date_str)} {extend_date_str}")
                                    sys.exit(e)
                            else:
                                extend_date_str = current_time.strftime("%Y-%m-%d")
                                extend_date = datetime.strptime(extend_date_str, "%Y-%m-%d")
                   
                   
                   
                    try:
                        global expired_date, Expire 
                        expired_date = extend_date #if extend_date else None
                    except Exception as err:
                        print (f"skipping : {err}") 
                    if expired_date:
                        x_days = (expired_date - created_date).days
                        x_hours = (default_end_date - created_date).total_seconds()/3600
                        delta =(default_end_date - today).total_seconds()/3600
                        

                        if (delta) < 0:
                            Expire = "Expired"
                            delta =delta*(-1)
                        else:
                            Expire = "Not Expired"
                            delta =delta
                    else:
                        x = None


                        
                    # Define the MySQL INSERT query
                    insert_query = f"""
                    INSERT INTO {db_name}.{db_table_name} (Name, Instance_ID, AWS_ID, Zone, Environment, Type, Start_Time, End_Time, Lease_Duration, Remaining_Days, Status, Expire, Time_Remaining) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    # Data to be inserted
                    data_to_insert = (name, instance_id, aws_id, zone, env_name, Instance_type, start_time, default_end_date, x_hours, time_remaining, instance_status, Expire, time_remaining)

                    # check if Instance exist in the databse

                    check_query = f"SELECT Instance_ID FROM {db_name}.{db_table_name} WHERE Instance_ID = %s"
                    cursor.execute(check_query, (instance_id,))
                    existing_instance = cursor.fetchone()

                    if existing_instance is None:
                        # Instance does not exist, insert the new record
                        cursor.execute(insert_query, data_to_insert)
                        conn.commit()
                    else:
                        # Update query for SQL
                        update_query = f"""
                            UPDATE {db_name}.{db_table_name}
                            SET Name = %s, 
                                AWS_ID = %s, 
                                Zone = %s,
                                Environment =%s, 
                                Type = %s, 
                                Start_Time = %s, 
                                End_Time = %s, 
                                Lease_Duration = %s, 
                                Remaining_Days = %s, 
                                Status = %s, 
                                Expire = %s,
                                Time_Remaining = %s
                            WHERE Instance_ID = %s
                        """

                        # Data to be updated
                        data_to_update = (name, aws_id, zone, env_name, Instance_type, start_time, default_end_date, x_hours, time_remaining, instance_status, Expire, time_remaining, instance_id)

                        # Execute the UPDATE query
                        cursor.execute(update_query, data_to_update)
                        conn.commit()
                        print("Instance already exists in the database. Updating table.")
                   
                    data.append([name, instance_id, aws_id, zone,env_name, Instance_type, start_time, default_end_date, x_hours, time_remaining, instance_status, Expire, time_remaining])
                    intances_id.append(instance_id)

def main():

    Script_header()
    global stop_th
    stop_th = False
    th = threading.Thread(target=wait, daemon=True)
    th.start()
    for region in ec2_regions: 
        multi_region_data(region)
    stop_th = True
    if data:
        headers = ["Name", "Instance ID", "AWS ID", "Zone","Environment", "Type", "Start Time", "End Time", "Lease duration", "Remaining Days", "Status", "Expire", "Time Remaining"]
        x = tabulate(data, headers=headers, tablefmt="grid")
        print(x)

if __name__ == '__main__':

    main()
