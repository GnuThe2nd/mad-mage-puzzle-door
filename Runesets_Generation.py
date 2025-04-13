from random import choice, seed, shuffle, randint
from math import ceil

class Runedials :
    '''
    This class is used to generate a random runeset for each level.
    '''
    def __init__(self, random_seed="Blackcloak"): #setting the seed to a default value
        self.runes = [
        "Anarath",
        "Angras",
        "Halaster",
        "Korombos",
        "Laebos",
        "Lammath",
        "Nchasme",
        "Savaros",
        "Ullathar",
        ]
        self.rseed = random_seed
        seed(self.rseed) #setting the seed for the random number generator
        
        self.level_order = self.__generate_level_order()

        runesets, solutions = self.__combine_runesets_and_solutions()

        self.runesets = runesets
        self.solutions = solutions
        

    def __generate_solution(self):

        '''
        This funciton generates a random solution for each level, based on a randomness seed. This makes sure that every generation is same, if the same seed is used.
        Every rune in a single solution is unique. Due to the setup logic, the second and third rune cannot be Halaster.
        '''
    
        solution_list = []
        available_runes = self.runes.copy()
        for i in range(3):
            rune = choice(available_runes)
            solution_list.append(rune)
            available_runes.remove(rune)
            if "Halaster" in available_runes:
                available_runes.remove("Halaster")

        return solution_list, available_runes
    
    def __generate_level_order(self): 
        random_level_order = []
        '''
        This generates a list with numbers 0-21, but leaves out 5, since the level it refers to
        is the Level 6: The Lost Level, which doesnt have a door like that.
        '''
        for i in range(1, 23):
            if i != 6:
                random_level_order.append(i)
        shuffle(random_level_order)

        return random_level_order
    
    def __shift_list_to_right(self, lst, index):
        index = index % len(lst)
        return lst[-index:] + lst[:-index]

    def __create_runeset(self, level):
        '''
        This function takes a soluton set and adds all other runes to create a random valid order.
        The anwser is list generated based on the following rules:
        Solutions 1. rune is the one that the arrow in the middle points towards
        Solutions 2. rune is always the rune 1 rune onward from the "Halaster" Rune (which means it cannot itself be Halaster Rune)
        Solutions 3. rune must be a rune, that is Level / 5 rounded up spots onwards from the second rune' (which also cannot be Halaster rune)
        '''
        
        solution_set, available_runes = self.__generate_solution()

        runeset = []
        for i in range(9):
            runeset.append(0)

        runeset[0] = solution_set[2] #we set the third rune down first
        
        step = ceil(level/5)
        runeset[-step] = solution_set[1]
        runeset[-step-1] = "Halaster"
        
        if solution_set[0] != "Halaster":
            available_runes.append(solution_set[0]) #we add the first rune back.

        zero_index = 0
        while len(available_runes) != 0: #loop infinitely, since we dont know how many runes we will need to add (due to halaster rune being in the solution or not)
            rune = choice(available_runes)
            if runeset[zero_index] == 0:
                available_runes.remove(rune)
                runeset[zero_index] = rune
            zero_index += 1

        return self.__shift_list_to_right(runeset, randint(0, 8)), solution_set
    
    def __combine_runesets_and_solutions(self):
        '''
        This function takes the generated unique solution and combines it with the level order to create a final solution. If a solution already excists, a new one is generated.
        '''
        combined_runesets = {}
        combined_solutions = {}
        for i in range(len(self.level_order)):
            runeset, solution_set = self.__create_runeset(self.level_order[i])
            while runeset in combined_runesets.values() or solution_set in combined_solutions.values():
                runeset, solution_set = self.__create_runeset(self.level_order[i])
            combined_runesets[self.level_order[i]] = runeset
            combined_solutions[self.level_order[i]] = solution_set
        return combined_runesets, combined_solutions
    
testObj = Runedials()

for rida in testObj.solutions:
    print(testObj.solutions[rida])

for rida in testObj.runesets:
    print(testObj.runesets[rida])
