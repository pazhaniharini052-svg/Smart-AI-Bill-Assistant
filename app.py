import os
import json
import streamlit as st
from dotenv import load_dotenv

from PIL import Image
from pdf2image import convert_from_bytes

from database import Session, Bill
from chat import ask_bill_assistant
from view_bills import show_bills

from ocr import extract_text
from groq_ai import extract_bill_details
from dashboard import show_dashboard


load_dotenv()


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart AI Bill Assistant",
    page_icon="🧾",
    layout="wide"
)


# ---------------- UPLOAD FOLDER ----------------

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ---------------- SESSION ----------------

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


if "file_path" not in st.session_state:
    st.session_state.file_path = None



# ---------------- SIDEBAR ----------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Upload Bill",
        "Dashboard",
        "My Bills"
    ]
)



# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    show_dashboard()



# ==================================================
# MY BILLS
# ==================================================

elif page == "My Bills":

    show_bills()



# ==================================================
# UPLOAD BILL
# ==================================================

else:


    left, right = st.columns([3, 1])


    with left:


        st.title(
            "🧾 Smart AI Bill Assistant"
        )


        st.write(
            "Upload a bill image or PDF and extract details using AI."
        )


        # ---------------- UPLOAD ----------------


        uploaded_file = st.file_uploader(
            "Choose Bill",
            type=[
                "png",
                "jpg",
                "jpeg",
                "pdf"
            ]
        )


        if uploaded_file:


            save_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )


            with open(
                save_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )


            st.session_state.file_path = save_path



            if uploaded_file.type == "application/pdf":


                pages = convert_from_bytes(
                    uploaded_file.getvalue(),
                    poppler_path=r"C:\Users\pazha\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
                )


                image = pages[0]


            else:


                image = Image.open(
                    uploaded_file
                )



            st.session_state.uploaded_image = image


            st.success(
                "✅ Bill Uploaded Successfully"
            )



        # ---------------- PREVIEW ----------------


        if st.session_state.uploaded_image:


            st.image(
                st.session_state.uploaded_image,
                caption="Bill Preview",
                use_container_width=True
            )


            extract = st.button(
                "🚀 Extract Bill Details"
            )


        else:


            extract = False
                    # ---------------- OCR + GROQ ----------------

        if extract:

            try:

                with st.spinner(
                    "Reading bill text..."
                ):

                    bill_text = extract_text(
                        st.session_state.uploaded_image
                    )


                st.subheader(
                    "📄 Extracted Text"
                )


                st.text_area(
                    "OCR Output",
                    bill_text,
                    height=200
                )


                with st.spinner(
                    "Extracting bill details..."
                ):


                    data = extract_bill_details(
                        bill_text
                    )



                st.success(
                    "✅ Bill Details Extracted"
                )



                # ---------------- STORE DETAILS ----------------


                st.subheader(
                    "🏪 Store Information"
                )


                st.write(
                    "Store Name:",
                    data.get("store_name")
                )


                st.write(
                    "Invoice Number:",
                    data.get("invoice_number")
                )


                st.write(
                    "Date:",
                    data.get("date")
                )


                st.write(
                    "Total Amount:",
                    f"₹ {data.get('total_amount')}"
                )


                st.write(
                    "GST:",
                    f"₹ {data.get('gst')}"
                )



                # ---------------- ITEMS ----------------


                st.subheader(
                    "🛒 Purchased Items"
                )


                for index, item in enumerate(
                    data.get("items", []),
                    start=1
                ):


                    st.markdown(
                        f"### {index}. {item.get('name')}"
                    )


                    c1, c2, c3 = st.columns(3)


                    with c1:

                        st.write(
                            "Quantity"
                        )

                        st.info(
                            item.get("quantity")
                        )


                    with c2:

                        st.write(
                            "Rate"
                        )

                        st.info(
                            f"₹ {item.get('rate')}"
                        )


                    with c3:

                        st.write(
                            "Amount"
                        )

                        st.success(
                            f"₹ {item.get('amount')}"
                        )



                st.divider()



                # ---------------- SAVE BILL ----------------


                session = Session()


                bill = Bill(

                    store_name=data.get(
                        "store_name"
                    ),


                    date=data.get(
                        "date"
                    ),


                    invoice_number=data.get(
                        "invoice_number"
                    ),


                    total_amount=float(
                        str(
                            data.get(
                                "total_amount",
                                0
                            )
                        ).replace(",", "")
                    ),


                    gst=float(
                        str(
                            data.get(
                                "gst",
                                0
                            )
                        ).replace(",", "")
                    ),


                    items=json.dumps(
                        data.get(
                            "items",
                            []
                        )
                    ),


                    file_path=st.session_state.file_path

                )


                session.add(
                    bill
                )


                session.commit()


                session.close()



                st.success(
                    "💾 Bill Saved Successfully"
                )


                



            except Exception as e:


                st.error(
                    "❌ Failed to extract bill"
                )


                st.exception(e)





    # ==================================================
    # CHAT ASSISTANT
    # ==================================================


    with right:


        st.subheader(
            "🤖 Smart Bill Assistant"
        )


        question = st.chat_input(
            "Ask about your bills..."
        )


        if question:


            answer = ask_bill_assistant(
                question
            )


            st.chat_message(
                "assistant"
            ).write(
                answer
            )