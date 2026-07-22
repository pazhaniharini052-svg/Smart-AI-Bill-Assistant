import os
import json
import streamlit as st

from database import Session, Bill


def show_bills():

    st.title("📂 My Bills")

    session = Session()

    try:

        bills = session.query(Bill).all()

    except Exception as e:

        st.error(f"Database error: {e}")
        session.close()
        return



    if not bills:

        st.info("No bills uploaded yet.")
        session.close()
        return



    for bill in bills:


        total = float(bill.total_amount or 0)


        with st.expander(
            f"🧾 {bill.store_name} | ₹{total:.2f}"
        ):


            st.write(
                "📅 Date:",
                bill.date
            )


            st.write(
                "🧾 Invoice Number:",
                bill.invoice_number
            )


            gst = float(bill.gst or 0)


            st.write(
                "💰 GST:",
                f"₹ {gst:.2f}"
            )



            # ================= ITEMS =================


            st.subheader(
                "🛒 Purchased Items"
            )


            try:

                items = json.loads(
                    bill.items
                )


                for i, item in enumerate(
                    items,
                    start=1
                ):

                    st.markdown(
                        f"### {i}. {item.get('name')}"
                    )


                    c1, c2, c3 = st.columns(3)


                    with c1:

                        st.write("Quantity")

                        st.info(
                            item.get("quantity")
                        )


                    with c2:

                        st.write("Rate")

                        st.info(
                            f"₹ {float(item.get('rate',0)):.2f}"
                        )


                    with c3:

                        st.write("Amount")

                        st.success(
                            f"₹ {float(item.get('amount',0)):.2f}"
                        )


            except:

                st.write(
                    bill.items
                )



            st.divider()



            # ================= BILL FILE =================


            st.subheader(
                "📄 Bill Copy"
            )


            if bill.file_path:


                file_path = bill.file_path


                st.write(
                    "File:",
                    file_path
                )


                if os.path.exists(file_path):


                    st.success(
                        "✅ Bill copy available"
                    )


                    file_name = os.path.basename(
                        file_path
                    )


                    # -------- IMAGE --------


                    if file_path.lower().endswith(
                        (".png",".jpg",".jpeg")
                    ):


                        st.image(
                            file_path,
                            width=400
                        )


                        with open(
                            file_path,
                            "rb"
                        ) as file:


                            st.download_button(

                                label="⬇️ Download Image",

                                data=file,

                                file_name=file_name,

                                mime="image/jpeg"

                            )



                    # -------- PDF --------


                    elif file_path.lower().endswith(
                        ".pdf"
                    ):


                        with open(
                            file_path,
                            "rb"
                        ) as file:


                            st.download_button(

                                label="⬇️ Download PDF",

                                data=file,

                                file_name=file_name,

                                mime="application/pdf"

                            )


                    else:

                        st.warning(
                            "Unsupported file type"
                        )



                else:


                    st.error(
                        "❌ File missing from uploads folder"
                    )


            else:


                st.info(
                    "No bill copy available"
                )



            st.divider()



            # ================= DELETE =================


            if st.button(
                "🗑 Delete Bill",
                key=f"delete_{bill.id}"
            ):


                if bill.file_path and os.path.exists(
                    bill.file_path
                ):

                    os.remove(
                        bill.file_path
                    )


                session.delete(
                    bill
                )


                session.commit()


                st.success(
                    "✅ Bill deleted successfully"
                )


                st.rerun()



    session.close()