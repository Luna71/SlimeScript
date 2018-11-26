class Lexer:
    def __init__(self, sourceFile):
        self.sourceFile = sourceFile
        self.tokens = []

        self.keywords = [
            'print',
            'stop',
        ]

        self.stringParticles = [
            '"',
            '\'',
        ]

        self.operators = {
            '+',
            '-',
            '*',
            '/',
        }

        self.other = [
            '{',
            '}',
            '(',
            ')',
            ',',
            '=',
        ]

    def getAndClearBuffer(self, buf):
        tmpBuffer = list(buf)
        buf.clear()
        return ''.join(tmpBuffer)

    def tokenizeBuffer(self, buf):
        if len(buf) == 0:
            return
        bufferString = self.getAndClearBuffer(buf)
        if bufferString.isdigit():
            self.tokens.append(['number',  bufferString])
        elif bufferString in self.keywords:
            self.tokens.append(['keyword', bufferString])
        else:
            self.tokens.append(['symbol',  bufferString])


    def tokenize(self):
        buffer = []

        state = {
            'string': {
                'parsing': False,
                'particle': '',
            }
        }

        for line in self.sourceFile:
            for letter in line:

                if letter in self.stringParticles:
                    if not state['string']['parsing']: # Have we started recording a string?
                        state['string']['parsing'] = True
                        state['string']['particle'] = letter
                        buffer = []
                    else: 
                        sameParticle = letter == state['string']['particle'] # Are we using the same string particle to end the line, that we used to start the line?
                        escapePresent = buffer[len(buffer) - 1] == "\\" # Do we escape the particle?
                        if sameParticle and not escapePresent:
                            state['string']['parsing'] = False
                            self.tokens.append(['string', self.getAndClearBuffer(buffer)]) # Append the string token
                        else:
                            if escapePresent:
                                buffer.pop() # Remove escape character
                            buffer.append(letter) # Record string particle as part of the string

                elif state['string']['parsing']: # Are we inside a string?
                    buffer.append(letter)
                    continue

                elif letter in self.operators:
                    self.tokenizeBuffer(buffer)
                    self.tokens.append(['operator', letter])

                elif letter in self.other:
                    self.tokenizeBuffer(buffer)
                    self.tokens.append(['other', letter])

                elif letter == " ": 
                    if len(buffer) == 0:
                        continue
                    self.tokenizeBuffer(buffer)

                elif letter == "\n":
                    self.tokenizeBuffer(buffer)
                    self.tokens.append(['newline', ''])

                else:
                    buffer.append(letter)