from xml.dom import minidom as mini
from tkinter import filedialog


class FetchData:

    @classmethod
    def get_xml_location(cls):
        return filedialog.askopenfilename(title='select your pda xml', filetypes=(('xml files', '*.xml'), ('all files', '*.*')))

    doc = None
    states = None
    transitions = None

    @classmethod
    def fetch_states(cls):
        cls.doc = mini.parse(cls.get_xml_location())
        cls.states = cls.doc.getElementsByTagName('state')
        state_objects = []
        for state in cls.states:
            state_objects.append(State(state.attributes['name'].value))
        return state_objects

    @classmethod
    def fetch_transitions(cls):
        cls.transitions = cls.doc.getElementsByTagName('transition')
        transition_objects = []
        for transition in cls.transitions:
            source = transition.attributes['source'].value
            dest = transition.attributes['destination'].value
            read_input = transition.attributes['input'].value
            pop = transition.attributes['pop'].value
            push = transition.attributes['push'].value
            transition_objects.append(Transition(source, dest, read_input, pop, push))
        return transition_objects






class Transition:

    def __init__(self, source, destination, input, pop, push):
        self.source = source
        self.destination = destination
        self.input = input
        self.pop = pop
        self.push = push



class State:
    def __init__(self, name):
        self.name = name





class Computation:
    states = None
    transitions = None
    file = None


    @classmethod
    def pushing_move(cls, transition):
        for state in cls.states:
            for second_state in cls.states:
                pushing_grammer = "(" + transition.source + transition.pop + state.name + ") ->"
                if transition.input != 'la':
                    pushing_grammer += transition.input
                pushing_grammer += "(" + transition.destination + transition.push[0] + second_state.name + ")("
                pushing_grammer += second_state.name + transition.push[1] + state.name + ")"
                if second_state.name != cls.states[-1].name:
                    pushing_grammer += " | "
                cls.file.write(pushing_grammer)
            cls.file.write("\n")


    @classmethod
    def poping_move(cls, transition):
        cls.file.write("(" + transition.source + transition.pop + transition.destination + ")" + " ->" + transition.input+"\n")

    @classmethod
    def normalize(cls):
        for transition in cls.transitions:
            if len(transition.push) == len(transition.pop):
                temp = transition.pop
                substack_element = cls.transitions[cls.transitions.index(transition)-1].push
                substack_element = substack_element.replace(temp, '')
                new_state = State('q' + str(len(cls.states)))
                cls.states.append(new_state)
                source = transition.source
                transition.destination = new_state.name
                transition.pop = temp
                transition.push = 'la'
                cls.transitions.append(Transition(new_state.name, source, 'la', substack_element, temp + substack_element))




    @classmethod
    def compute(cls):
        cls.states = FetchData.fetch_states()
        cls.transitions = FetchData.fetch_transitions()
        cls.file = open('output.txt', 'w')
        cls.normalize()
        for transition in cls.transitions:
            if transition.push == 'la':
                cls.poping_move(transition)

        for transition in cls.transitions:
            if transition.push != 'la':
                cls.pushing_move(transition)
        cls.file.close()





def main():

    Computation.compute()


if __name__ == '__main__':
    main()
