import csv
import os
from datetime import datetime

def get_next_file_number():
    """Get the next available timetable file number"""
    i = 1
    while os.path.exists(f"timetable{i}.csv"):
        i += 1
    return i

def export_timetables_to_csv(timetables):
    """Export timetables to CSV with automatic file numbering"""
    file_number = get_next_file_number()
    filename = f"timetable{file_number}.csv"
    
    # Prepare the data in a format suitable for CSV
    csv_rows = []
    
    # Add header row
    header = ['Class', 'Day', 'Time Slot', 'Subject', 'Teacher', 'Classroom']
    csv_rows.append(header)
    
    # Add data rows
    for class_name, timetable in timetables.items():
        for day in timetable:
            for time_slot, assignments in timetable[day].items():
                if class_name in assignments:
                    assignment = assignments[class_name]
                    row = [
                        class_name,
                        day,
                        time_slot,
                        assignment['subject'],
                        assignment['teacher'],
                        assignment['classroom']
                    ]
                    csv_rows.append(row)
                else:
                    # Include empty slots in the CSV
                    row = [
                        class_name,
                        day,
                        time_slot,
                        'No Class',
                        '-',
                        '-'
                    ]
                    csv_rows.append(row)
    
    # Write to CSV file
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)
    
    return filename