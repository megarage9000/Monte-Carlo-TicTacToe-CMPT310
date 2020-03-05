
class Player:
    def __init__(self, playerToken):
        self.playerToken = playerToken
        
    def getPlayerToken(self):
        return self.playerToken
    
    

class Board: 
    
    board = [['_' for x in range(3)] for x in range(3)]
    
    def __init__(self):
        self.win = False
    
    def getBoard(self):
        return self.board
    
    
        
    
def main():
    print("Hello World")
    


    
    

main()

    
