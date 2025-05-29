import boto3
import email
from email import policy
from email.parser import BytesParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

s3 = boto3.client('s3')
ses = boto3.client('ses')

FROM_ADDRESS = "Service Accounts Desk UK <no-reply@sesmail.catenacloud.net>"
TO_ADDRESS = "service-inbox@catenacloud.net"
SOURCE_ARN = "arn:aws:ses:eu-north-1:850995576846:identity/sesmail.catenacloud.net"

def lambda_handler(event, context):
    print("Received event:", event)

    try:
        # Extract bucket and object key
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"Fetching email from bucket: {bucket}, key: {key}")

        # Read raw email from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        raw_email = response['Body'].read()

        # Parse original email content
        parsed_email = BytesParser(policy=policy.default).parsebytes(raw_email)
        original_subject = parsed_email['subject'] or "(no subject)"
        original_body = parsed_email.get_body(preferencelist=('plain')).get_content() if parsed_email.get_body() else "(no body)"

        # Construct a new email with your verified sender address
        msg = MIMEMultipart()
        msg['Subject'] = "FWD: " + original_subject
        msg['From'] = FROM_ADDRESS
        msg['To'] = TO_ADDRESS

        # Attach original content
        body = MIMEText(original_body, 'plain')
        msg.attach(body)

        # Send via SES
        result = ses.send_raw_email(
            Source=FROM_ADDRESS,
            Destinations=[TO_ADDRESS],
            RawMessage={'Data': msg.as_string()},
            SourceArn=SOURCE_ARN
        )

        print("Email forwarded successfully:", result)
        return {'status': 'success', 'messageId': result['MessageId']}

    except Exception as e:
        print("Error forwarding email:", str(e))
        return {'status': 'error', 'message': str(e)}
