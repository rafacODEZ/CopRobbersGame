import copy


class CopRobGame:
    def __init__(self, moves):
        self.movesAllowed = moves
        self.copMoves = 0
        self.copQuit = False
        self.firstMove = True
        self.vertex = []
        self.edges = []
        self.playersPosition = dict()
        self.playersTurn = "Cop"
        self.UI = UserInterface()

                        ###########             The  Game           ##############
    def playGame(self):
        while self.UI.startGameQuestion() == True:
            self.gameIntro()                  # start of game
            self.createVertexSecton()         # users creates vertices
            self.createEdgeSection()          # user creates edges
            self.placePlayerSection()         # users place their players
            self.movePlayerSection()          # users move their players
            self.endGameSection()             # game has ended
            self.resetGame()                  # reset internal data
        self.UI.displayThanks()               # End message



####################################################################################################################
############################                Parts of The Game                              #########################
        
    def gameIntro(self):
        # intro to program
        self.UI.printIntro()

        # user question: moves cop is allowed
        # then stores it to local variable
        moves = self.UI.moveLimitQuestion()
        self.movesAllowed = moves

        # divides the programs different section with stars
        self.UI.dividers()
        
    def createVertexSecton(self):
        # explains vertex section to user
        self.UI.questionExplained("vertex")
        vertex = self.UI.vertexQuestion()

        # keeps asking for vertex until user
        # decides they are "done"
        while vertex != "done":
            # only creates vertex if vertex does not already exist
            if vertex in self.vertex:
                self.UI.displayError("Vertex_Exist")
            # creates the vertex
            else:
                self.createVertex(vertex)
                self.UI.vertexSuccessful()

            vertex = self.UI.vertexQuestion()
        # divides the programs different section with stars
        self.UI.dividers()
        
    def createEdgeSection(self):
        # explains edge section to user
        self.UI.questionExplained("edges")
        self.UI.displayVertex(self.getVertex())

        # asks user to create edges
        edge = self.UI.edgesQuestion()

        # keeps asking user for allowed edges until
        # user decides they are "done"
        while edge[0] != "done":
            vertex_1 = edge[0]
            vertex_2 = edge[1]

            # checks if edge was successfully created
            if self.createEdge(vertex_1, vertex_2) == True:
                # checks if vertices of edges being
                # created exist
                if vertex_1 not in self.vertex or vertex_2 not in self.vertex:
                    self.UI.displayError("Vertex")
                else:
                    self.UI.edgeSuccessful(True)

            # False if edge not created
            elif self.createEdge(vertex_1, vertex_2) == False:
                # checks that the edge being created has valid vertices
                if vertex_1 not in self.vertex or vertex_2 not in self.vertex:
                    self.UI.displayError("Vertex")

                # handles user trying to create as looped edge
                elif vertex_1 == vertex_2:
                    self.UI.edgeSuccessful("same")

                else:
                    self.UI.edgeSuccessful(False)
            # question asked again if the user has entered something invalid
            edge = self.UI.edgesQuestion()

        # divides the section with stars
        self.UI.dividers()
        
    def placePlayerSection(self):
        # explains placing the player to the user
        self.UI.questionExplained("place")

        # allows both players cop and robber to place
        # themselves on the graph
        for place in range(2):
            if place == 1:
                self.UI.dividers()

            # prints a new line
            self.UI.makeSpace()
            
            # displays who's turn it is
            self.whoseTurn()

            # show the user the current vertex & edges created
            # and the players position
            self.display()

            placedPlayer = self.UI.placeQuestion(self.vertex)

            # first place goes to the cop, makes sure cop is making a move

            if place == 0:
                if placedPlayer[0] != "C":
                    self.UI.displayNotYourTurn(self.playersTurn)
                    placedPlayer = self.UI.placeQuestion(self.vertex)
                # changes turn
                self.playersTurn = "Robber"

            # second place foes to the robber, makes sure the robber is making a move
            elif place == 1:
                if placedPlayer[0] == "C":
                    self.UI.displayNotYourTurn(self.playersTurn)
                    placedPlayer = self.UI.placeQuestion(self.vertex)
                # changes turn
                self.playersTurn = "Cop"

            # places the player
            self.placePlayer(placedPlayer[0], placedPlayer[1])

        # divides the programs different section with stars
        self.UI.dividers()
        
    def movePlayerSection(self):
        # ask user where they would like to move their player
        # starting with the cop
        self.UI.questionExplained("move")

        # keeps asking for moves until cop exceeds allowed moves
        while self.copMoves < self.movesAllowed:
            # checks if the cop has won
            # ends game if so
            if self.winCheck() == "C":
                break

            # no longer the first move, sets its internal data to False
            self.firstMove = False
            moveAccepted = "Deny"
            while moveAccepted != "Accept":

                # adds a divider after the first move
                # to create separation
                if self.copMoves >= 1:
                    self.UI.dividers()

                # shows the user the Cop's current move count, who's turn
                # it is, edges and the players position on the graphs
                self.UI.displayCopsMoves(self.movesAllowed, self.copMoves)
                self.UI.displayWhoseTurn(self.playersTurn)
                self.UI.displayPlayers(self.playersPosition)
                self.UI.displayEdges(self.edges)

                # ask user where they want to move
                movePlayer = self.UI.moveQuestion(
                    self.vertex, self.firstMove, self.playersTurn)

                # checks if cop has given up
                # ends game if True
                if movePlayer == "copQuit":
                    self.copQuit = True
                    break

                # assigns player and vertex respectively dependent on user input
                player = movePlayer[0]
                vertex = movePlayer[1]

                # keeps perivous positions to nullfy a move
                # if made incorrectly
                previousPosition = copy.deepcopy(self.playersPosition)

                # alerts user if the move was successful
                if self.movePlayer(player, vertex) == True:
                    moveAccepted = self.UI.moveSuccessful(
                        previousPosition, True, self.playersTurn, self.playersPosition, player, vertex)
                else:
                    moveAccepted = self.UI.moveSuccessful(
                        None, False, None, None, None, None)

                # checks if player is trying to move when it's not his turn
                if moveAccepted == "repeat":
                    # nullify players move if players moves when their turn isn't up
                    self.playersPosition = previousPosition

            # ends game if cop quits
            if self.copQuit == True:
                break

            # checks if cop has caught the robber
            if self.winCheck() == "C":
                break

            # updates by 1 the amount of moves the cop has made
            if self.playersTurn == "Cop":
                self.copMoves += 1

            # switches players turns
            if self.playersTurn == 'Robber':
                self.playersTurn = "Cop"
            else:
                self.playersTurn = "Robber"
                
        # divides the programs different section with stars
        self.UI.dividers()
        
    def endGameSection(self):
        # checks who has won at the end of the game
        winner = self.winCheck()

        # if cop exceeds moves allowed the robber wins
        if self.copMoves == self.movesAllowed and winner == "X":
            winner = "R"
            
        # cop has quit at some point in the game
        # so the winner is the robber
        if self.copQuit == True:
            winner = "R"

        # displays who won
        self.UI.displayWinner(winner)

        # displays end game results
        self.display()

        # dividers
        self.UI.dividers()
        self.UI.dividers()
        
