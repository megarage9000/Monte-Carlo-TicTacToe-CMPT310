
class Player:
    def __init__(self, playerToken, playerName):
        self.playerToken = playerToken
        self.moveRow = self.moveColumn = 0
        self.playerName = playerName
        self.hasWon = False
        
    def getPlayerToken(self):
        return self.playerToken
    
    def getMove(self, moveList):
        raise NotImplementedError("No move method yet")
    
    def getPlayerName(self):
        return self.playerName
    
    def playerWon(self):
        self.hasWon = True
        
    def toString(self):
        print(self.playerName)
        print(self.playerToken)
        print(self.hasWon)
        print(self.moveRow)
        print(self.moveColumn)
        
# --- Monte Carlo Tree Search AI Implementation ---

class AIPlayer(Player):
    def __init__(self, playerToken, playerName):
        super.__init__()
        


# Node Class to store averageValue per node and it's number of nodes
class Node():
    def __init(self, averageValue, numVisit):
        self.averageValue = averageValue
        self.numVisit = numVisit
        self.children = []
        
    def addChild(self, childNode):
        self.children.append(childNode)

# --- Monte Carlo Tree Search AI Implementation ---class HumanPlayer(Player):
class HumanPlayer(Player):
    def __init__(self, playerToken, playerName):
        super().__init__(playerToken, playerName)
        
    def getMove(self, moveList):
        isValidMove = False
        while(not isValidMove):
            try:
                print("Enter row and column position of your move:")
                self.moveRow = int(input("ROW > "))
                self.moveColumn = int(input("COLUMN > "))
                
                # Checks if given move is one of the available moves
                move = (self.moveRow, self.moveColumn)
                print(move)
                for i in range(len(moveList)):
                    if move == moveList[i]:
                        isValidMove = True
                    
                if(isValidMove == False):
                    print("Not a valid move!")

            except:
                print("Enter in an integer please!")
    
        return self.moveRow, self.moveColumn
    
    


class Board: 
    
    def __init__(self):
        self.emptyTile = '_'
        self.board = [[self.emptyTile for x in range(3)] for x in range(3)]
            
    def setBoardPosition(self, token, row, column):  
        self.board[row][column] = token
    
    def getBoardPosition(self, row, column):
        return self.board[row][column]
    
    def isTileEmpty(self, row, column):
        return self.board[row][column] == self.emptyTile
    
    # Getting connected rows for given token
    def isConnectedinRow(self, token):        
        for i in range(3):
            # Horizontal rows
            if(self.board[i][0] == token):
                if(self.board[i][1] == self.board[i][2] == token):
                    return True
            
            # Vertical rows
            if(self.board[0][i] == token):
                if(self.board[1][i] == self.board[2][i] == token):
                    return True
        
        # Checking Angled rows        
        if(self.board[0][0] == self.board[1][1] == self.board[2][2] == token):
            return True
        
        elif(self.board[0][2] == self.board[1][1] == self.board[2][0] == token):
            return True
        
        return False
    
    # Get all Empty Positions
    def getEmptyPositions(self):
        emptyPositions = []
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                if(self.isTileEmpty(i, k)):
                    # Store move as tuple
                    move = (i, k)
                    emptyPositions.append(move)
        return emptyPositions
    
    def displayBoard(self):
        for i in range(len(self.board)):
            row = ""
            for k in range(len(self.board[i])):
                row += self.board[i][k] + " "
            print(row)
    
class TicTacToe:
    
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.win = False
        self.draw = False
    
    def playGame(self):
        while(not self.win and not self.draw):
            self.playTurn(self.player1)
            self.playTurn(self.player2)
            
    def playTurn(self, player):
        if(self.win == False and self.draw == False):
            
           
           # Checks if a player can make a move or not 
            possibleMoves = self.board.getEmptyPositions()
            if(len(possibleMoves) == 0):
                self.draw = True
                print("Draw! no one wins")
                self.board.displayBoard()
            else:
                 # Display board and process move
                self.board.displayBoard()
                print(player.getPlayerName() + "'s Turn")
                moveRow, moveColumn = player.getMove(possibleMoves)
                self.board.setBoardPosition(player.getPlayerToken(), moveRow, moveColumn)
                
                # Checks if player has won
                if(self.board.isConnectedinRow(player.getPlayerToken())):
                    self.win = True
                    player.playerWon()
                    winMessage = player.getPlayerName() + " Has won!"
                    print(winMessage)
                    self.board.displayBoard()
                    player.toString()        
                
def main():
    player1 = HumanPlayer("O", "Player 1")
    player2 = HumanPlayer("X", "Player 2")
    game = TicTacToe(player1, player2)
    # player1.toString()
    # player2.toString()
    game.playGame()
    
    
main()

    
