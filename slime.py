from lexer import Lexer

def main():
    filename = 'hello.slime'
    sourceFile = open(filename, 'r')

    lexer = Lexer(sourceFile)
    lexer.tokenize()
    print(lexer.tokens)

if __name__ == "__main__":
    main()