####################################################################################################################
############################            Get Information Methods & Who's Turn               #########################
        
    # returns the current vertices at any given time
    def getVertex(self):
        return self.vertex

    # return the current edges at any given time
    def getEdge(self):
        return self.edges

    # prints apportiate message depending on who's turn
    def whoseTurn(self):

        if self.playersTurn == "Cop":
            self.UI.displayWhoseTurn("Cop")

        elif self.playersTurn == "Robber":
            self.UI.displayWhoseTurn("Robber")
            
    def resetGame(self):
        self.copMoves = 0
        self.copQuit = False
        self.firstMove = True
        self.vertex = []
        self.edges = []
        self.playersPosition = dict()
        self.playersTurn = "Cop"
        self.UI = UserInterface()
        
####################################################################################################################
############################                    Required Methods                           #########################

    # creates vertex and adds them to the end
    # of the gobal vertex list
    def createVertex(self, vertex):
        self.vertex.append(vertex)

    # creates edges and adds it to the end
    # of gobal edges list
    def createEdge(self, vertex1, vertex2):
        # set to false by default
        newVertex = False
        # checks if the vertices given are valid vertex
        if vertex1 == vertex2:
            pass
        # checks if vertex1 and vertex2 is in vertex list
        elif vertex1 not in self.vertex or vertex2 not in self.vertex:
            pass
        # checks if edge already exist, if it does then it doesn't create the edge
        elif (vertex1, vertex2) and (vertex2, vertex1) in self.edges:
            pass
        else:
            # returns true if edge created then
            # adds the edge to the gobal edge list
            self.edges.append((vertex1, vertex2))
            newVertex = True

        return newVertex

    # places player sat their desired vertex
    def placePlayer(self, player, vertex):
        if vertex in self.vertex:
            self.playersPosition[player] = vertex

    # moves player to desired vertex if it's
    # andjacent to the vertex they are current on
    def movePlayer(self, movePlayer, moveVertex):
        # loops through the players position list
        for player, vertex in self.playersPosition.items():
            # if player moves to vertex they already on
            # return true
            if movePlayer == player and moveVertex == vertex:
                return True

            # makes sure looped player is the decised player
            elif movePlayer == player:
                # creates edges to check if they in edge list
                # both possible variations
                vertexReg = (vertex, moveVertex)
                vertexFliped = (moveVertex, vertex)

                # checks if players desired move is possible
                if vertexReg in self.edges or vertexFliped in self.edges:
                    self.playersPosition[player] = moveVertex
                    return True
        return False

    # checks if there is a winner
    def winCheck(self):
        # cop catches player so cop wins
        if self.playersPosition["C"] == self.playersPosition["R"]:
            return "C"
        # return "R" if the move has exceed they move count
        # resulting in the robbers win
        elif self.copMoves > self.movesAllowed:
            return "R"
        else:
            # return "X" if there isn't a winner
            return "X"

    # displays the cops and robbers position
    # all created vertices are and edges
    def display(self):
        copPosition = "Cop not placed"
        robbersPosition = "Robber not placed"

        # goes through the players positions and assign
        # the players positions
        for player, position in self.playersPosition.items():
            if player == "C":
                copPosition = position
            elif player == "R":
                robbersPosition = position

        # creates the string printed to the user
        # of the created vertexs
        vertex1 = " "
        for vertex in self.vertex:
            vertex1 += f"{vertex}, "

        # creates the string printed to the user
        # of the created edges
        edges = " "
        for edge in self.edges:
            edges += f"({edge[0]},{edge[1]}), "

        results = f"Cop: {copPosition}    Robber: {robbersPosition}"
        results += "\n" + f"Vertices: {vertex1[:-2]}"
        results += "\n" + f"Edges: {edges[:-2]}"

        print(results)
        print()


