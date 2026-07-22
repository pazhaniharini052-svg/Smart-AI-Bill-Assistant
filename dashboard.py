import streamlit as st
import pandas as pd
import plotly.express as px

from database import Session, Bill


def show_dashboard():

    st.title("📊 Smart Bill Dashboard")

    session = Session()

    bills = session.query(Bill).all()

    session.close()

    if len(bills) == 0:

        st.info("No bills available.")

        return

    data = []

    for bill in bills:

        data.append({

            "Store": bill.store_name,

            "Date": bill.date,

            "Invoice Number": bill.invoice_number,

            "Total": float(bill.total_amount),

            "GST": float(bill.gst)

        })

    df = pd.DataFrame(data)

    # ---------------- KPI ----------------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🧾 Total Bills",
            len(df)
        )

    with c2:
        st.metric(
            "💰 Total Expense",
            f"₹ {df['Total'].sum():,.2f}"
        )

    with c3:
        st.metric(
            "📈 Average Bill",
            f"₹ {df['Total'].mean():,.2f}"
        )

    st.divider()

    # ---------------- TABLE ----------------

    st.subheader("📄 Bill Summary")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # ---------------- STORE EXPENSE ----------------

    st.subheader("🏪 Store-wise Expenses")

    store_df = (
        df.groupby("Store", as_index=False)["Total"]
        .sum()
        .sort_values("Total", ascending=False)
    )

    fig1 = px.bar(
        store_df,
        x="Store",
        y="Total",
        title="Expense by Store",
        text_auto=True
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ---------------- PIE CHART ----------------

    st.subheader("🥧 Expense Distribution")

    fig2 = px.pie(
        store_df,
        names="Store",
        values="Total",
        hole=0.4
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ---------------- GST ANALYSIS ----------------

    st.subheader("💸 GST Analysis")

    fig3 = px.bar(
        df,
        x="Store",
        y="GST",
        text_auto=True,
        title="GST Paid per Bill"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )