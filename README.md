# 🧠 AI Calendar Assistant

A Python desktop calendar assistant built with `Tkinter`, powered by an LLM (Ollama), allowing users to manage events using natural language.

## ✨ Features

- 📅 Monthly calendar view with clickable day boxes
- 🧠 Natural language input (e.g. _"I have a meeting next Friday at 2pm in San Diego"_)
- ✅ LLM-powered intent classification: add, view, delete events
- 🔍 View upcoming events (next 30 days)
- ✏️ Edit or delete events via popup
- 🎨 Highlights today's date and days with events
- 💬 Built-in chatbot interface for commands like:
  - `"view upcoming"`
  - `"delete lunch with John"`
  - `"show all events"`

## 📁 File Structure

```
project/
│
├── main.py                  # Launches the GUI
├── calender_gui.py          # Main GUI layout and chatbot integration
├── calendar_views.py        # Calendar rendering and date interactions
├── popup_editor.py          # Popup window for editing/deleting events
├── calendar_assistant.py    # LLM integration for parsing and intent detection
├── events.json              # Stored event data
└── README.md                # Project documentation
```

## 🧪 How It Works

1. User types: _"Dinner with mom next Saturday at 7pm in San Diego"_
2. The LLM parses it into structured event JSON
3. The assistant saves it into `events.json`
4. The calendar refreshes and highlights that day
5. Clicking a date shows all events for that day

## 🛠️ Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) installed with a local model (e.g. `llama3`)
- The following Python libraries:
  - `tkinter`
  - `json`
  - `re`
  - `datetime`
  - `calendar`

## 🚀 Getting Started

1. Install [Ollama](https://ollama.com/)
2. Start a model:
   ```
   ollama run llama3
   ```
3. Run the app:
   ```
   python main.py
   ```

## 🧠 Model Prompting

Uses structured prompts to extract events as:
```json
{
  "title": "Dinner with Mom",
  "date": "2025-05-23",
  "time": "19:00",
  "location": "San Diego"
}
```

Also includes a lightweight intent classifier to handle commands like `"view upcoming"` or `"delete event"`.

## 📌 Future Improvements

- Recurring events
- Timezone and date localization
- Drag-to-add events
- Sync with Google Calendar or Outlook
- Advanced natural language (e.g. "every Monday at 5pm")

## 📃 License

MIT License
