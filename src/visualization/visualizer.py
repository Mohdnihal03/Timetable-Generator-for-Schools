import numpy as np
import plotly.express as px

class TimetableVisualizer:
    def __init__(self, schedule, class_data, classroom_data):
        self.schedule = schedule
        self.class_data = class_data
        self.classroom_data = classroom_data

    def create_gantt_chart(self):
        """Create a Gantt chart visualization of the timetable"""
        df = []
        
        for day in self.schedule:
            for time_slot in self.schedule[day]:
                for class_name, assignment in self.schedule[day][time_slot].items():
                    if assignment:
                        df.append(dict(
                            Task=class_name,
                            Start=f"{day} {time_slot['start']}",
                            Finish=f"{day} {time_slot['end']}",
                            Resource=assignment['subject']
                        ))

        fig = ff.create_gantt(df, 
                            group_tasks=True,
                            showgrid_x=True,
                            showgrid_y=True)
        
        fig.update_layout(
            title="School Timetable",
            height=800
        )
        
        return fig

    def create_heatmap(self):
        """Create a heatmap visualization of classroom utilization"""
        # Create a grid of classrooms vs time slots
        classrooms = [room['name'] for room in self.classroom_data]
        time_slots = [f"{slot['start']}-{slot['end']}" for slot in self.schedule[next(iter(self.schedule))]]
        
        # Initialize matrix to store occupancy data
        heatmap_data = np.zeros((len(time_slots), len(classrooms)))
        
        for day in self.schedule:
            for time_slot in self.schedule[day]:
                for class_name, assignment in self.schedule[day][time_slot].items():
                    if assignment:
                        room_index = classrooms.index(assignment['classroom'])
                        time_index = time_slots.index(f"{time_slot['start']}-{time_slot['end']}")
                        heatmap_data[time_index][room_index] += 1
        
        # Create heatmap
        fig = px.imshow(heatmap_data, 
                        labels=dict(x="Classrooms", y="Time Slots"), 
                        x=classrooms, 
                        y=time_slots,
                        color_continuous_scale="Viridis")
        
        fig.update_layout(
            title="Classroom Utilization Heatmap",
            xaxis_title="Classroom",
            yaxis_title="Time Slot",
            height=600
        )
        
        return fig
