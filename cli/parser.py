
class Parser:
    ''' Parses raw cli input. Returns the command and arguments as a tuple. '''
    def parse(self, raw):
        tokens = raw.strip().split()

        if not tokens:
            return None, []

        command = tokens[0]
        args = tokens[1:]

        for i in range(len(args)):
            try:
                f_arg = float(args[i])
                args[i] = f_arg
            except ValueError:
                pass

        return command, args
