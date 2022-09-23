import logging
import json
import azure.functions as func
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch
from flask import Flask,render_template,url_for
from flask import request as req
import requests
import os
# Initialize the HuggingFace summarization pipeline
summarizer = pipeline("summarization",model="t5-base", tokenizer="t5-base")


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            text = req_body.get('text')

    summarized = summarizer(str(text), min_length=75, max_length=300)
    if summarized is not None:
        logging.info("Got back a summary")
    if text:
        return func.HttpResponse(json.dumps({"text": text, "summary": summarized}), mimetype="application/json")
    else:
        return func.HttpResponse(
            "Function executed successfully. Pass a text in the query string or in the request body to summarise.",
            status_code=400
        )
