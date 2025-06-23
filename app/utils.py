import bleach
from datetime import datetime

def sanitize_input(text):
    return bleach.clean(text)

def validate_date(date_text):
    try:
        dt = datetime.strptime(date_text, "%Y-%m-%d")
        if dt.date() < datetime.today().date():
            return False, "Date cannot be in the past."
        return True, dt
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

def escape_html(text):
    return text.replace("<", "<").replace(">", ">")