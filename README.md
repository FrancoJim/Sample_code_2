# Sample Code 2

This is just a sample application to demonstrate coding capabilities.

## Python Dependencies

- pytest
- boto3
- pandas
- poetry
- Bureau of Economic Analysis (BEA) API
  - [API Guide](https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf)

## Pre-requisites

### Copy Environment Variables File

```bash
cp example.env .env
```

### Bureau of Economic Analysis (BEA) API Request

1. Go to [BEA Data Application Programming Interface (API)](https://apps.bea.gov/API/signup/)
2. Register for an API key.
3. Open email and click on the link `Please click here to activate your key`.
4. Complete Captcha and click `Activate Key`.
5. Copy the API key from email.
6. Add API key string to environment variable `BEA_API_KEY` in `.env` file.

### AWS Credentials

1. Go to [AWS Management Console](https://aws.amazon.com/console/)
2. Click Username in upper-right corner, then `My Security Credentials`.
3. Click on `Access keys (access key ID and secret access key)`.
4. Click on `Create New Access Key`.
5. Copy and add `Access key ID` and `Secret access key` to environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `.env` file.

## Docker Execution

To run the application in a Docker container, execute the following command:

## Production

```bash
docker-compose --profile sample_2_prod up -d
```

## Development

```bash
docker-compose --profile sample_2_dev up -d
```

## Testing

```bash
docker-compose --profile sample_2_test up -d
```
