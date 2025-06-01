This repo is an agile retrospective summary app.

The key details:
- It should have a Streamlit UI app that allows a user to submit individual "what went well", "not so well" and "what could we improve" text.
- It should have a persistent store (MongoDB) to store the user responses.
- The UI should have a have a button that says "summarise retro" that when pressed will run a summarisation transformer model to take in
get all mongodb entries for well, not so well and improvements and summarise each individually.
- It should be dockerised and have a docker-compose to help run it easily.