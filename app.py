 import streamlit as st
    from pymongo import MongoClient
    from transformers import pipeline

    # MongoDB setup
    client = MongoClient('mongodb://localhost:27017/')
    db = client['retro_summaries']

    def insert_response(well, not_well, improvement):
        db.responses.insert_one({
            'what_went_well': well,
            'not_well': not_well,
            'improvement': improvement
        })

    def summarize_responses():
        summarizer = pipeline('summarization')
        well_entries = list(db.responses.find({}, {'what_went_well': 1}))
        not_well_entries = list(db.responses.find({}, {'not_well': 1}))
        improvement_entries = list(db.responses.find({}, {'improvement': 1}))

        # Concatenate entries for summarization
        well_summary = summarizer(' '.join([entry['what_went_well'] for entry in well_entries]), max_length=130, min_length=30, do_sample=False)
        not_well_summary = summarizer(' '.join([entry['not_well'] for entry in not_well_entries]), max_length=130, min_length=30, do_sample=False)
        improvement_summary = summarizer(' '.join([entry['improvement'] for entry in improvement_entries]), max_length=130, min_length=30, do_sample=False)

        return well_summary, not_well_summary, improvement_summary

    st.title('Agile Retrospective Summary')

    with st.form('response_form'):
        well = st.text_area('What went well?')
        not_well = st.text_area('What did not go well?')
        improvement = st.text_area('What could we improve?')
        submit = st.form_submit_button('Submit')
        if submit:
            insert_response(well, not_well, improvement)
            st.success('Response submitted!')

    if st.button('Summarise Retro'):
        well_summary, not_well_summary, improvement_summary = summarize_responses()
        st.write('Well Summary:', well_summary)
        st.write('Not Well Summary:', not_well_summary)
        st.write('Improvement Summary:', improvement_summary)