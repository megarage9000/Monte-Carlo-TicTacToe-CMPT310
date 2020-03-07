
import random, math, copy

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
    
    numPlayouts = 10
    winScore = 10
    def __init__(self, playerToken, playerName):
        super().__init__(playerToken, playerName)
        self.numPlayouts = 10
        self.winScore = 10
        
    def getMove(self, board):
        
        currentState = State(board)
        rootNode = Node(currentState)
        opposingPlayer = board.getOpposingPlayer(self)
        for i in range(self.numPlayouts):
            # --- Selection Phase
            promisingNode = self.selection(rootNode)
            # --- Expansion
            if(promisingNode.getState().getStatus() == board.inProgressToken):
                self.expand(promisingNode)
                promisingNode = promisingNode.selectRandomChild()
            
            # ---Simulation
            # - return result based on token   
            result = self.simulate(promisingNode, opposingPlayer)
            self.backpropogate(promisingNode, result)
            print(i)
            
        childToReturn = self.findBestChildNode(rootNode)
        move = childToReturn.getState().getMove()
        return move[0], move[1]
        
            
                        
    def selection(self, rootNode):
        node = rootNode
        while(len(node.getChildren()) != 0):
                node = self.findBestChildNode(node)
                
        return node
    
    def expand(self, node):
        successorStates = node.getState().generateSuccessorStates()
        for state in successorStates:
            childNode = Node(state)
            childNode.setParent(node)
            node.addChild(childNode)
    
    # Returns a token based on result
    def simulate(self, node, opposingPlayer):
        testNode = node
        stateToTest = testNode.getState().getStatus()
        if(stateToTest == opposingPlayer.getPlayerToken()):
            node.getParent().setWinScore(-self.winScore)
            node.getState().board.displayBoard()
            return stateToTest
        
        while(stateToTest != testNode.getState().board.inProgressToken):
            testNode.getState().randomPlayout()
            stateToTest = testNode.getState().getStatus()
            
        return stateToTest
        
            

    def backpropogate(self, node, resultToken):
        tempNode = node
        while(tempNode != node.noParent):
            tempNode.incrementVisits()
            if(tempNode.getState().getCurrentPlayer() == resultToken):
                tempNode.addToWinScore(self.winScore)
            tempNode = tempNode.getParent()
            
            
        
    
    
    # For calculating UCB values 
    def findBestChildNode(self, node):
        maxUCB = 0
        bestChild = node.getChildAt(0)
        parentVisits = node.getNumVisits()
        
        for child in node.getChildren():
            calculatedUCB = self.UCBvalue(child, parentVisits)
            if (calculatedUCB > maxUCB):
                bestChild = child
                maxUCB = calculatedUCB
        return bestChild
                
        
    def UCBvalue(self, childNode, parentVisits):
        numVisits = childNode.getNumVisits()
        numWins = childNode.getNumWins()
        
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
    
    noParent = "No Parent"
    
    def __init__(self, state):
        self.children = []
        self.state = state
        self.winScore = 0
        self.numVisits = 0
        self.parentNode = self.noParent
        
    def addChild(self, childNode):
        self.children.append(childNode)
        
    def setParent(self, parentNode):
        self.parentNode = parentNode
        
    def getParent(self):
        return self.parentNode
    
    def getState(self):
        return self.state
    
    def getNumVisits(self):
        return self.numVisits
    
    def getNumWins(self):
        return self.winScore
    
    def addToWinScore(self, score):
        if(self.winScore >= 0):
            self.winScore += score
        
    def setWinScore(self, score):
        self.winScore = score
        
    def incrementVisits(self):
        self.numVisits += 1
    
    def selectRandomChild(self):
        child = random.choice(self.children)
        return child
    
    def getChildren(self):
        return self.children
    
    def getChildAt(self, index):
        return self.children[index]
    
