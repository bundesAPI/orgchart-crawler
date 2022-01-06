import hashlib
import logging
import os
from io import BytesIO

from utils import get_client

import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import requests
from queries import ORG_CHART_URLS_QUERY, ORG_CHART_CREATE_ERROR

USER_AGENT = "strukturen.bund.dev crawler (crawler.beta.strukturen.bund.dev)"
CONTACT = "kontakt@bund.dev"

AWS_LAMBDA_FUNCTION_NAME = os.getenv("AWS_LAMBDA_FUNCTION_NAME", None)
AWS_REGION = os.getenv("AWS_REGION", None)
AWS_VERSION = os.getenv("AWS_LAMBDA_FUNCTION_VERSION", None)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DOMAIN = os.getenv("SERVICE_DOMAIN")
ORGCHART_CRAWLER_SNS_TOPIC = os.getenv("ORGCHART_CRAWLER_SNS_TOPIC", None)



def check_all_orgcharts():
    client = get_client(DOMAIN, CLIENT_ID, CLIENT_SECRET)
    orgcharts = client.execute(ORG_CHART_URLS_QUERY)
    logger.info("Fetched Orgchart URLS")
    for orgchart in orgcharts["allOrgChartUrls"]["edges"]:
        og = None
        try:
            og = download_orgchart(orgchart["node"]["url"])
        except DownloadError as e:
            report_error(orgchart["node"]["id"], e)
            continue
        if og and not orgchart_exists(og, orgchart["node"]["orgchartDocuments"]["edges"]):
            save_orgchart(orgchart["node"]["id"], og)
        else:
            print("already in DB")


def check_orgchart(orgchart_url_id):
    pass


def report_error(orgchart_url_id, message):
    logger.error(message)
    client = get_client(DOMAIN, CLIENT_ID, CLIENT_SECRET)
    client.execute(ORG_CHART_CREATE_ERROR, variable_values={"message": str(message),
                                                            "orgChartUrlId": orgchart_url_id})

def orgchart_exists(document, stored_orgcharts):
    m = hashlib.md5()
    m.update(document.read())

    if str(m.hexdigest()) in [o["node"]["documentHash"] for o in stored_orgcharts]:
        return True
    return False

def save_orgchart(orgchart_url_id, document, hash):
    logger.info("save orgchart")
    client = get_client(DOMAIN, CLIENT_ID, CLIENT_SECRET)
    orgcharts = client.execute(ORG_CHART_CREATE_ERROR, variable_values={}, upload_files = True)

class DownloadError(Exception):
    pass


def download_orgchart(orgchart_url):
    headers = {
        'User-Agent': USER_AGENT,
        'From': CONTACT
    }

    blob = requests.get(orgchart_url, headers=headers)
    file_obj = BytesIO(blob.content)
    file_obj.seek(0)

    try:
        pdf = pdfplumber.open(file_obj)
        logger.info(pdf.metadata)
    except PDFSyntaxError as e:
        raise DownloadError(e)
    return file_obj


if __name__ == "__main__":
    check_all_orgcharts()