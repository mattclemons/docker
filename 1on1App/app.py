from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import csv
import os
from fpdf import FPDF
import json

app = Flask(__name__)

DATABASE_PATH = 'data/database.db'

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS meetings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        employee_name TEXT NOT NULL,
                        notes TEXT,
                        follow_up_actions TEXT,
                        mood TEXT,
                        topics TEXT,
                        grade TEXT,
                        date_of_meeting TEXT,
                        next_meeting_date TEXT,
                        employee_goals TEXT,
                        employee_feedback TEXT,
                        action_status TEXT,
                        challenges_faced TEXT,
                        achievements TEXT,
                        skills_to_improve TEXT,
                        support_needed TEXT,
                        performance_rating TEXT,
                        engagement_level TEXT,
                        workload_assessment TEXT,
                        well_being TEXT,
                        managers_observations TEXT
                    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT employee_name, date_of_meeting, next_meeting_date, notes, follow_up_actions, topics, grade,
                      employee_goals, employee_feedback, challenges_faced, achievements, skills_to_improve, support_needed,
                      performance_rating, engagement_level, workload_assessment, well_being, managers_observations FROM meetings''')
    meetings = cursor.fetchall()
    conn.close()
    return render_template('index.html', meetings=meetings)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT mood, COUNT(*) FROM meetings GROUP BY mood')
    mood_data = cursor.fetchall()
    cursor.execute('SELECT grade, COUNT(*) FROM meetings GROUP BY grade')
    grade_data = cursor.fetchall()
    cursor.execute('SELECT employee_name, COUNT(*) FROM meetings GROUP BY employee_name')
    meeting_frequency = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', mood_data=mood_data, grade_data=grade_data, meeting_frequency=meeting_frequency)

@app.route('/add_meeting', methods=['POST'])
def add_meeting():
    try:
        employee_name = request.form['employee_name']
        notes = request.form.get('notes', '')
        follow_up_actions = request.form.get('follow_up_actions', '')
        mood = request.form.get('mood', '')
        topics = request.form.get('topics', '')
        grade = request.form.get('grade', '')
        date_of_meeting = request.form.get('date_of_meeting', '')
        next_meeting_date = request.form.get('next_meeting_date', '')
        employee_goals = request.form.get('employee_goals', '')
        employee_feedback = request.form.get('employee_feedback', '')
        action_status = request.form.get('action_status', '')
        challenges_faced = request.form.get('challenges_faced', '')
        achievements = request.form.get('achievements', '')
        skills_to_improve = request.form.get('skills_to_improve', '')
        support_needed = request.form.get('support_needed', '')
        performance_rating = request.form.get('performance_rating', '')
        engagement_level = request.form.get('engagement_level', '')
        workload_assessment = request.form.get('workload_assessment', '')
        well_being = request.form.get('well_being', '')
        managers_observations = request.form.get('managers_observations', '')

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO meetings (employee_name, notes, follow_up_actions, mood, topics, grade, date_of_meeting, next_meeting_date, 
                          employee_goals, employee_feedback, action_status, challenges_faced, achievements, skills_to_improve, support_needed, 
                          performance_rating, engagement_level, workload_assessment, well_being, managers_observations) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (employee_name, notes, follow_up_actions, mood, topics, grade, date_of_meeting, next_meeting_date, employee_goals, employee_feedback, 
                        action_status, challenges_faced, achievements, skills_to_improve, support_needed, performance_rating, engagement_level, workload_assessment, 
                        well_being, managers_observations))
        conn.commit()
        conn.close()

    except KeyError as e:
        return f"Missing form field: {str(e)}", 400

    return redirect('/')

@app.route('/export_csv')
def export_csv():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT employee_name, date_of_meeting, next_meeting_date, notes, follow_up_actions, topics, grade,
                      employee_goals, employee_feedback, challenges_faced, achievements, skills_to_improve, support_needed,
                      performance_rating, engagement_level, workload_assessment, well_being, managers_observations FROM meetings''')
    meetings = cursor.fetchall()
    conn.close()

    with open('meetings.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Employee Name', 'Date of Meeting', 'Next Meeting Date', 'Notes', 'Follow-up Actions', 'Topics', 'Grade',
                             'Employee Goals', 'Employee Feedback', 'Challenges Faced', 'Achievements', 'Skills to Improve',
                             'Support Needed', 'Performance Rating', 'Engagement Level', 'Workload Assessment', 'Well-being',
                             'Managers Observations'])
        csv_writer.writerows(meetings)

    return send_file('meetings.csv', as_attachment=True)

@app.route('/export_pdf')
def export_pdf():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT employee_name, date_of_meeting, next_meeting_date, notes, follow_up_actions, topics, grade,
                      employee_goals, employee_feedback, challenges_faced, achievements, skills_to_improve, support_needed,
                      performance_rating, engagement_level, workload_assessment, well_being, managers_observations FROM meetings''')
    meetings = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Employee 1-on-1 Meeting Summary', ln=True, align='C')

    pdf.set_font('Arial', size=12)
    for meeting in meetings:
        pdf.cell(200, 10, txt=f'Employee Name: {meeting[0]}', ln=True)
        pdf.cell(200, 10, txt=f'Date of Meeting: {meeting[1]}', ln=True)
        pdf.cell(200, 10, txt=f'Next Meeting Date: {meeting[2]}', ln=True)
        pdf.cell(200, 10, txt=f'Notes: {meeting[3]}', ln=True)
        pdf.cell(200, 10, txt=f'Follow-up Actions: {meeting[4]}', ln=True)
        pdf.cell(200, 10, txt=f'Topics: {meeting[5]}', ln=True)
        pdf.cell(200, 10, txt=f'Grade: {meeting[6]}', ln=True)
        pdf.cell(200, 10, txt=f'Employee Goals: {meeting[7]}', ln=True)
        pdf.cell(200, 10, txt=f'Employee Feedback: {meeting[8]}', ln=True)
        pdf.cell(200, 10, txt=f'Challenges Faced: {meeting[9]}', ln=True)
        pdf.cell(200, 10, txt=f'Achievements: {meeting[10]}', ln=True)
        pdf.cell(200, 10, txt=f'Skills to Improve: {meeting[11]}', ln=True)
        pdf.cell(200, 10, txt=f'Support Needed: {meeting[12]}', ln=True)
        pdf.cell(200, 10, txt=f'Performance Rating: {meeting[13]}', ln=True)
        pdf.cell(200, 10, txt=f'Engagement Level: {meeting[14]}', ln=True)
        pdf.cell(200, 10, txt=f'Workload Assessment: {meeting[15]}', ln=True)
        pdf.cell(200, 10, txt=f'Well-being: {meeting[16]}', ln=True)
        pdf.cell(200, 10, txt=f'Managers Observations: {meeting[17]}', ln=True)
        pdf.cell(200, 10, txt=' ', ln=True)

    pdf_file_path = 'meetings.pdf'
    pdf.output(pdf_file_path)

    return send_file(pdf_file_path, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
