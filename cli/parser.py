
class Parser:
    ''' Parses raw cli input. Returns the command and arguments as a tuple. '''
    def parse(self, raw):
        tokens = raw.strip().split()

        if not tokens:
            return None, []

        command = tokens[0]
        args = tokens[1:]

        return command, args