class UserInterface:

#############################               Intro & How-To Prints                         ############################

    # prints games intro, explaining the game
    def printIntro(self):
        print()
        welcomeMSG = (
            "                                                                  "
            + "\n                                                              "
            + "\n               - Welcome to Cop and Robber -                  "
            + "\n                                                              "
            + "\n    Cop and Robber is a 2-player game, one player is a Cop    "
            + "\n   the other the Robber. The game can be played on any graph, "
            + "\n   created by the player before the start of the game. First  "
            + "\n     the player must enter the number of moves the cop is     "
            + "\n    allowed to make. Then create vertices and edges. After    "
            + "\n   creating the vertices and edges (creating a graph) the     "
            + "\n   Cop and Robber are allowed to place themselves on any of   "
            + "\n   the created vertices. Once both players are on the graph   "
            + "\n    they will be allowed to move to an adjacent vertex. The   "
            + "\n    players will alternate moving vertex to vertex starting   "
            + "\n   with the Cop. Both players take turns until either the Cop "
            + "\n    occpies the same vertex as the Robber (Cop wins),the cop  "
            + "\n  gives up by typing 'cop gives up' on his turn (Robber wins) "
            + "\n          or the Cop runs out of moves (Robber wins).         "
            + "\n                                                              "
            + "\n                         Good luck!                           "
            + "\n               May the odds be in your favor.                 "
            + "\n                                                              "
            + "\n                                                              "
        )
        print(welcomeMSG)
        print()

    # prints explaintion for the different questions throughout the game
    def questionExplained(self, whichQuestion):

        if whichQuestion == "vertex":
            vertexMSG = (
                "                                                                "
                + "\n                                                            "
                + "\n   Create as many vertices as you like using the alphabet   "
                + "\n    when you're done type 'Done' and hit return to stop.    "
                + "\n                                                            "
                + "\n                     Example: a                             "
                + "\n                                                            "
                + "\n                                                            "
            )
            print(vertexMSG)
            print()

        if whichQuestion == "edges":

            edgesMSG = (
                "                                                                 "
                + "\n                                                             "
                + "\n        Create as many edges as you like as long as the      "
                + "\n       vertices exist by typing in the vertex followed by    "
                + "\n      a comma then the other vertex. When you're done type   "
                + "\n                 'Done' and hit return to stop.              "
                + "\n                                                             "
                + "\n                        Example: a,b                         "
                + "\n                                                             "
                + "\n                                                             "
            )
            print(edgesMSG)
            print()

        if whichQuestion == "place":

            placeMSG = (
                "                                                                 "
                + "\n                                                             "
                + "\n      You may place your player on any existing vertex by    "
                + "\n      typing in 'C' for Cop or 'R' for Robber followed by    "
                + "\n                   a comma and the vertex.                   "
                + "\n                                                             "
                + "\n                   Example: C,a                              "
                + "\n                                                             "
                + "\n                                                             "
            )
            print(placeMSG)
            print()

        if whichQuestion == "move":

            moveMSG = (
                "                                                                 "
                + "\n                                                             "
                + "\n     The Cop and Robber will alternate turns, starting with  "
                + "\n        the cop.You may move your player to any existing     "
                + "\n      vertex that is connected by an edge. Type in 'C' for   "
                + "\n        Cop or 'R' for Robber followed by a comma and the    "
                + "\n         vertex. The cop may give up anytime by typing       "
                + "\n                      'Cop Gives Up'                         "
                + "\n                                                             "
                + "\n                       Example: R,c                          "
                + "\n                                                             "
                + "\n                                                             "
            )
            print(moveMSG)
            print()

