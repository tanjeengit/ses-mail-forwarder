# AWS SES Email Forwarder

This project demonstrates how to use **Amazon SES**, **S3**, and **Lambda** to forward incoming emails to a target inbox.

## 📧 Example

Emails sent to addresses like:

```
support@forwarding.example.com
info@forwarding.example.com
noreply@forwarding.example.com
```

Will be:

1. **Received by SES**
2. **Stored in an S3 bucket**
3. **Forwarded by a Lambda function** to `inbox@example.com`

## 📂 Folder Structure

- `lambda_function.py` – AWS Lambda function script
- `README.md` – Project overview and documentation

## ✅ Prerequisites

- Verified domain in Amazon SES (`forwarding.example.com`)
- S3 bucket for storing raw messages
- Proper IAM roles and Lambda permissions

## 🛠️ Customization

Replace `FROM_ADDRESS` and `TO_ADDRESS` in `lambda_function.py` to fit your requirements.


