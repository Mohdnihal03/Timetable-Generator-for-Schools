class ConstraintsChecker:
    def __init__(self, teacher_data, class_data, classroom_data, schedule_info):
        self.teacher_data = teacher_data
        self.class_data = class_data
        self.classroom_data = classroom_data
        self.schedule_info = schedule_info
        
    def check_consecutive_classes(self, schedule, day, time_slot_key, class_name, subject):
        """Check if this would create too many consecutive classes of the same subject"""
        # Get all time slots
        time_slots = list(schedule[day].keys())
        current_slot_index = time_slots.index(time_slot_key)
        
        # Check previous 2 slots
        consecutive_count = 0
        for i in range(max(0, current_slot_index - 2), current_slot_index):
            slot = time_slots[i]
            if (class_name in schedule[day][slot] and 
                schedule[day][slot][class_name].get('subject') == subject):
                consecutive_count += 1
                
        # More than 2 consecutive classes of same subject not allowed
        return consecutive_count < 2
    
    def check_daily_subject_limit(self, schedule, day, class_name, subject):
        """Check if adding this subject would exceed daily limit"""
        daily_count = sum(
            1 for slot in schedule[day].values()
            if class_name in slot and slot[class_name].get('subject') == subject
        )
        return daily_count < 2  # Maximum 2 classes of same subject per day
    
    def check_teacher_availability(self, teacher, day, time_slot_key, schedule):
        """Check if teacher is available at this time"""
        # Check if teacher is already teaching
        for class_schedule in schedule[day][time_slot_key].values():
            if class_schedule.get('teacher') == teacher['name']:
                return False
                
        # Check teacher's daily hours
        daily_hours = sum(
            1 for slot in schedule[day].values()
            for assignment in slot.values()
            if assignment.get('teacher') == teacher['name']
        )
        
        return daily_hours < teacher['max_hours_per_day']
    
    def check_room_availability(self, room, day, time_slot_key, schedule):
        """Check if room is available at this time"""
        for class_schedule in schedule[day][time_slot_key].values():
            if class_schedule.get('classroom') == room['name']:
                return False
        return True
    
    def check_specialized_room(self, room, subject):
        """Check if room is suitable for the subject"""
        if 'Lab' in subject:
            return ('specialized_for' in room and 
                   subject in room['specialized_for'])
        return True
    
    def check_valid_time_slot(self, time_slot_key):
        """Check if this is a valid time slot (not during breaks)"""
        start_time = time_slot_key.split('-')[0].strip()
        
        # Convert break times to comparable format
        snack_break_start = self.schedule_info['snack_break']['start']
        lunch_break_start = self.schedule_info['lunch_break']['start']
        
        return not (start_time == snack_break_start or 
                   start_time == lunch_break_start)
    
    def check_all_constraints(self, schedule, day, time_slot_key, class_info, 
                            subject, teacher, room):
        """Check all constraints at once"""
        return all([
            self.check_consecutive_classes(schedule, day, time_slot_key, 
                                        class_info['name'], subject),
            self.check_daily_subject_limit(schedule, day, class_info['name'], 
                                         subject),
            self.check_teacher_availability(teacher, day, time_slot_key, schedule),
            self.check_room_availability(room, day, time_slot_key, schedule),
            self.check_specialized_room(room, subject),
            self.check_valid_time_slot(time_slot_key)
        ])