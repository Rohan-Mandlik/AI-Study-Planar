# app/planner.py
from datetime import datetime, timedelta
import random
from fpdf import FPDF
import os
from collections import defaultdict

def generate_study_plan(subjects, exam_date_str, hours_per_day, intensity):
    try:
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    today = datetime.today().date()
    days_left = (exam_date.date() - today).days
    if days_left < 1:
        raise ValueError("Exam date must be at least one day ahead.")

    subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
    if not subject_list:
        raise ValueError("At least one subject is required.")

    total_study_hours = days_left * hours_per_day
    total_subjects = len(subject_list)

    # Step 1: Distribute hours across subjects
    base_hours_per_subject = total_study_hours // total_subjects
    remainder = total_study_hours % total_subjects

    subject_hours = defaultdict(int)
    for subj in subject_list:
        extra = 1 if remainder > 0 else 0
        subject_hours[subj] = base_hours_per_subject + extra
        remainder -= extra

    # Step 2: Plan days
    plan = {}
    current_day = today

    for _ in range(days_left):
        day_plan = []
        daily_total = 0
        num_topics = {
            "Light": 1,
            "Moderate": 2,
            "Intense": random.randint(2, 3)
        }.get(intensity, 2)

        assigned = set()
        remaining_subjs = [s for s in subject_list if subject_hours[s] > 0]

        while len(day_plan) < num_topics and remaining_subjs:
            subj = random.choice(remaining_subjs)
            if subj in assigned:
                remaining_subjs.remove(subj)
                continue

            max_hours = min(subject_hours[subj], hours_per_day - daily_total, 8)
            if max_hours <= 0:
                remaining_subjs.remove(subj)
                continue

            assign_hours = random.randint(1, max_hours)
            subject_hours[subj] -= assign_hours
            daily_total += assign_hours
            day_plan.append(f"{subj} ({assign_hours} hrs)")
            assigned.add(subj)

        # Fill up remaining hours if needed
        fill_subjs = [s for s in subject_list if subject_hours[s] > 0]
        while daily_total < hours_per_day and fill_subjs:
            subj = random.choice(fill_subjs)
            max_hours = min(subject_hours[subj], hours_per_day - daily_total)
            if max_hours <= 0:
                fill_subjs.remove(subj)
                continue
            assign_hours = max(1, min(max_hours, random.randint(1, max_hours)))
            subject_hours[subj] -= assign_hours
            daily_total += assign_hours
            day_plan.append(f"{subj} ({assign_hours} hrs)")

        plan[current_day.strftime("%A, %B %d")] = day_plan
        current_day += timedelta(days=1)

    return plan

def generate_pdf(study_plan, filename="study_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    
    sorted_days = sorted(
        study_plan.keys(),
        key=lambda d: datetime.strptime(d.split(",")[1], " %B %d")  
    )

    pdf.cell(200, 10, txt="Study Plan", ln=True, align='C')
    pdf.ln(10)

    for day in sorted_days:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, day, border=1, ln=True)
        pdf.set_font("Arial", size=10)
        for topic in study_plan[day]:
            pdf.cell(0, 8, f"- {topic}", ln=True)
        pdf.ln(2)

    filepath = os.path.join("exports", filename)
    pdf.output(filepath)
    return filepath

# study_plan = generate_study_plan("Math", "2025-07-8", 2, "Moderate")
# print(f"Generated Study Plan: {study_plan}")
# print(f"Type of study_plan: {type(study_plan)}")
