import random
from deap import base, creator, tools, algorithms

class GeneticTimetableOptimizer:
    def __init__(self, initial_schedule, constraints_checker):
        self.initial_schedule = initial_schedule
        self.constraints = constraints_checker
        
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", dict, fitness=creator.FitnessMax)
        
        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self.create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.evaluate_schedule)

    def create_individual(self):
        """Create a new timetable individual"""
        return creator.Individual(self.initial_schedule.copy())

    def crossover(self, ind1, ind2):
        """Perform crossover between two timetables"""
        point1 = random.randint(0, len(ind1) - 1)
        point2 = random.randint(0, len(ind2) - 1)
        ind1[point1:], ind2[point2:] = ind2[point2:], ind1[point1:]
        return ind1, ind2

    def mutate(self, individual):
        """Mutate a timetable"""
        time_slot1 = random.choice(list(individual.keys()))
        time_slot2 = random.choice(list(individual.keys()))
        individual[time_slot1], individual[time_slot2] = individual[time_slot2], individual[time_slot1]
        return individual,

    def evaluate_schedule(self, schedule):
        """Evaluate the fitness of a schedule"""
        score = 0
        for day, time_slots in schedule.items():
            for time_slot, assignment in time_slots.items():
                if not self.constraints.check_teacher_availability(assignment['teacher'], day, time_slot, schedule):
                    score -= 10
                
                if not self.constraints.check_room_availability(assignment['classroom'], day, time_slot, schedule):
                    score -= 5
                
                if not self.constraints.check_lab_hours(assignment['class'], day, schedule):
                    score -= 5
        return score,

    def optimize(self, generations=50, population_size=50):
        """Run the genetic algorithm"""
        pop = self.toolbox.population(n=population_size)
        result = algorithms.eaSimple(pop, self.toolbox, cxpb=0.7, mutpb=0.2, ngen=generations)
        return tools.selBest(pop, k=1)[0]
