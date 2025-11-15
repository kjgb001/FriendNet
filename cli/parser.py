
class Parser:
    def parse(self, raw):
        tokens = raw.strip().split()

        if not tokens:
            return None, []

        command = tokens[0]
        args = tokens[1:]

        return command, args
