from datetime import datetime, timedelta

def parse_time(time_str):
    """Convert time string to datetime object"""
    return datetime.strptime(time_str, "%I:%M %p")

def format_time(dt):
    """Convert datetime object to string format"""
    return dt.strftime("%I:%M %p")

def generate_time_slots(schedule_info):
    """Generate time slots based on schedule info"""
    slots = []
    current_time = parse_time(schedule_info['start_time'])
    end_time = parse_time(schedule_info['end_time'])
    duration = timedelta(minutes=schedule_info['class_duration'])
    
    snack_break_start = parse_time(schedule_info['snack_break']['start'])
    snack_break_end = parse_time(schedule_info['snack_break']['end'])
    lunch_break_start = parse_time(schedule_info['lunch_break']['start'])
    lunch_break_end = parse_time(schedule_info['lunch_break']['end'])
    
    while current_time + duration <= end_time:
        slot_end = current_time + duration
        
        # Skip break times
        if not (
            (current_time <= snack_break_start < slot_end) or
            (current_time <= lunch_break_start < slot_end)
        ):
            slots.append({
                'start': format_time(current_time),
                'end': format_time(slot_end)
            })
            
        if slot_end <= snack_break_start:
            current_time = slot_end
        elif current_time < snack_break_end:
            current_time = snack_break_end
        elif slot_end <= lunch_break_start:
            current_time = slot_end
        elif current_time < lunch_break_end:
            current_time = lunch_break_end
        else:
            current_time = slot_end
            
    return slots