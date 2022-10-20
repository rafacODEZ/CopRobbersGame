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

    def playGame(self):
        while self.UI.startGameQuestion() == True:
            self.gameIntro()
            self.createVertexSection()
            self.createEdgeSection()
            self.placePlayerSection()
            self.movePlayerSection()
            self.endGameSection()
            self.resetGame()
        self.UI.displayThanks()

####################################################################################################################
############################                Parts of The Game                              #########################

    def gameIntro(self):
        self.UI.printIntro()

        moves = self.UI.moveLimitQuestion()
        self.movesAllowed = moves

        self.UI.dividers()

    def createVertexSection(self):

        self.UI.questionExplained("vertex")
        vertex = self.UI.vertexQuestion()

        while vertex != "done":

            if vertex in self.vertex:
                self.UI.displayError("Vertex_Exist")

            else:
                self.createVertex(vertex)
                self.UI.vertexSuccessful()

            vertex = self.UI.vertexQuestion()

        self.UI.dividers()

    def createEdgeSection(self):

        self.UI.questionExplained("edges")
        self.UI.displayVertex(self.getVertex())

        edge = self.UI.edgesQuestion()

        while edge[0] != "done":
            vertex_1 = edge[0]
            vertex_2 = edge[1]

            if self.createEdge(vertex_1, vertex_2) == True:
                if vertex_1 not in self.vertex or vertex_2 not in self.vertex:
                    self.UI.displayError("Vertex")
                else:
                    self.UI.edgeSuccessful(True)

            elif self.createEdge(vertex_1, vertex_2) == False:
                if vertex_1 not in self.vertex or vertex_2 not in self.vertex:
                    self.UI.displayError("Vertex")

                elif vertex_1 == vertex_2:
                    self.UI.edgeSuccessful("same")

                else:
                    self.UI.edgeSuccessful(False)

            edge = self.UI.edgesQuestion()

        self.UI.dividers()

    def placePlayerSection(self):
        self.UI.questionExplained("place")

        for place in range(2):
            if place == 1:
                self.UI.dividers()

            self.UI.makeSpace()
            self.whoseTurn()
            self.display()

            placedPlayer = self.UI.placeQuestion(self.vertex)

            if place == 0:
                if placedPlayer[0] != "C":
                    self.UI.displayNotYourTurn(self.playersTurn)
                    placedPlayer = self.UI.placeQuestion(self.vertex)
                self.playersTurn = "Robber"

            elif place == 1:
                if placedPlayer[0] == "C":
                    self.UI.displayNotYourTurn(self.playersTurn)
                    placedPlayer = self.UI.placeQuestion(self.vertex)
                self.playersTurn = "Cop"

            self.placePlayer(placedPlayer[0], placedPlayer[1])

        self.UI.dividers()

    def movePlayerSection(self):
        self.UI.questionExplained("move")

        while self.copMoves < self.movesAllowed:

            if self.winCheck() == "C":
                break

            self.firstMove = False
            moveAccepted = "Deny"
            while moveAccepted != "Accept":

                if self.copMoves >= 1:
                    self.UI.dividers()

                self.UI.displayCopsMoves(self.movesAllowed, self.copMoves)
                self.UI.displayWhoseTurn(self.playersTurn)
                self.UI.displayPlayers(self.playersPosition)
                self.UI.displayEdges(self.edges)

                movePlayer = self.UI.moveQuestion(
                    self.vertex, self.firstMove, self.playersTurn)

                if movePlayer == "copQuit":
                    self.copQuit = True
                    break

                player = movePlayer[0]
                vertex = movePlayer[1]

                previousPosition = copy.deepcopy(self.playersPosition)

                if self.movePlayer(player, vertex) == True:
                    moveAccepted = self.UI.moveSuccessful(
                        previousPosition, True, self.playersTurn, self.playersPosition, player, vertex)
                else:
                    moveAccepted = self.UI.moveSuccessful(
                        None, False, None, None, None, None)

                if moveAccepted == "repeat":
                    self.playersPosition = previousPosition

            if self.copQuit == True:
                break

            if self.winCheck() == "C":
                break

            if self.playersTurn == "Cop":
                self.copMoves += 1

            if self.playersTurn == 'Robber':
                self.playersTurn = "Cop"
            else:
                self.playersTurn = "Robber"

        self.UI.dividers()

    def endGameSection(self):
        winner = self.winCheck()

        if self.copMoves == self.movesAllowed and winner == "X":
            winner = "R"

        if self.copQuit == True:
            winner = "R"

        self.UI.displayWinner(winner)
        self.display()
        self.UI.dividers()
        self.UI.dividers()

