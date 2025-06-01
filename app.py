import os
import streamlit as st
from pymongo import MongoClient
from transformers import pipeline

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["retro_summaries"]


def insert_response(well, not_well, improvement):
    if well and well.strip():
        db.went_well.insert_one({"text": well})
    if not_well and not_well.strip():
        db.not_well.insert_one({"text": not_well})
    if improvement and improvement.strip():
        db.improvements.insert_one({"text": improvement})


def summarize_responses():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", do_sample=False)
    well_entries = list(db.went_well.find({}, {"text": 1}))
    not_well_entries = list(db.not_well.find({}, {"text": 1}))
    improvement_entries = list(db.improvements.find({}, {"text": 1}))

    well_text = " ".join([entry["text"] for entry in well_entries])
    not_well_text = " ".join([entry["text"] for entry in not_well_entries])
    improvement_text = " ".join([entry["text"] for entry in improvement_entries])

    well_summary = summarizer(well_text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
    not_well_summary = summarizer(not_well_text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
    improvement_summary = summarizer(improvement_text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]

    return well_summary, not_well_summary, improvement_summary
def clear_responses():
    db.went_well.delete_many({})
    db.not_well.delete_many({})
    db.improvements.delete_many({})

st.title("Agile Retrospective Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("What went well?")
    well_cursor = db.went_well.find({}, {"text": 1}).sort("_id", -1).limit(3)
    for entry in well_cursor:
        st.write("- " + entry.get("text", ""))
with col2:
    st.subheader("What did not go well?")
    not_well_cursor = db.not_well.find({}, {"text": 1}).sort("_id", -1).limit(3)
    for entry in not_well_cursor:
        st.write("- " + entry.get("text", ""))
with col3:
    st.subheader("What could we improve?")
    improvement_cursor = db.improvements.find({}, {"text": 1}).sort("_id", -1).limit(3)
    for entry in improvement_cursor:
        st.write("- " + entry.get("text", ""))

with st.form("response_form"):
    well = st.text_area("What went well?")
    not_well = st.text_area("What did not go well?")
    improvement = st.text_area("What could we improve?")
    submit = st.form_submit_button("Submit")
    if submit:
        insert_response(well, not_well, improvement)
        st.success("Response submitted!")

if st.button("Summarise Retro"):
    well_summary, not_well_summary, improvement_summary = summarize_responses()
    st.write("Well Summary:", well_summary)
    st.write("Not Well Summary:", not_well_summary)
    st.write("Improvement Summary:", improvement_summary)

if st.button("Clear all responses"):
    clear_responses()
    st.warning("All responses have been cleared.")
