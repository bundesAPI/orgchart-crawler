import logging
import os

from utils import get_client
from gql import gql


AWS_LAMBDA_FUNCTION_NAME = os.getenv("AWS_LAMBDA_FUNCTION_NAME", None)
AWS_REGION = os.getenv("AWS_REGION", None)
AWS_VERSION = os.getenv("AWS_LAMBDA_FUNCTION_VERSION", None)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DOMAIN = os.getenv("SERVICE_DOMAIN")
ORGCHART_CRAWLER_SNS_TOPIC = os.getenv("ORGCHART_CRAWLER_SNS_TOPIC", None)

ORG_CHART_URLS_QUERY = gql(
    """
    query allOrgChartUrls(){
     {
      allOrgChartUrls {
        edges {
          node {
            url
            createdAt
            id
            orgchartDocuments {
              edges {
                node {
                  createdAt
                  documentHash
                  status
                }
              }
            }
          }
        }
      }
    }
    }
    """
)


def check_all_orgcharts():
    client = get_client(DOMAIN, CLIENT_ID, CLIENT_SECRET)
    orgcharts = client.execute(ORG_CHART_URLS_QUERY)
    logger.info("Fetched Orgchart URLS")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
