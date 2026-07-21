import os
from dotenv import load_dotenv
from google import genai

from database import Session, Bill


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)



def get_bill_data():

    session = Session()

    try:

        bills = session.query(Bill).all()

        if not bills:
            return "No bills are uploaded yet."


        bill_text = ""


        for bill in bills:

            bill_text += f"""
Bill Details:

Store Name: {bill.store_name}

Date: {bill.date}

Invoice Number: {bill.invoice_number}

Total Amount: ₹{bill.total_amount}

GST: ₹{bill.gst}

Items:
{bill.items}

-------------------------
"""


        return bill_text


    finally:
        session.close()



def ask_bill_assistant(question):

    bills = get_bill_data()


    if bills == "No bills are uploaded yet.":

        return "Please upload a bill first so I can answer questions about it."



    prompt = f"""
You are Smart AI Bill Assistant.

Answer only from the uploaded bill data.

Rules:
- Do not make up information.
- If information is missing, reply:
  "I couldn't find that information in your uploaded bills."
- Keep answers short and clear.
- Mention money values with ₹.


Uploaded Bills:

{bills}


User Question:

{question}

"""


    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )


    return response.text.strip()