####################################################################################################################
############################            Get Information Methods & Who's Turn               #########################

    def getVertex(self):
        return self.vertex

    def getEdge(self):
        return self.edges

    def whoseTurn(self):

        if self.playersTurn == "Cop":
            self.UI.displayWhoseTurn("Cop")

        elif self.playersTurn == "Robber":
            self.UI.displayWhoseTurn("Robber")

    def getDisplay(self):
        copPosition = "Cop not placed"
        robbersPosition = "Robber not placed"

        for player, position in self.playersPosition.items():
            if player == "C":
                copPosition = position
            elif player == "R":
                robbersPosition = position

        vertex1 = " "
        for vertex in self.vertex:
            vertex1 += f"{vertex}, "

        edges = " "
        for edge in self.edges:
            edges += f"({edge[0]},{edge[1]}), "

        results = f"Cop: {copPosition}    Robber: {robbersPosition}"
        results += "\n" + f"{vertex1[:-2]}"
        results += "\n" + f"{edges[:-2]}"

        return results

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

    def createVertex(self, vertex):
        self.vertex.append(vertex)

    def createEdge(self, vertex1, vertex2):
        newVertex = False
        if vertex1 == vertex2:
            pass
        elif vertex1 not in self.vertex or vertex2 not in self.vertex:
            pass
        elif (vertex1, vertex2) in self.edges or (vertex2, vertex1) in self.edges:
            pass
        else:
            self.edges.append((vertex1, vertex2))
            newVertex = True

        return newVertex

    def placePlayer(self, player, vertex):
        if vertex in self.vertex:
            self.playersPosition[player] = vertex

    def movePlayer(self, movePlayer, moveVertex):
        for player, vertex in self.playersPosition.items():
            if movePlayer == player and moveVertex == vertex:
                return True

            elif movePlayer == player:
                vertexReg = (vertex, moveVertex)
                vertexFliped = (moveVertex, vertex)

                if vertexReg in self.edges or vertexFliped in self.edges:
                    self.playersPosition[player] = moveVertex
                    return True
        return False

    def winCheck(self):
        if self.playersPosition["C"] == self.playersPosition["R"]:
            return "C"
        elif self.copMoves > self.movesAllowed:
            return "R"
        else:
            return "X"

    def display(self):
        copPosition = "Cop not placed"
        robbersPosition = "Robber not placed"

        for player, position in self.playersPosition.items():
            if player == "C":
                copPosition = position
            elif player == "R":
                robbersPosition = position

        vertex1 = " "
        for vertex in self.vertex:
            vertex1 += f"{vertex}, "

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

    def printIntro(self):
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
        return welcomeMSG

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

    def moveLimitQuestion(self):
        while True:
            try:
                user = input("How many moves is the Cop allowed to make?")

                if (chr(33) <= user <= chr(47)) or (chr(58) <= user <= chr(126)):
                    raise Exception

                elif int(user) <= 0:
                    raise Exception
                else:
                    user = int(user)
                    break
            except:
                self.displayError("invalid_input")
        return user

    def vertexQuestion(self):
        while True:
            user = input("Create Vertex: ").strip().lower()

            if chr(97) <= user <= chr(122) and len(user) == 1:
                return user

            elif user == "done":
                return user

            else:
                self.displayError("invalid_input")

    def edgesQuestion(self):
        print()
        while True:
            edge = input("Create Edges: ").lower().strip().split(",")

            if edge[0] == "done":
                return edge

            elif len(edge) < 2:
                self.displayError("invalid_input")

            elif chr(97) <= edge[0] <= chr(122) and chr(97) <= edge[1] <= chr(122):
                return edge

            else:
                self.displayError("invalid_input")

    def placeQuestion(self, vertex):
        while True:
            try:
                placedPlayer = input("Place your player: ").strip().split(",")

                if placedPlayer[0] != "C" and placedPlayer[0] != "R":
                    self.Error("Player")
                    raise Exception

                elif placedPlayer[1] not in vertex:
                    self.Error("Vertex")
                    raise Exception

                elif len(placedPlayer) < 2 or len(placedPlayer) > 2:
                    self.Error("too_many_char")
                    raise Exception

                else:
                    return placedPlayer
            except:
                self.displayError("invalid_input")

    def moveQuestion(self, vertex, firstMove, playersTurn):
        while True:
            try:

                if playersTurn == "Cop":
                    print()
                    print("Cop may quit anytime by Typing 'Cop gives up'.")

                movePlayer = input("Move player: ").strip().split(",")

                if playersTurn == "Cop" and movePlayer[0].lower() == "cop gives up":
                    return "copQuit"

                if movePlayer[0] != "C" and firstMove == True:
                    self.copsTurn()

                elif movePlayer[0] != "C" and movePlayer[0] != "R":
                    raise Exception

                elif movePlayer[1] not in vertex:
                    raise Exception

                elif len(movePlayer) < 2 or len(movePlayer) > 2:
                    raise Exception

                else:
                    return movePlayer
            except:
                self.displayError("invalid_input")

