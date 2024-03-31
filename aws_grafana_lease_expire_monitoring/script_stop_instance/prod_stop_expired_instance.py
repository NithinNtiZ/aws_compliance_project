import boto3
import os
from connection import db_con, boto_con 




# db_name = "grafana_test"
# db_table_name = "instance_data_test"

db_name = os.getenv('DB_NAME')
db_table_name =  os.getenv('DB_TABLE_NAME')

conn = db_con()
cursor = conn.cursor()

expire_instance_query_prod = f"""
SELECT Instance_ID FROM {db_name}.{db_table_name} WHERE Expire = 'Expired' AND Status = 'running'
"""
cursor.execute(expire_instance_query_prod)

instance_id = cursor.fetchall()
instance_id_list = [i[0] for i in instance_id]


region_name= None
ec2 = boto_con('ec2', region_name)
ec2_regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]


def intances_region(instance_id):
        for region in ec2_regions:
            ec2 = boto_con('ec2', region)
            describe = ec2.describe_instances()
            for reservation in describe['Reservations']:
                for instance in reservation['Instances']:
                    if instance_id == instance['InstanceId']:
                        return region 


def stop_instance(instance_id,intances_region_of_instance_id):
    ec2= boto_con('ec2',intances_region_of_instance_id)
    response = ec2.stop_instances(InstanceIds=[instance_id])
     

def main():
    for instance_id in instance_id_list:
        intances_region_of_instance_id = intances_region(instance_id)
        stop_instance(instance_id,intances_region_of_instance_id)

if __name__ == "__main__":
     main()