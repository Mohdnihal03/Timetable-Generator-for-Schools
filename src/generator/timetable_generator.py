from ..constraints import ConstraintsChecker
from ..utils.time_utils import generate_time_slots

class TimetableGenerator:
    def __init__(self, teacher_data, class_data, classroom_data, schedule_info):
        self.teacher_data = teacher_data
        self.class_data = class_data
        self.classroom_data = classroom_data
        self.schedule_info = schedule_info
        self.constraints = ConstraintsChecker(
            teacher_data, class_data, classroom_data, schedule_info
        )
        self.time_slots = generate_time_slots(schedule_info)

    def initialize_schedule(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        time_slot_keys = [f"{slot['start']}-{slot['end']}" for slot in self.time_slots]
        return {
            day: {
                time_slot_key: {} 
                for time_slot_key in time_slot_keys
            } for day in days
        }

    def find_teacher_for_subject(self, subject, day, time_slot_key, current_schedule):
        for teacher in self.teacher_data:
            if subject in teacher['subjects']:
                # Check if teacher is already assigned at this time
                is_available = True
                for class_schedule in current_schedule[day][time_slot_key].values():
                    if class_schedule.get('teacher') == teacher['name']:
                        is_available = False
                        break
                
                if is_available:
                    # Count teacher's daily hours
                    daily_hours = 0
                    for slot in current_schedule[day].values():
                        for assignment in slot.values():
                            if assignment.get('teacher') == teacher['name']:
                                daily_hours += 1
                    
                    if daily_hours < teacher['max_hours_per_day']:
                        return teacher
        return None

    def find_room_for_subject(self, subject, class_info, day, time_slot_key, current_schedule):
        for room in self.classroom_data:
            # Check if room has enough capacity
            if room['capacity'] < class_info['size']:
                continue
                
            # Check if room is specialized for the subject if needed
            if 'Lab' in subject:
                if 'specialized_for' not in room or subject not in room['specialized_for']:
                    continue
                    
            # Check if room is already in use at this time
            is_available = True
            for assignment in current_schedule[day][time_slot_key].values():
                if assignment.get('classroom') == room['name']:
                    is_available = False
                    break
                    
            if is_available:
                return room
        return None

    def generate_timetable_for_class(self, class_info):
        schedule = self.initialize_schedule()
        
        for subject, freq in class_info['weekly_subject_frequency'].items():
            assigned = 0
            attempts = 0
            max_attempts = 1000
            
            while assigned < freq and attempts < max_attempts:
                attempts += 1
                for day in schedule:
                    if assigned >= freq:
                        break
                        
                    # Check lab hours for the day
                    if 'Lab' in subject:
                        lab_hours = sum(
                            1 for slot in schedule[day].values()
                            for assignment in slot.values()
                            if assignment.get('subject', '').endswith('Lab')
                        )
                        if lab_hours >= 2:  # Maximum 2 lab hours per day
                            continue
                    
                    for time_slot in self.time_slots:
                        if assigned >= freq:
                            break
                            
                        time_slot_key = f"{time_slot['start']}-{time_slot['end']}"
                        
                        if class_info['name'] not in schedule[day][time_slot_key]:
                            teacher = self.find_teacher_for_subject(
                                subject, day, time_slot_key, schedule
                            )
                            if not teacher:
                                continue
                                
                            room = self.find_room_for_subject(
                                subject, class_info, day, time_slot_key, schedule
                            )
                            if not room:
                                continue
                                
                            schedule[day][time_slot_key][class_info['name']] = {
                                'subject': subject,
                                'teacher': teacher['name'],
                                'classroom': room['name']
                            }
                            assigned += 1
                            
            if assigned < freq:
                print(f"Warning: Could not assign all periods for {subject} in {class_info['name']}. "
                      f"Assigned {assigned}/{freq}")
                
        return schedule

    def generate_all_timetables(self):
        all_timetables = {}
        for class_info in self.class_data:
            all_timetables[class_info['name']] = self.generate_timetable_for_class(class_info)
        return all_timetables