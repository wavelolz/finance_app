import streamlit as st
from google.cloud import firestore
import pandas as pd

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("testing.json")

# Create a reference to the Google post.
doc_ref = db.collection("test").document("stock_id_123")

# Then get the data at that reference.
doc = doc_ref.get()

data = doc.to_dict()["data"]
df = pd.DataFrame(data)
st.dataframe(df)
# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())
