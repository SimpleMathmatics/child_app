import streamlit as st
import pandas as pd
from timeline_utils import TimelineUtils as tu


# ----------------------------------Select Options for Sidebar ----------------------------------
st.sidebar.image("img/SOS-Logo.png", use_column_width=True)
child_id = st.sidebar.text_input('Please input a Child ID! (e.g d1b84a3b-6096-4703-bbb7-78084be5252f for Mitzi)')
st.sidebar.subheader("Go to:")
tab = st.sidebar.radio("Please select a tab!", ("Timeline", "Overview", "Details"))

# -----------------------------------------------------------------------------------------------
tu = tu()

@st.cache(allow_output_mutation=True)
def get_data():
    df = pd.read_parquet(path="data/ChildEvents_1.parquet", engine="pyarrow")
    df = tu.add_childid_colum(df=df)
    return df



plot = tu.create_timeline(childIDs=[child_id], df=get_data())

if plot == -1:
    """
    ## No plot could be generated:
    """
    "### ", "No Child with the ID: ", child_id, " found"

elif plot is None:
    "### ", "Please select a valid Child ID and push the generation button!"

elif type(plot).__name__ == "Figure":
    if tab == "Timeline":
        st.title("SOS Kinderdorf - Child Timeline")
        st.plotly_chart(plot)
    elif tab == "Overview":
        st.title("SOS Kinderdorf - Child Overview")
        st.image(image="img/SOS_Kinderdorf_Overview.png", use_column_width=True)
    else:
        st.title("SOS Kinderdorf - Child Details")
        st.image(image="img/SOS_Kinderdorf.png", use_column_width=True)
else:
    pass
