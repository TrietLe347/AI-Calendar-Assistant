import tkinter as tk
from datetime import datetime, timedelta
from calendar_assistant import CalendarAssistant
import tkinter.messagebox as messagebox


from calendar_views import draw_calendar, show_upcoming_events


class CalendarGUI:
    def __init__(self, root):
        self.assistant = CalendarAssistant()
        self.root = root
        self.root.title("AI Calendar Assistant")

        # === Layout frames ===
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)

        # === Calendar Header + Nav ===
        self.current_date = datetime.today().replace(day=1)
        self.calendar_header = tk.Label(self.left_frame, font=('Arial', 16))
        self.calendar_header.pack()

        nav_frame = tk.Frame(self.left_frame)
        nav_frame.pack()

        tk.Button(nav_frame, text="←", command=self.prev_month).pack(side=tk.LEFT)
        tk.Button(nav_frame, text="→", command=self.next_month).pack(side=tk.LEFT)

        self.calendar_frame = tk.Frame(self.left_frame)
        self.calendar_frame.pack()

        draw_calendar(self)

        # === Chatbot Interface ===
        tk.Label(self.right_frame, text="🧠 AI Input", font=('Arial', 12)).pack(anchor='w')

        self.chat_input = tk.Text(self.right_frame, height=3, width=80)
        self.chat_input.pack()

        self.send_button = tk.Button(self.right_frame, text="Send to Assistant", command=self.handle_chat)
        self.send_button.pack(pady=5)

        tk.Label(self.right_frame, text="🧾 Result", font=('Arial', 12)).pack(anchor='w')

        self.result_box = tk.Text(self.right_frame, height=10, width=80,  state=tk.DISABLED)
        self.result_box.pack()
        show_upcoming_events(self)


    def prev_month(self):
        self.current_date = (self.current_date - timedelta(days=1)).replace(day=1)
        draw_calendar(self)

    def next_month(self):
        year = self.current_date.year + (self.current_date.month // 12)
        month = (self.current_date.month % 12) + 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        draw_calendar(self)



    def handle_chat(self):
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)

        user_input = self.chat_input.get("1.0", tk.END).strip()
        self.chat_input.delete("1.0", tk.END)

        if not user_input:
            self.result_box.insert(tk.END, "⚠️ Please enter something.")
            self.result_box.config(state=tk.DISABLED)
            return

        # Ask AI to classify intent
        intent = self.assistant.classify_input(user_input)

        if "delete" in intent:
            # Try to identify which event they want to delete
            all_events = self.assistant.load_events()
            if not all_events:
                self.result_box.insert(tk.END, "📭 No events to delete.")
                return

            matched = [
                e for e in all_events if any(
                    keyword in user_input.lower() for keyword in [e['title'].lower(), e['date'], e['location'].lower()]
                )
            ]

            if not matched:
                self.result_box.insert(tk.END, "❌ I couldn't find a matching event to delete.")
            elif len(matched) == 1:
                confirm = messagebox.askyesno("Confirm Delete",
                                                 f"Delete event:\n\n{matched[0]['title']} on {matched[0]['date']}?")
                if confirm:
                    all_events.remove(matched[0])
                    self.assistant.save_events(all_events)
                    self.result_box.insert(tk.END, f"🗑️ Deleted: {matched[0]['title']} on {matched[0]['date']}")

                    draw_calendar(self)
            else:
                self.result_box.insert(tk.END, "⚠️ Multiple matching events found. Be more specific.")

        elif "view upcoming" in intent:
            events = self.assistant.get_upcoming_events()
            if not events:
                self.result_box.insert(tk.END, "📭 No upcoming events found.")
            else:
                self.result_box.insert(tk.END, "📅 Upcoming Events (Next 30 Days):\n\n")
                for i, e in enumerate(events, 1):
                    self.result_box.insert(tk.END,
                                           f"{i}. {e['title']} on {e['date']} at {e['time']} in {e['location']}\n")

        elif "view all" in intent:
            events = self.assistant.load_events()
            if not events:
                self.result_box.insert(tk.END, "📭 No events saved.")
            else:
                self.result_box.insert(tk.END, "📋 All Events:\n\n")
                for i, e in enumerate(events, 1):
                    self.result_box.insert(tk.END,
                                           f"{i}. {e['title']} on {e['date']} at {e['time']} in {e['location']}\n")

        elif "add" in intent:
            event = self.assistant.extract_event(user_input)
            if event:
                events = self.assistant.load_events()
                events.append(event)
                self.assistant.save_events(events)

                self.result_box.insert(tk.END, f"✅ Event added:\n\n")
                self.result_box.insert(tk.END, f"Title: {event['title']}\n")
                self.result_box.insert(tk.END, f"Date: {event['date']}\n")
                self.result_box.insert(tk.END, f"Time: {event['time']}\n")
                self.result_box.insert(tk.END, f"Location: {event['location']}\n")

                draw_calendar(self)
            else:
                self.result_box.insert(tk.END, "❌ Failed to parse the event.")

        else:
            self.result_box.insert(tk.END, "🤔 I didn't understand that. Try rephrasing.")

        self.result_box.config(state=tk.DISABLED)

    def refresh_calendar(self):
        draw_calendar(self)

    def refresh_day_view(self, date_str):
        from calendar_views import show_events_for_day  # ✅ Import locally to avoid circular import
        show_events_for_day(self, date_str)







