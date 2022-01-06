# Strukturen-ML
This service can be used via an SNS-Topic asynchronously.

## Supported SNS Messages
Every method works the same way with the same GET-Parameters as documented in the API Documentation.

### Update all orgcharts
**Topic:** ```orgchart-crawler-bund-dev```
```json
{
    "action": "crawl-all-orgcharts",
    "parameters": {
    }
}
```


## Service Configuration
This service is partly configured via [terraform](https://github.com/bundesAPI/terraform/blob/main/orgchart_crawler.tf). The deployment pipeline (via serverless.yaml) needs the following environment variables in its build context:

| Variable                         | Value                                                                                                                |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------|
| ORGCHART_CRAWLER_SNS_TOPIC       | SNS Topic ARN for orgchart crawler jobs                                                                              |
| SENTRY_DSN                       | sentry monitoring dsn…                                                                                               |
| SENTRY_PROJECT                   | sentry project name (orgchart-ml)                                                                                    |
| SERVICE_DOMAIN                   | backend service domain                                                                                               |
| CLIENT_ID                        | to authenticate as a service via oauth2 client credentials                                                           |
| CLIENT_SECRET                    | to authenticate as a service via oauth2 client credentials                                                           |
| LAMBDA_EXECUTION_ROLE_ARN        | the iam rule that executes the lambda. Needs access to lambda, the buckets, the queues and cloudwatch                |
| DOMAIN                           | the domain this service is running under. Needs to be configured for gateway and already an tls certificate assigned |
