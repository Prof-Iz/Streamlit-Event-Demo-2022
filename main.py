import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime


def main():

    st.write("# This is a demo of the Streamlit framework of my DATACOM assignment")

    date_data_begin = datetime(2022, 3, 1)
    date_data_end = datetime(2022, 4, 1)

    with st.form("get_data"):
        col1, col2 = st.columns(2)
        with col1:
            select_date_begin = st.date_input(
                "Select a start date",
                value=datetime(2022, 3, 1),
                max_value=date_data_end,
                min_value=date_data_begin,
            )
        with col2:
            select_date_end = st.date_input(
                "Select a start date",
                value=datetime(2022, 4, 1),
                max_value=date_data_end,
                min_value=date_data_begin,
            )

        timescale = st.radio(
            label="Choose Frequency of Data", options=["daily", "hourly"]
        )

        submit_btn = st.form_submit_button("Get Data")

        if submit_btn:

            with st.spinner("Fetching Data from Thingspeak"):
                url = f"https://api.thingspeak.com/channels/1674983/feeds.json?api_key=1HFCHQH0JULE0E98&start={select_date_begin}%2000:00:00&timescale={timescale}&round=1&end={select_date_end}%2000:00:00"
                global data_fetched
                data_fetched = get_data(url)

            data_json = json.loads(data_fetched.text)

            df = pd.DataFrame.from_dict(data_json["feeds"])
            df.rename(
                inplace=True, columns={"field1": "temperature", "field2": "humidity"}
            )

            df.temperature = pd.to_numeric(df.temperature, errors="coerce")
            df.humidity = pd.to_numeric(df.humidity, errors="coerce")
            df.created_at = pd.to_datetime(df.created_at)
            df.dropna(inplace=True)
            df.set_index("created_at", inplace=True)
            try:
                df.drop(columns=["entry_id"], axis=1, inplace=True)
            except Exception as e:
                pass
            st.dataframe(df)
            st.line_chart(df)


@st.cache
def get_data(url: str):
    return requests.get(url)


if __name__ == "__main__":
    main()
