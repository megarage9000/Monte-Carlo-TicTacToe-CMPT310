
import random, math

class Player:
    def __init__(self, playerToken, playerName):
        self.playerToken = playerToken
        self.moveRow = self.moveColumn = 0
        self.playerName = playerName
        self.hasWon = False
        
    def getPlayerToken(self):
        return self.playerToken
    
    def getMove(self, board):
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
        
# --- Monte Carlo Tree Search AI Implementation --- BEGIN

# Sources:
# - https://medium.com/swlh/tic-tac-toe-at-the-monte-carlo-a5e0394c7bc2
# - https://www.baeldung.com/java-monte-carlo-tree-search

class AIPlayer(Player):
    
    def __init__(self, playerToken, playerName):
        super.__init__()
        self.numPlayouts = 10
        
    def getMove(self, board):
        
        currentState = State(board)
        rootNode = Node(currentState)
        for i in range(self.numPlayouts):
            promisingNode = self.selection(rootNode)
            
    def selection(self, rootNode):
        node = rootNode
        while(len(node.getChildren) != 0):
                node = self.findBestChildNode(node)
                
        return node
    
    
    # For calculating UCB values 
    def findBestChildNode(self, node):
        maxUCB = 0
        bestChild = node.getChildAt(0)
        parentVisits = node.getState().getNumVisits()
        
        for child in node.getChildren():
            calculatedUCB = self.UCBvalue(child, parentVisits)
            if (calculatedUCB > maxUCB):
                bestChild = child
                maxUCB = calculatedUCB
        return bestChild
                
        
    def UCBvalue(self, childNode, parentVisits):
        childState = childNode.getState()
        numVisits = childState.getNumVisits()
        numWins = childState.getNumWins()
        
        # If child has not been visited, give preference to that child (since it can't be calculated with UCB)
        if numVisits == 0:
            return math.inf
        
        # calculate based on UCB formula
        else:
            return float(numWins/numVisits) + math.sqrt(2) * math.log(float(parentVisits/numVisits))
                
    

# Node Class to store averageValue per node and it's number of nodes
class Node():
    
    # Node stores the following:
    # - Its parent
    # - Its children
    # - A state to describe the game
    
    parentNode = "No Parent"
    
    def __init__(self, state):
        self.children = []
        self.state = state
        
    def addChild(self, childNode):
        self.children.append(childNode)
        
    def setParent(self, parentNode):
        self.parentNode = parentNode
        
    def getParent(self):
        return self.parentNode
    
    def getState(self):
        return self.state
    
    def selectRandomChild(self):
        index = random.randint(0, len(self.children))
        child = self.children[index]
        return child
    
    def getChildren(self):
        return self.children
    
    def getChildAt(self, index):
        return self.children[index]
    
# Stores data of a state        
class State():
    
    def __init__(self, board, currentPlayer, oppositePlayer):
        self.winScore = 0
        self.numVisits = 0
        self.currentPlayer = currentPlayer
        self.oppositePlayer = oppositePlayer
        self.board = board
    
    # TODO - determine whether winScore and numVisits belong in Node class
        
    def getNumVisits(self):
        return self.numVisits
    
    def getNumWins(self):
        return self.winScore
    
    def incrementWins(self):
        self.winScore += 1
        
    def incnrementVisits(self):
        self.numVisits += 1


    # TODO - implement generate children states
    # These states become other player's turn

            
    

# --- Monte Carlo Tree Search AI Implementation --- END

class HumanPlayer(Player):
    def __init__(self, playerToken, playerName):
        super().__init__(playerToken, playerName)
        
    def getMove(self, board):
        isValidMove = False
        while(not isValidMove):
            try:
                moveList = board.getEmptyPositions()
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
    
    
# TODO, refactor board so it:
# - has information on both players
# - determines which one has won
# - can return the token/symbol of other player

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
            
    def getBoard(self):
        return self.board

 
# TODO - refactor TicTacToe to simply handle board game functions
    
class TicTacToe:
    
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.win = False
        self.draw = False
    
    def playGame(self):
        while(not self.win and not self.draw):
            self.playTurn(self.player1)
            self.playTurn(self.player2)
            
    def playTurn(self, player):
        if(self.win == False and self.draw == False):
            
           
           # Checks if a player can make a move or not 
            if(len(self.board.getEmptyPositions()) == 0):
                self.draw = True
                print("Draw! no one wins")
                self.board.displayBoard()
            else:
                 # Display board and process move
                self.board.displayBoard()
                print(player.getPlayerName() + "'s Turn")
                moveRow, moveColumn = player.getMove(self.board)
                self.board.setBoardPosition(player.getPlayerToken(), moveRow, moveColumn)
                
                # Checks if player has won
                if(self.board.isConnectedinRow(player.getPlayerToken())):
                    self.win = True
                    player.playerWon()
                    winMessage = player.getPlayerName() + " Has won!"
                    print(winMessage)
                    self.board.displayBoard()      
                
def main():
    board = Board()
    player1 = HumanPlayer("O", "Player 1")
    player2 = HumanPlayer("X", "Player 2")
    game = TicTacToe(player1, player2, board)
    game.playGame()
    
    
main()

    
