import tkinter as tk
import re


import tkinter.messagebox as messagebox


def open_edit_popup(calendar_gui, event_data):
    popup = tk.Toplevel(calendar_gui.root)
    popup.title(f"Edit Event on {event_data['date']}")
    popup.geometry("300x300")

    popup.transient(calendar_gui.root)
    popup.grab_set()
    popup.focus_force()

    popup.update_idletasks()

    # Get main window position and size
    main_x = calendar_gui.root.winfo_x()
    main_y = calendar_gui.root.winfo_y()
    main_w = calendar_gui.root.winfo_width()
    main_h = calendar_gui.root.winfo_height()

    # Get popup size
    popup_w = popup.winfo_width()
    popup_h = popup.winfo_height()

    # Calculate center position relative to main window
    x = main_x + (main_w // 2) - (popup_w // 2)
    y = main_y + (main_h // 2) - (popup_h // 2)

    popup.geometry(f"+{x}+{y}")

    tk.Label(popup, text="Title").pack()
    title_entry = tk.Entry(popup)
    title_entry.insert(0, event_data["title"])
    title_entry.pack()

    tk.Label(popup, text="Time (HH:MM)").pack()
    time_entry = tk.Entry(popup)
    time_entry.insert(0, event_data["time"])
    time_entry.pack()

    tk.Label(popup, text="Location").pack()
    location_entry = tk.Entry(popup)
    location_entry.insert(0, event_data["location"])
    location_entry.pack()

    def is_valid_time(time_str):
        return re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_str) is not None

    def save_changes():
        new_title = title_entry.get().strip()
        new_time = time_entry.get().strip()
        new_location = location_entry.get().strip()

        if not is_valid_time(new_time):
            tk.messagebox.showerror("Invalid Time", "Time must be in HH:MM format (24-hour).")
            return

        events = calendar_gui.assistant.load_events()

        for i, e in enumerate(events):
            if (
                    e["date"] == event_data["date"]
                    and e["title"] == event_data["original_title"]
                    and e["time"] == event_data["time"]
                    and e["location"] == event_data["location"]
            ):
                events[i] = {
                    "title": new_title,
                    "date": event_data["date"],
                    "time": new_time,
                    "location": new_location,
                }
                calendar_gui.assistant.save_events(events)
                popup.destroy()
                calendar_gui.refresh_calendar()
                calendar_gui.refresh_day_view(event_data["date"])
                return

        tk.messagebox.showerror("Error", "Event not found. It may have been renamed or deleted.")

    def delete_event():
        confirm = tk.messagebox.askyesno("Delete Event", "Are you sure you want to delete this event?")
        if not confirm:
            return

        events = calendar_gui.assistant.load_events()
        new_events = [
            e for e in events
            if not (
                    e["date"] == event_data["date"]
                    and e["title"] == event_data["original_title"]
                    and e["time"] == event_data["time"]
                    and e["location"] == event_data["location"]
            )
        ]

        calendar_gui.assistant.save_events(new_events)
        popup.destroy()
        calendar_gui.refresh_calendar()
        calendar_gui.refresh_day_view(event_data["date"])

    def cancel():
        popup.destroy()

    # Buttons
    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Save", command=save_changes).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_event, fg="red").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