# Stores data of a state        
# - Equal for both Opponent and Player
class State():
    
    def __init__(self, board, move=(-1,-1)):
        self.board = board
        self.currentPlayer = board.getCurrentPlayer()
        self.oppositePlayer = board.getOpposingPlayer(self.currentPlayer)
        self.isPlayerWon = board.isConnectedinRow(self.currentPlayer.getPlayerToken())
        self.isOpponentWon = board.isConnectedinRow(self.oppositePlayer.getPlayerToken())
        self.isDraw = self.board.isDraw()
        self.move = move
      
     # generate children   
    def generateSuccessorStates(self):
        successorStates = []
        possibleMoves = self.board.getEmptyPositions()
        for move in possibleMoves:
            # makes a new board per state
            newBoard = self.board.board.copy()
            possibleBoardState = Board(self.currentPlayer, self.oppositePlayer, newBoard)
            possibleBoardState.setBoardPosition(self.currentPlayer.getPlayerToken(), move[0], move[1])
            possibleBoardState.switchCurrentPlayer()
            possibleSuccessorState = State(possibleBoardState, move)
            successorStates.append(possibleSuccessorState)
            possibleBoardState.displayBoard()
        return successorStates

    # play the currrent player
    def randomPlayout(self):
        possibleMoves = self.board.getEmptyPositions()
        move = random.choice(possibleMoves)
        self.board.setBoardPosition(self.currentPlayer.getPlayerToken(), move[0], move[1])
        self.board.switchCurrentPlayer()            
        
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    def getOpposingPlayer(self):
        return self.getOpposingPlayer
    
    def getStatus(self):
        if(self.isPlayerWon):
            return self.currentPlayer.getPlayerToken()
        elif(self.isOpponentWon):
            return self.oppositePlayer.getPlayerToken()
        elif(self.isDraw):
            return self.board.drawToken
        else:
            return self.board.inProgressToken
    
    def getMove(self):
        return self.move
    
    # Checks if the given player passed in parameters has lost
    # - Does this by determining if the current player has won
    # - when the passed in player is the opposing player
    def ifGivenPlayerLost(self, player):
        return player == self.oppositePlayer and self.isPlayerWon
    
    def ifGivenPlayerWon(self, player):
        return player == self.currentPlayer and self.isPlayerWon

    def inProgress(self):
        return self.isPlayerWon or self.isDraw
        

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
        board.switchCurrentPlayer()
        return self.moveRow, self.moveColumn
    
    
# TODO, refactor board so it:
# - has information on both players
# - determines which one has won
# - can return the token/symbol of other player

class Board: 
    
    def __init__(self, player1, player2, board=[['_' for x in range(3)] for x in range(3)]):
        self.emptyTile = '_'
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = player1
        self.drawToken = "Draw"
        self.inProgressToken = "In Progress"
    
    # --- Getters and Setters
    
    def setBoardPosition(self, token, row, column):  
        self.board[row][column] = token
    
    def getBoardPosition(self, row, column):
        return self.board[row][column]
    
    def getOpposingPlayer(self, player):
        if(player == self.player1):
            return self.player2
        else:
            return self.player1
    
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    def isTileEmpty(self, row, column):
        return self.board[row][column] == self.emptyTile
    
    def switchCurrentPlayer(self):
        if(self.currentPlayer == self.player1):
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
    

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
            
    # Checks states of board        
    def isPlayerWon(self, player):
        return self.isConnectedinRow(player.getToken())
    
    def isDraw(self):
        return len(self.getEmptyPositions()) == 0
    
    def isInProgress(self):
        return not self.isDraw()
    
    def getBoard(self):
        return self.board.copy()
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
          
class A():
    
    def __init__(self):
        self.x = 0
        
    def test(self, otherObject):
        if otherObject == self:
            print("YES")
        else:
            print("afafa")
        
def main():
    player1 = HumanPlayer("O", "Player 1")
    player2 = AIPlayer("X", "Player 2")
    board = Board(player1, player2)
    game = TicTacToe(player1, player2, board)
    game.playGame()

    
main()

    