####################################################################################################################
#############################                 Dialog With User                          ############################

    # start game question
    def startGameQuestion(self):
        print()
        print()
        user = input(
            "Do you want to play Cop and Robber? (Yes or No):").lower()

        while True:
            try:
                if user == 'yes':
                    return True
                elif user == 'no':
                    return False
                else:
                    raise Exception
            except:
                self.displayError("invalid_input")

            user = input(
                "Do you want to play Cop and Robber? (Yes or No):").lower()


    # prompts user for desired move or their respective players
    def moveLimitQuestion(self):
        while True:
            try:
                user = input("How many moves is the Cop allowed to make?")

                # makes sure its a integer
                if (chr(33) <= user <= chr(47)) or (chr(58) <= user <= chr(126)):
                    raise Exception
                # raises exception if user input a digit less than 0
                elif int(user) <= 0:
                    raise Exception
                else:
                    user = int(user)
                    break
            except:
                self.displayError("invalid_input")
        return user

    # prompts user to create vertex also checks for when the user is done creating
    def vertexQuestion(self):
        while True:
            user = input("Create Vertex: ").strip().lower()

            # assures user inputs a alphabet for a vertex. uppercase made to lower case
            if chr(97) <= user <= chr(122) and len(user) == 1:
                return user

            elif user == "done":
                return user

            else:
                self.displayError("invalid_input")

    # prompts user to crate edges also checks for when the user is done creating
    def edgesQuestion(self):
        print()
        while True:
            edge = input("Create Edges: ").lower().strip().split(",")

            # allows user to get out of loop
            if edge[0] == "done":
                return edge
            # doesn't accept edges more than length 2
            elif len(edge) < 2:
                self.displayError("invalid_input")

            # asures edge is an alphabet
            elif chr(97) <= edge[0] <= chr(122) and chr(97) <= edge[1] <= chr(122):
                return edge

            else:
                self.displayError("invalid_input")

    # prompts use to place their players on the graph
    def placeQuestion(self, vertex):
        while True:
            try:
                placedPlayer = input("Place your player: ").strip().split(",")

                # makes sure Cop or Robber are being placed on graph
                if placedPlayer[0] != "C" and placedPlayer[0] != "R":
                    self.Error("Player")
                    raise Exception

                # makes sure vertex exist
                elif placedPlayer[1] not in vertex:
                    self.Error("Vertex")
                    raise Exception

                # makes sure length of entered placed player is no more than 2
                elif len(placedPlayer) < 2 or len(placedPlayer) > 2:
                    self.Error("too_many_char")
                    raise Exception

                else:
                    return placedPlayer
            except:
                self.displayError("invalid_input")

    # prompts user to move their respective player
    def moveQuestion(self, vertex, firstMove, playersTurn):
        while True:
            try:

                # message only for cop
                if playersTurn == "Cop":
                    print()
                    print("Cop may quit anytime by Typing 'Cop gives up'.")

                movePlayer = input("Move player: ").strip().split(",")

                # allows cop to quit
                if playersTurn == "Cop" and movePlayer[0].lower() == "cop gives up":
                    return "copQuit"

                # Makes sure the cop is the first to move
                if movePlayer[0] != "C" and firstMove == True:
                    self.copsTurn()

                # checks allowed players are being entered to move
                elif movePlayer[0] != "C" and movePlayer[0] != "R":
                    raise Exception

                # assures desired move vertex exist
                elif movePlayer[1] not in vertex:
                    raise Exception

                # assures move entry is of length 2
                elif len(movePlayer) < 2 or len(movePlayer) > 2:
                    raise Exception

                else:
                    return movePlayer
            except:
                self.displayError("invalid_input")
                
