import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_bill_details(text):

    prompt = f"""
You are an expert Bill Information Extraction Assistant.

Extract the bill information from the OCR text below.

Return ONLY valid JSON.

JSON Format:

{{
    "store_name":"",
    "date":"",
    "invoice_number":"",
    "total_amount":"",
    "gst":"",
    "items":[
        {{
            "name":"",
            "quantity":"",
            "rate":"",
            "amount":""
        }}
    ]
}}

Rules:
- Do not return markdown.
- Do not explain anything.
- If any field is missing, keep it as an empty string.
- Return only JSON.

OCR Text:

{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")

    return json.loads(result)