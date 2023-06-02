'''
gửi log metadata vào S3 các truy cập Internet và 
thông báo lỗi nếu có hoặc các truy cập không được phép.
'''


import boto3
import json
import urllib.request


def is_access_allowed(event):
    # Lấy địa chỉ IP nguồn từ event
    source_ip = event['requestContext']['identity']['sourceIp']
    
    # Kiểm tra nếu địa chỉ IP nguồn không được phép
    if source_ip not in allowed_ips:
        return False
    
    return True

def lambda_handler(event, context):
    # Lấy thông tin log metadata từ event
    log_metadata = event['log_metadata']

    # Kiểm tra truy cập Internet và thông báo lỗi nếu có
    try:
        response = urllib.request.urlopen('<http://www.example.com>')
        # Xử lý dữ liệu từ response (nếu cần)
    except urllib.error.URLError as e:
        # Ghi lại thông báo lỗi vào log metadata
        log_metadata['error'] = str(e)

    # Kiểm tra truy cập không được phép và ghi lại thông báo lỗi nếu có
    if not is_access_allowed():
        log_metadata['error'] = 'Access not allowed'

    # Tạo client S3
    s3_client = boto3.client('s3')

    # Lưu log metadata vào S3
    # bucket_name = 'my-s3-bucket'
    # key = 'logs/log_metadata.json'
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    s3_client.put_object(
        Body=json.dumps(log_metadata),
        Bucket=bucket_name,
        Key=key
    )
    

if __name__ == "__main__":
    # list of allowed access ips for example 
    allowed_ips = ['192.0.2.1', '203.0.113.10', '198.51.100.50']
