# Architecture
Streamlit UI (`app.py`) calls local Python modules. The message analyzer uses transparent keyword/URL heuristics. Timer and incident notes use Streamlit session state. No external AI API or real notification service is connected.
Production needs authentication, secure storage, consent, tested delivery, threat modelling, accessibility testing, and evaluation for false positives/negatives.
