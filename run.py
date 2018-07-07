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

        self.gates = dict()
        self.gates_values = dict()

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
        self.gates_values.update(self.gates)
        self.gates_values.update(self.inputs_values)
        self.output_values = self.outputs

    def execute(self):
        """ Traverses thru the gates tree.
        """
        self._init_inputs()
        for _ in range(self.count_to):
            for name, params in self.gates.items():
                result_path = params.get('r')
                result_path = result_path if result_path else name
                value = self.element_function(
                    self.gates_values[params['a']],
                    self.gates_values[params['b']],
                )
                self.gates_values[result_path] = value
                if result_path in self.output_values:
                    self.output_values[result_path] = value


def do_job(filename_in, filename_out, use_defaults, clocks):
    """ Do interpreter's job!

    Args:
        filename (str): file with logic scheme

    """
    with open(filename_in, 'r') as file:
        yaml = YAML()
        code = yaml.load(file.read())

        executor = Executor()
        executor.inputs = code['inputs']
        executor.outputs = code['outputs']
        executor.gates = code['gates']
        executor.count_to = code.get('clocks') or 1

        executor.count_to = 1 # execute loop of clock just 1 time
        executor.fill_inputs()

        if use_defaults:
            executor.inputs_values = dict(code.get('default_inputs'))

        executor.execute()

        yaml_out = YAML()
        if filename_out:
            with open(filename_out, 'w') as output:                
                yaml_out.dump(executor.gates_values, output)
        else:
            yaml_out.dump(executor.gates_values, sys.stdout)

        print('--- Outputs ---')
        yaml_out.dump(executor.output_values, sys.stdout)


def main(argv):
    """ Main function.
    """
    try:
        opts, _ = getopt.getopt(argv, 'hi:o:d:c', ['ifile=', 'ofile=', 'defaults', 'clocks='])
    except getopt.GetoptError:
        print('run.py -i <inputfile>')
        sys.exit(2)

    filename_in = None
    filename_out = None
    use_defaults = False
    clocks = 1

    for opt, arg in opts:
        if opt in ('-i', '--ifile'):
            filename_in = arg
        elif opt in ('-o', '--ofile'):
            filename_out = arg
        elif opt in ('-d', '--defaults'):
            use_defaults = True
        elif opt in ('-c', '--clocks'):
            clocks = arg

    do_job(filename_in, filename_out, use_defaults, clocks)


if __name__ == '__main__':
    main(sys.argv[1:])
