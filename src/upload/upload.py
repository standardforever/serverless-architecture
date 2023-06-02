import boto3
import base64

def lambda_handler(event, context):
    # Extract the payload from the event
    response = base64.b64decode(event['body-json']).decode('utf-8')
    return (response)
    image_data_base64 = event["content"]

    # Decode the base64-encoded image data
    image_data = base64.b64decode(image_data_base64)

    # Set up the S3 client
    s3 = boto3.client('s3')

    # Define the S3 bucket and key for the uploaded image
    bucket_name = 'your-s3-bucket-name'
    key = 'path/to/uploaded-image.jpg'  # Modify as needed

    # Upload the image to S3
    try:
        s3.put_object(Body=image_data, Bucket=bucket_name, Key=key)
        response_body = 'Image uploaded successfully'
        status_code = 200
    except Exception as e:
        response_body = str(e)
        status_code = 500

    # Return the response
    response = {
        'statusCode': status_code,
        'body': response_body
    }

    return response