####################################################################################################################
#############################            Answers To Users Inputs                          ##########################

    def vertexSuccessful(self):
        print("Vertex created")
        print()

    def edgeSuccessful(self, edge):
        if edge == True:
            print("Edge succesfully created.")
            print()

        elif edge == False:
            print("Edge already exist.\nEdge not created.")
            print()

        elif edge == "same":
            print("Cannot create a looped edged.")

    def moveSuccessful(self, perivousPosition, move, playersTurn, playersPosition, player, vertex):
        if move == True:
            if player == 'C':
                playerTemp = 'Cop'
            elif player == 'R':
                playerTemp = 'Robber'

            if playersTurn == playerTemp:

                if player in playersPosition.keys() and vertex == perivousPosition[player]:
                    print()
                    print("You decided to stay at your current vertex.")
                    print("You were not moved.")
                    print()
                    return "Accept"

                else:
                    print()
                    print("Move was successful.")
                    print()
                    return "Accept"

            else:
                repeat = self.displayNotYourTurn(playersTurn)
                return repeat

        elif move == False:
            print("Move not allowed.")
            print()

        return "Deny"

####################################################################################################################
#############################                 Displays to user                           ###########################

    def displayVertex(self, vertex):
        ver = " "
        for vert in vertex:
            ver += f"{vert}, "
        print()
        print(f"Vertices: {ver[:-2]}")

    def displayEdges(self, edges):
        edgeMSG = " "
        for edge in edges:
            edgeMSG += f"({edge[0]},{edge[1]}) "

        print(f"Edges: {edgeMSG}")

    def displayPlayers(self, playersPosition):
        copPosition = "Cop not placed"
        robbersPosition = "Robber not placed"

        for player, position in playersPosition.items():
            if player == "C":
                copPosition = position
            elif player == "R":
                robbersPosition = position

        print(f"Cops: {copPosition}    Robbers: {robbersPosition}")

    def displayCopsMoves(self, movesAllowed, movesTaken):
        remainingMoves = movesAllowed - movesTaken
        print()
        print((f"Cop's remaining moves: {remainingMoves}").center(50))

    def displayNotYourTurn(self, player):
        print("Not your turn!")
        print()
        return "repeat"

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

    def displayThanks(self):
        print("Thanks for playing.")

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
