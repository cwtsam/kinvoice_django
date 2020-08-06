import boto3

s3 = boto3.client('s3')
s3.upload_file('M_3.mp3','djangomediakinvoice','M_3upload.mp3')