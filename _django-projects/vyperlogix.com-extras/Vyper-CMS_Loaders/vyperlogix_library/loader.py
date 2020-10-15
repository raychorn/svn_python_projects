from vyperlogix.enum.Enum import Enum

class Config(Enum):
    path = r'C:\_@4_\VyperLogixLib-1.0-py2.5.egg\html'

def main():
    print Config.path

if (__name__ == '__main__'):
    main()
    
