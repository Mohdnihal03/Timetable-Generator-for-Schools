from src.generator import TimetableGenerator
from src.validators import TimetableValidator
from src.utils.export_csv import export_timetables_to_csv  # Add this new import
import json

def format_timetable_display(timetables):
    """Format timetables for display"""
    output = []
    for class_name, timetable in timetables.items():
        output.append(f"\nTimetable for {class_name}:")
        for day in timetable:
            output.append(f"\n{day}:")
            for time_slot_str in timetable[day]:
                start_time, end_time = time_slot_str.split('-')
                output.append(f"\n{start_time.strip()} - {end_time.strip()}:")
                assignments = timetable[day][time_slot_str]
                if class_name in assignments:
                    assignment = assignments[class_name]
                    output.append(f"  {class_name}: {assignment['subject']} - "
                                f"{assignment['teacher']} - {assignment['classroom']}")
                else:
                    output.append(f"  {class_name}: No class scheduled")
    return '\n'.join(output)

def main():
    # Load data
    with open('data/sample_data.json', 'r') as f:
        data = json.load(f)
        
    # Generate timetable
    generator = TimetableGenerator(
        data['teacher_data'],
        data['class_data'],
        data['classroom_data'],
        data['schedule_info']
    )
    
    timetables = generator.generate_all_timetables()
    
    # Validate timetable
    validator = TimetableValidator(timetables, data['class_data'])
    
    subject_violations = validator.validate_subject_frequencies()
    lab_violations = validator.validate_lab_hours()
    
    if subject_violations:
        print("\nSubject frequency violations:")
        for violation in subject_violations:
            print(f"{violation['class']} - {violation['subject']}: "
                  f"Required {violation['required']}, Got {violation['actual']}")
    
    if lab_violations:
        print("\nLab hours violations:")
        for violation in lab_violations:
            print(f"{violation['day']} - {violation['class']}: "
                  f"Has {violation['lab_hours']} lab hours (max is 2)")
    
    # Print formatted timetables
    print(format_timetable_display(timetables))
    
    # Export to CSV
    csv_filename = export_timetables_to_csv(timetables)
    print(f"\nTimetable exported to {csv_filename}")

if __name__ == "__main__":
    main()