import json
import boto3

led_topic = "<YOUR_LED_TOPIC>"

client = boto3.client('iot-data', region_name='us-west-2')

def lambda_handler(event, context):
    try:
        client.publish(topic=led_topic, qos=1, payload=event["queryStringParameters"]["led"]) 
        return {
            'statusCode': 200,
            'body': json.dumps(event["queryStringParameters"]["led"])
        }
    except:
         return {
            'statusCode': 200,
            'body': json.dumps("Error, led status should be a get: http://<FULL_URL>?led=1")
        }
