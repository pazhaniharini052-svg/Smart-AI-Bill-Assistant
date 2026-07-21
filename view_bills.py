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



            # -------- ITEMS DISPLAY --------


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


                    col1, col2, col3 = st.columns(3)



                    with col1:

                        st.write(
                            "Quantity"
                        )

                        st.info(
                            item.get("quantity")
                        )



                    with col2:

                        st.write(
                            "Rate"
                        )

                        st.info(
                            f"₹ {float(item.get('rate',0)):.2f}"
                        )



                    with col3:

                        st.write(
                            "Amount"
                        )

                        st.success(
                            f"₹ {float(item.get('amount',0)):.2f}"
                        )


                    st.divider()



            except Exception:

                st.write(
                    bill.items
                )



            # -------- BILL COPY --------


            st.subheader(
                "📄 Bill Copy"
            )


            if bill.file_path:


                if os.path.exists(
                    bill.file_path
                ):


                    st.success(
                        "✅ Bill copy available"
                    )


                    # IMAGE

                    if bill.file_path.lower().endswith(
                        (".png",".jpg",".jpeg")
                    ):


                        st.image(
                            bill.file_path,
                            width=400
                        )



                    # PDF

                    elif bill.file_path.lower().endswith(
                        ".pdf"
                    ):


                        with open(
                            bill.file_path,
                            "rb"
                        ) as file:


                            st.download_button(

                                label="📄 View / Download PDF",

                                data=file,

                                file_name=os.path.basename(
                                    bill.file_path
                                ),

                                mime="application/pdf"

                            )


                else:

                    st.warning(
                        "⚠️ Bill file not found"
                    )



            else:

                st.info(
                    "No bill copy available"
                )



            # -------- DELETE BILL --------


            st.divider()


            if st.button(
                "🗑 Delete Bill",
                key=f"delete_{bill.id}"
            ):


                # Delete uploaded file

                if bill.file_path and os.path.exists(
                    bill.file_path
                ):

                    os.remove(
                        bill.file_path
                    )



                # Delete database record

                session.delete(
                    bill
                )

                session.commit()


                st.success(
                    "✅ Bill deleted successfully"
                )


                st.rerun()



    session.close()