####################################################################################################################
#############################            Answers To Users Inputs                          ##########################

    # prints vertex created
    def vertexSuccessful(self):
        print("Vertex created")
        print()

    # alerts the user of a successful edge creation
    def edgeSuccessful(self, edge):
        if edge == True:
            print("Edge succesfully created.")
            print()

        elif edge == False:
            print("Edge already exist.\nEdge not created.")
            print()

        elif edge == "same":
            print("Cannot create a looped edged.")

    # alerts the user of a successful move
    def moveSuccessful(self, perivousPosition, move, playersTurn, playersPosition, player, vertex):
        if move == True:
            # changes 'C' to 'Cop & 'R' to 'Robber'
            if player == 'C':
                playerTemp = 'Cop'
            elif player == 'R':
                playerTemp = 'Robber'

            if playersTurn == playerTemp:

                # display message if your moves to current location
                if player in playersPosition.keys() and vertex == perivousPosition[player]:
                    print()
                    print("You decided to stay at your current vertex.")
                    print("You were not moved.")
                    print()
                    return "Accept"

                # tells user their move was completed
                else:
                    print()
                    print("Move was successful.")
                    print()
                    return "Accept"

            # deals with user moving when it isn't their turn
            else:
                repeat = self.displayNotYourTurn(playersTurn)
                return repeat

        elif move == False:
            print("Move not allowed.")
            print()

        return "Deny"
    
####################################################################################################################
#############################                 Displays to user                           ###########################

    # displays the created vertex
    def displayVertex(self, vertex):

        ver = " "
        for vert in vertex:
            ver += f"{vert}, "
        print()
        print(f"Vertices: {ver[:-2]}")

    # displays the created edges
    def displayEdges(self, edges):

        edgeMSG = " "
        for edge in edges:
            edgeMSG += f"({edge[0]},{edge[1]}) "

        print(f"Edges: {edgeMSG}")

    # displays the positions of the players
    def displayPlayers(self, playersPosition):
        copPosition = "Cop not placed"
        robbersPosition = "Robber not placed"

        for player, position in playersPosition.items():
            if player == "C":
                copPosition = position
            elif player == "R":
                robbersPosition = position

        print(f"Cops: {copPosition}    Robbers: {robbersPosition}")

    # displays how many moves the cop has left
    def displayCopsMoves(self, movesAllowed, movesTaken):
        remainingMoves = movesAllowed - movesTaken
        print()
        print((f"Cop's remaining moves: {remainingMoves}").center(50))

    # display error message if player moves without it being their turn
    def displayNotYourTurn(self, player):
        print("Not your turn!")
        print()
        return "repeat"

    # displays who's turn it is
    def displayWhoseTurn(self, player):
        turnMSG = "Player's Turn: "
        if player == "Cop":
            turnMSG += "Cop"
            print(turnMSG.center(50))
            print()
            print()

        elif player == "Robber":
            turnMSG += "Robber"
            print(turnMSG.center(50))
            print()
            print()
                
    # prints and assigns the winner of the game respectively
    def displayWinner(self, winner):
        msg = ""
        if winner == "C":
            winner = "Cop"
            msg += f"The "
        elif winner == "R":
            winner = "Robber"
            msg += f"The "
        else:
            winner = "No Body"

        msg += f"{winner} has won!"
        print()
        print(msg)
        print()
        
    # displays to the user thanks for playing        
    def displayThanks(self):
        print("Thanks for playing.")
        
    # does some error checking
    def displayError(self, whichError):
        if whichError == "Vertex":
            print("Vertices do not exist.")
            print("Please, use any of the above vertices.")

        elif whichError == "Vertex_Exist":
            print("Vertex already exist.")
            print("Create a different vertex.")
            print()

        elif whichError == "Player":
            print("Only 'C' or 'R' allowed.")
            print("Please use valid players.")

        elif whichError == "too_many_char":
            print("Too many characters")
            print("One Player: 'C' or 'R' , and one valid vertex.")

        elif whichError == "invalid_input":
            print()
            print("Entry Invalid.")
            print("Try entering valid inputs.")
            print()

####################################################################################################################       
#############################                        Other                                ##########################
        
    # creates a dividor so the different sections of the game
    def dividers(self):
        line = "*" * 70
        print()
        print(line)

    def makeSpace(self):
        print()
        
####################################################################################################################
#############################             Runs Game When File is Opened                   ##########################

def main():
    game = CopRobGame(0)
    game.playGame()


if __name__ == "__main__":
    main()
