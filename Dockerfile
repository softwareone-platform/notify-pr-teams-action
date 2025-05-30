FROM python:3.9-slim

LABEL "com.github.actions.name"="Notify Pull Request Teams Action"
LABEL "com.github.actions.description"="Sends PR notification to Microsoft Teams"
LABEL "com.github.actions.icon"="message-circle"
LABEL "com.github.actions.color"="blue"

COPY notify_teams.py /app/notify_teams.py
RUN pip install requests

ENTRYPOINT ["python", "/app/notify_teams.py"] 