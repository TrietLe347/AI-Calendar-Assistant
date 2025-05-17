import os
import json
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from ollama import chat
import re

class CalendarAssistant:
    def __init__(self, storage_file='events.json'):
        self.file = storage_file
        self.today = datetime.today().strftime("%A, %Y-%m-%d")  # e.g. "Thursday, 2025-05-15"

    def intro(self):
        print("Hello and welcome to the AI calendar assistant!")
        print(f"Todays date is {self.today}")
        print('-' * 50)


    def load_events(self):
        if not os.path.exists(self.file):
            return []
        try:
            with open(self.file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_events(self, events):
        with open(self.file, 'w') as f:
            json.dump(events, f, indent=2)

    def add_event(self, user_input):
        event = self.extract_event(user_input)
        if event:
            events = self.load_events()
            events.append(event)
            self.save_events(events)
            print("✅ Event saved:", event)
        else:
            print("❌ Could not parse the event.")

    def extract_event(self, user_input):
        today_str = datetime.today().strftime("%A, %Y-%m-%d")
        prompt = f"""
    Today is {today_str}.

    Extract a calendar event from the input below.

    Return only VALID JSON in this format (no extra text, no markdown):

    {{
      "title": "Event title",
      "date": "YYYY-MM-DD",
      "time": "HH:MM",
      "location": "City or place name"
    }}

    Assume the user means the most likely upcoming date and time if not explicit.
    Text: "{user_input}"
    """
        response = chat(model="llama3.2", messages=[
            {"role": "system", "content": "Extract calendar events as structured JSON. No extra text."},
            {"role": "user", "content": prompt}
        ])

        try:
            raw = response['message']['content']
            print("🔍 LLM raw output:\n", raw)

            json_str = self._extract_json(raw)
            event = json.loads(json_str)

            # Validate required fields
            required = ["title", "date", "time", "location"]
            bad_values = ["none", "none specified", "n/a", "null"]
            missing = [
                k for k in required
                if not event.get(k) or event[k].strip().lower() in bad_values
            ]
            if missing:
                raise ValueError(f"Missing fields: {missing}")

            # Validate date format
            parse_date(event["date"])
            return event

        except Exception as e:
            print("❌ Parsing failed:", e)
            return None

    def _extract_json(self, text):
        """
        Extracts and autocorrects the first JSON object from a string.
        Adds missing closing braces if needed.
        """
        match = re.search(r'\{[\s\S]*', text)  # match from first {
        if not match:
            return None

        json_text = match.group(0)

        # Count mismatched braces
        open_braces = json_text.count('{')
        close_braces = json_text.count('}')
        if open_braces > close_braces:
            json_text += '}' * (open_braces - close_braces)

        return json_text

    def get_upcoming_events(self):
        today = datetime.today().date()
        one_month_later = today + timedelta(days=30)
        upcoming = []
        for event in self.load_events():
            try:
                event_date = parse_date(event["date"]).date()
                if today <= event_date <= one_month_later:
                    upcoming.append(event)
            except Exception:
                continue

        return sorted(upcoming, key=lambda e: e["date"])

    def filter_by_keyword(self, keyword):
        return [
            e for e in self.load_events()
            if keyword.lower() in e["title"].lower()
        ]

    def delete_event_by_index(self, index):
        events = self.load_events()
        if 0 <= index < len(events):
            to_delete = events[index]
            confirm = input(f"❗ Confirm delete '{to_delete['title']}' on {to_delete['date']}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                events.pop(index)
                self.save_events(events)
                print("✅ Event deleted.")
            else:
                print("🚫 Deletion canceled.")
        else:
            print("❌ Invalid index.")

    def classify_input(self, user_input):
        """
        Use the LLM to classify the intent of a user's message.
        Returns: one of ['add', 'view upcoming', 'view all', 'unknown']
        """
        prompt = f"""
    You are an assistant that classifies user input into calendar commands.
    Respond with one of the following JSON values:

    "add" - if the user is describing a new event to add
    "view upcoming" - if they want to see upcoming events
    "view all" - if they want to see all saved events
    "delete" - if they want to delete or remove an event
    "unknown" - if you can't tell

    Input: "{user_input}"
    Respond with the matching string only. No explanation.
    """

        response = chat(model="llama3.2", messages=[
            {"role": "system", "content": "Classify the user's calendar-related intent."},
            {"role": "user", "content": prompt}
        ])

        intent = response['message']['content'].strip().lower()
        print(f"response: {intent}")

        return intent


