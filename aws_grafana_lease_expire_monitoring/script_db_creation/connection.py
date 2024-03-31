import boto3
import mysql.connector 
import json, os, sys


aws_access_key_id= os.getenv('ACCESS_KEY')
aws_secret_access_key=os.getenv('SECRET_KEY')
db_name=os.getenv('DB_NAME')
db_host_s=os.getenv('DB_HOST')

# sys.exit(db_host)

def boto_con(service, region_name):
    region = 'us-west-1' if region_name == "" or region_name is None else region_name
    region_name = region
    aws_access_key_id= os.getenv('ACCESS_KEY')
    aws_secret_access_key=os.getenv('SECRET_KEY')
    return boto3.client(service, aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region_name)



def get_secret_data():
    secret_name = "Grafana_aws_project_secret"
    region_name = "us-west-1"
    sm = boto_con('secretsmanager',region_name)
    get_secret_value_response = sm.get_secret_value(SecretId=secret_name)
    return json.loads(get_secret_value_response['SecretString'])

def db_host():
    return get_secret_data().get('DB_HOST')
    #  print (x)
    #  return x

def db_pass():
    return get_secret_data().get('DB_PASS')

def db_user():
    return get_secret_data().get('DB_USER')

# def db_name():
#     return get_secret_data().get('DB_NAME')



if db_host_s is None or db_host_s == '':
    db_host_s = db_host()

    
db_user = db_user()
db_pass = db_pass()


def db_con ():    
    return mysql.connector.connect(
    host= db_host_s,
    user= db_user,
    password= db_pass,
        )


if __name__ == "__main__":

    res = db_con()

    print(res)