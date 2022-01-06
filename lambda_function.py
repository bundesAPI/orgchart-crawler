import asyncio
import json
import os

import sentry_sdk

from main import check_all_orgcharts

sentry_sdk.init(
    os.getenv("SENTRY_DSN", None),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

SNS_ACTIONS_MAPPING = {
    "crawl-all-orgcharts": check_all_orgcharts,
}


def handler(event, context):
    """this service is currently sns only"""
    event = json.loads(event["Records"][0]["Sns"]["Message"])
    if event["action"] in SNS_ACTIONS_MAPPING:
        asyncio.run(SNS_ACTIONS_MAPPING[event["action"]](**event["parameters"]))
    return {"ok": True, "message": "SNS Task executed successfully"}
