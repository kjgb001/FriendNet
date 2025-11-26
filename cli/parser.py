import shlex

class Parser:
    ''' Parses raw CLI input. Returns the command and arguments as a tuple. '''
    
    def parse(self, raw):
        try:
            tokens = shlex.split(raw.strip())
        except ValueError:
            # mismatched quotes or similar syntax errors
            return None, []

        if not tokens:
            return None, []

        command = tokens[0]
        args = tokens[1:]

        # Attempt numeric conversion
        for i in range(len(args)):
            try:
                args[i] = float(args[i])
            except ValueError:
                pass

        return command, args
