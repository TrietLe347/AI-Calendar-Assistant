from datetime import datetime
import tkinter as tk
import calendar

from popup_editor import open_edit_popup


def draw_calendar(calendar_gui):
    for widget in calendar_gui.calendar_frame.winfo_children():
        widget.destroy()

    year = calendar_gui.current_date.year
    month = calendar_gui.current_date.month

    events = calendar_gui.assistant.load_events()
    event_dates = set(e["date"] for e in events if e["date"].startswith(f"{year}-{month:02}"))

    today = datetime.today().date()

    calendar_gui.calendar_header.config(text=calendar_gui.current_date.strftime("%B %Y"))

    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for i, day in enumerate(days):
        tk.Label(calendar_gui.calendar_frame, text=day, font=('Arial', 10, 'bold'), width=10).grid(row=0, column=i)

    cal = calendar.Calendar(firstweekday=6)
    row = 1

    for week in cal.monthdayscalendar(year, month):
        for col, day in enumerate(week):
            day_str = str(day) if day != 0 else ""
            if not day_str:
                cell = tk.Label(calendar_gui.calendar_frame, text="", width=10, height=4)
            else:
                this_date = f"{year}-{month:02}-{int(day):02}"

                bg_color = "white"
                if this_date in event_dates:
                    bg_color = "lightgreen"
                elif datetime(year, month, day).date() == today:
                    bg_color = "lightblue"

                cell = tk.Label(calendar_gui.calendar_frame, text=day_str, width=10, height=4,
                                borderwidth=1, relief="solid", bg=bg_color)
                # Add click binding
                cell.bind("<Button-1>", lambda e, d=this_date: show_events_for_day(calendar_gui,d))

            cell.grid(row=row, column=col, padx=1, pady=1)
        row += 1
        
        

def show_events_for_day(calendar_gui, date_str):
    events = calendar_gui.assistant.load_events()
    day_events = [e for e in events if e["date"] == date_str]

    calendar_gui.result_box.config(state=tk.NORMAL)
    calendar_gui.result_box.delete("1.0", tk.END)

    if not day_events:
        calendar_gui.result_box.insert(tk.END, f"📭 No events on {date_str}")
    else:
        calendar_gui.result_box.insert(tk.END, f"📅 Events on {date_str}:\n\n")

        for i, e in enumerate(day_events, 1):
            calendar_gui.result_box.insert(tk.END, f"{i}. {e['title']} at {e['time']} in {e['location']}\n")
            btn = tk.Button(calendar_gui.result_box, text="Edit", fg="blue", cursor="hand2",
                            command=lambda ev=e: open_edit_popup(calendar_gui,{**ev, "original_title": ev["title"]}))
            calendar_gui.result_box.window_create(tk.END, window=btn)
            calendar_gui.result_box.insert(tk.END, "\n\n")

    calendar_gui.result_box.config(state=tk.DISABLED)


def show_upcoming_events(calendar_gui):
    events = calendar_gui.assistant.get_upcoming_events()
    if not events:
        output = "📭 No upcoming events found."
    else:
        output = "📅 Upcoming Events (Next 30 Days):\n\n"
        for i, e in enumerate(events, 1):
            output += f"{i}. {e['title']} on {e['date']} at {e['time']} in {e['location']}\n"

    calendar_gui.result_box.config(state=tk.NORMAL)
    calendar_gui.result_box.delete("1.0", tk.END)
    calendar_gui.result_box.insert(tk.END, output)
    calendar_gui.result_box.config(state=tk.DISABLED)