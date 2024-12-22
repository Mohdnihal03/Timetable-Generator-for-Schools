class TimetableValidator:
    def __init__(self, schedule, class_data):
        self.schedule = schedule
        self.class_data = class_data

    def validate_subject_frequencies(self):
        violations = []
        
        for class_info in self.class_data:
            subject_counts = {subject: 0 for subject in class_info['weekly_subject_frequency']}
            
            # Count actual frequencies in one loop
            for day in self.schedule:
                for time_slot in self.schedule[day]:
                    assignment = self.schedule[day][time_slot].get(class_info['name'])
                    if assignment:
                        subject = assignment['subject']
                        if subject in subject_counts:
                            subject_counts[subject] += 1
            
            # Check against required frequencies
            for subject, req_freq in class_info['weekly_subject_frequency'].items():
                actual_freq = subject_counts.get(subject, 0)
                if actual_freq != req_freq:
                    violations.append({
                        'class': class_info['name'],
                        'subject': subject,
                        'required': req_freq,
                        'actual': actual_freq,
                        'details': [(day, time_slot) for day in self.schedule for time_slot in self.schedule[day] if self.schedule[day][time_slot].get(class_info['name'], {}).get('subject') == subject]
                    })
        
        return violations

    def validate_lab_hours(self):
        violations = []
        
        for day in self.schedule:
            for class_info in self.class_data:
                lab_count = sum(
                    1 for slot in self.schedule[day].values()
                    for assignment in slot.values()
                    if (assignment.get('class') == class_info['name'] and 
                        'Lab' in assignment.get('subject', ''))
                )
                
                if lab_count > 2:
                    violations.append({
                        'day': day,
                        'class': class_info['name'],
                        'lab_hours': lab_count
                    })
        
        return violations
