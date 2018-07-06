""" Interpreter for virtual logic schemas
designed with NAND logic elements.
"""
import sys
import getopt

from ruamel.yaml import YAML


class Executor:
    """ Execute logic scheme
    """

    def __init__(self):
        self.inputs = None
        self.inputs_values = None # Immutable

        self.outputs = None
        self.output_values = None

        self.gates = None
        self.gates_values = None

        self.clock = False

        self.count_to = 0

    def fill_inputs(self):
        """ Fills inputs data with values.
        """
        self.inputs_values = {}
        for i in self.inputs:
            self.inputs_values[i] = False

    def tick(self):
        """ Does the tick.
        """
        self.clock = True

    def tock(self):
        """ Does the tock
        """
        self.clock = False

    def element_function(self, a_op, b_op):
        """ Does NAND stroke function on two operands.
        """
        return not (a_op and b_op)

    def _init_inputs(self):
        self.gates_values = self.inputs_values

    def execute(self):
        """ Traverses thru the gates tree.
        """
        self._init_inputs()
        for _ in range(self.count_to):
            for value in self.gates:
                name = list(value.keys())[0]
                params = list(value.values())[0]

                result_path = params.get('r')
                result_path = result_path if result_path else name
                self.gates_values[result_path] = self.element_function(
                    self.gates_values[params['a']],
                    self.gates_values[params['b']],
                )


def do_job(filename):
    """ Do interpreter's job!

    Args:
        filename (str): file with logic scheme

    """
    with open(filename, 'r') as file:
        yaml = YAML()
        code = yaml.load(file.read())

        executor = Executor()
        executor.inputs = code['inputs']
        executor.outputs = code['outputs']
        executor.gates = code['gates']

        # executor.inputs['a1'] = True

        executor.count_to = 1 # execute loop of clock just 1 time
        executor.fill_inputs()

        executor.inputs_values['a1'] = True
        executor.inputs_values['b1'] = True

        executor.execute()

        print(executor.gates_values)


def main(argv):
    """ Main function.
    """
    try:
        opts, args = getopt.getopt(argv, 'hi:o', ['ifile=', 'ofile='])
    except getopt.GetoptError:
        print('run.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-i', '-ifile'):
            do_job(arg)


if __name__ == '__main__':
    main(sys.argv[1:])
