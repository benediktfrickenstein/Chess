
from pieces import Rook,Queen,Pawn,Bishop,King,Knight
class setUp:
    def __init__(self):
        self.in_check=False
        
        
        
        
        self.white_captives=[]
        self.black_captives=[]

        white_rook_1 = Rook('r',0,0,'w')
        white_rook_2 = Rook('r',7,0,'w')
        white_knight_1 = Knight('h',1,0,'w')#name is h and stands for horse, k is already taken for king
        white_knight_2 = Knight('h',6,0,'w')
        white_bishop_1 = Bishop('b',5,2,'w')
        white_bishop_2 = Bishop('b',5,0,'w')
        white_queen = Queen('q',3,0,'w')
        white_king = King('k',4,0,'w')

        

        self.team='w'
        self.enemy='b'
        
        white_pawns = []
        for i in range(8):
            white_pawns.append(Pawn('p',i,1,'w'))
        
        black_rook_1 = Rook('r',0,0,'b')
        black_rook_2 = Rook('r',0,1,'b')
        black_knight_1 = Knight('h',1,7,'b')#name is h and stands for horse, k is already taken for king
        black_knight_2 = Knight('h',6,7,'b')
        black_bishop_1 = Bishop('b',2,7,'b')
        black_bishop_2 = Bishop('b',5,7,'b')
        black_queen = Queen('q',3,7,'b')
        black_king= King('k',4,4,'b')
        
        self.pieces=[white_king,white_bishop_1]
        self.pieces_enemy=[black_king,black_rook_1,black_rook_2]

        black_pawns = []
        for i in range(8):
            black_pawns.append(Pawn('p',i,6,'b'))
    
        
        
        self.board = [[0, 0, 0, white_king, 0, 0, 0, 0],
                  [black_rook_2, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, white_bishop_1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [black_king, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, black_rook_1, 0, 0, 0],
                  [0, 0,0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0,0, 0, 0, 0]
                  ]
    
    def change_team(self):
        temp1=self.team
        temp2=self.pieces
        self.team=self.enemy
        self.pieces=self.pieces_enemy
        self.enemy=temp1
        self.pieces_enemy=temp2

    def update_board(self):#strupid function that will be removed later
        for column,series  in enumerate(self.board):
            for row,square in enumerate(series):
                if square !=0 and square.get_coordinates()!=(row,column):#get_coordinates(
                    self.board[column][row]=0
                    self.board[square.get_col()][square.get_row()]=square

    def display_board(self):
        Brett=[[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0,0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0,0, 0, 0, 0]
                  ]
        white={'p':'♙','q':'♕','r':'♖','h':'♘','b':'♗','k':'♔'}#'♟','♜','♞','♝','♛','♚'
        black={'p':'♟','q':'♛','r':'♜','h':'♞','b':'♝','k':'♚'}
        for column,series  in enumerate(self.board):
            for row,square in enumerate(series):
                if square==0:
                    continue
                elif square.get_team()=='w':
                    Brett[column][row]=white[square.get_name()]
                else:
                    Brett[column][row]=black[square.get_name()]
                
        for i,col in enumerate(Brett):
            
            for row in col:
                
                print(row,end="|")
            print(f"|{i}")
            
        print("0|1|2|3|4|5|6|7")

        


    


                

        #returns all attacks of the team
    def get_all_attacks(self,team):
        attacks=[]
        pieces=self.pieces if team=='w' else self.pieces_enemy

        for piece in pieces:
                attacks.extend(piece.attacks(self))

        return sorted(set(attacks))
    def get_all_moves(self,team):
        moves=[]
        pieces=self.pieces if team=='w' else self.pieces_enemy

        for piece in pieces[1:]:
            moves.extend(piece.get_moves(self))
        return moves
    '''shows if it is possible to prevent a check by blocking or capturing the attacking piece'''
    def prevent_check(self):
        squares=[]
        for piece in self.pieces_enemy:
            squares.extend(piece.check_prevention())
        return squares

    
    def checkmate(self):#tells you if the oponents team is in checkmate 
        attacks=self.get_all_attacks(self.enemy) #moves from enemy
        moves=self.get_all_moves(self.team)
        king=self.pieces[0]
        if king.get_coordinates() in attacks:#checks if the king is being attacked
            self.in_check=True 
            '''if the king can't move and no allied piece can prevent the check it is checkmate!'''
            if not king.get_moves(self) and not bool(set(moves)&set(self.prevent_check())):
                return True
        return False
            




     
    def friendly_fire_preventer(self, attacks: tuple,team):
        
        for item in (attacks[:]):
            square=self.board[item[1]][item[0]]
            if square!=0 and square.get_team()==team:
                attacks.remove(item)
        return attacks

        # returns all horizonatal squares with coordinates, the piece can move to
    def horizontal_moves(self,column,row):
        """the list range will be returned at the end and will contain
        in wich range the piece is allowed to move"""
        
        king=False
        piece=self.board[column][row]
        line=(self.board[column])
        range_interval_piece=[0,0]
        attacks=[]
        squares=[]#squares that need to be occupied in order to prevent a checkmate
        position=None
        range_interval_piece = self.move_helper(row,line)
        
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            square=self.board[column][i]
            if (i,column)!=(row,column):
                attacks.append((i,column))
            if square!=0 and square.get_name()=='k' and square.get_team()!=piece.get_team():
                king = True
                position=i
        if king == True:
            if position>row:
                temp=position
                position=row
                row=temp
            else:
                position+=1
                row+=1
                
            for i in range(position, row):
                squares.append((i,column))
    
        return [attacks,squares]
    
    


    #returns alll horizontal squares the piece can move to
    def vertical_moves(self,column,row):
        line=[]
        for i in range(8):
            line.append(self.board[i][row])
        
        range_interval_piece=[0,0]
        attacks=[]
        squares=[]#squares that need to be occupied in order to prevent a checkmate
        piece=self.board[column][row]
        position=None
        king=False

        range_interval_piece = self.move_helper(row,line)       
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            square=self.board[i][row]
            if (i,column)!=(row,column):
                attacks.append((row,i))
            if square!=0 and square.get_name()=='k' and square.get_team()!=piece.get_team():
                king = True
                position=i
            
        if king == True:
            if position>column:
                temp=position
                position=column
                column=temp
            else:
                position+=1
                column+=1
            
            for i in range(position,column):
                squares.append((row,i))
            
        #if king ==True

        return [attacks,squares]
    #returns diagonal moves
    def diagonal1(self,column,row):
        #diagonal from left top to right bottom
        king=False
        start_row=0
        start_column=0
        range_interval_piece=[0,0]
        attacks=[]
        squares=[]#squares that need to be occupied in order to prevent a checkmate
        piece=self.board[column][row]
        


        if row>column:
            start_row=row-column
        elif row<column:
            start_column=column-row
        position=row-start_row
        a=start_row# just to not change start_row and start column with the wihile lookp
        b=start_column
        #start position helps to get the full diagonal
        line=[]
        while a<=7 and b<=7:
            line.append(self.board[b][a])
            b+=1
            a+=1
        range_interval_piece = self.move_helper(position,line)
        
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):
            square=self.board[start_row+i][start_column+i]
            if (start_row+i,start_column+i)!=(row,column):
                attacks.append((start_row+i,start_column+i))
            if square!=0 and square.get_name()=='k' and square.get_team()!=piece.get_team():
                king = True
                position1=i+start_row
                position2=i+start_column
        if king == True:
            if position1>row:
                temp=position1
                position1=row
                position2=column
                row=temp
            else:
                position1+=1
                position2+=1
                row+=1
            
            for i in range(position1,row):#unfinished     
                squares.append((i,position2))
                position2+=1
                
        return [attacks,squares]


    def diagonal2(self,column,row):
        #diagonal starts at the left bottom to right top
        king=False
        start_row=0
        start_column=7
        range_interval_piece=[0,0]
        attacks=[]
        squares=[]#squares that need to be occupied in order to prevent a checkmate
        piece=self.board[column][row]
        
        if row+column<7:
            start_column=row+column
            
        elif row+column>7:
            start_row=row-(7-column)
        position=row-start_row
        a=start_row# just to not change start_row and start column with the wihile lookp
        b=start_column
        #start position helps to get the full diagonal
        line=[]
        while a<=7 and b>=0:
            line.append(self.board[b][a])
            b-=1
            a+=1
        range_interval_piece = self.move_helper(position,line)
        
        for i in range(range_interval_piece[0],range_interval_piece[1]+1):

            if (start_row+i,start_column-i)!=(row,column):
                attacks.append((start_row+i,start_column-i))
                square=self.board[start_row+i][start_column-i]
            if square!=0 and square.get_name()=='k' and square.get_team()!=piece.get_team():
                king = True
                position=i
                position1=i+start_row
                position2=start_column-i
        if king == True:
            if position1>row:
                temp=position1
                position1=row
                position2=column
                row=temp
            else:
                position1+=1
                position2-=1
                row+=1
            
            for i in range(position1,row):#unfinished
                
                squares.append((i,position2))
                position2-=1
                
        return [attacks,squares]
            
    
    def horse_moves(self,column,row):
        #all hores moves(horizontal,vertical)
        moves=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]
        attacks=[]
        for item in moves:
            x=item[0]+row 
            y=item[1]+column 
            if x in range(0,8) and y in range(0,8):
                attacks.append((x,y))
        return attacks
    '''squares that are being attacked by the pawn, but may not be movable'''
    def pawn_attacks(self,column,row,team):
        attacks=[]
        
        if team=='w':
            if column+1<8 and row+1<8:
                attacks.append((row+1,column+1))
            if column+1<8 and row-1>=0:
                attacks.append((row-1,column+1))
        elif team =='b':
            if column-1<=0 and row+1<8:
                attacks.append((row+1,column-1))
            if column-1>=0 and row-1>=0:
                attacks.append((row-1,column-1))
        return attacks
    def pawn_moves(self,attacks,column, row,team):
        viable_moves=[]
        for attack in attacks:
            square=self.board[attack[1]][attack[0]]
            if square!=0 and square.get_team!=team:
                viable_moves.append(attack)

        if team =='w' and column!=7:
            if self.board[column+1][row]==0:
                viable_moves.append((row,column+1))
                if self.board[column+2][row]==0 and column==1:
                    viable_moves.append((row,column+2))

        if team =='b'and column!=0:
            if self.board[column-1][row]==0:
                viable_moves.append((row,column-1))
                if self.board[column-2][row]==0 and column==6:
                    viable_moves.append((row,column-2))
        return viable_moves

    def king_attacks(self,column,row):
        moves=[(1,0),(-1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)]
        attacks=[]
        for move in moves:
            x=row+move[0]
            y=column+move[1]
            if x in range(0,8) and y in range(0,8):
                attacks.append((x,y))
        return attacks  

    def move_helper(self, position,line):
        range_of_piece=[0,0]

        left=(line[0:position])
        left.reverse()

        right=line[position+1:8]
        if left:
            for i in range(len(left)):
                if left[i]==0:
                    range_of_piece[0]=(len(left)-1-i)
                    continue
                else:
                    range_of_piece[0]=(len(left)-1-i)#Player can move squares where the opponent is standing
                    break
        else:
            range_of_piece[0]=(position)
        if right:       
            for i in range(len(right)):
                if right[i]==0:#prblem if no other piece in row
                    range_of_piece[1]=(position+i+1)

                    continue
                else:
                    range_of_piece[1]=(position+i+1)
                    break
        else:
            range_of_piece[1]=(position)
        return range_of_piece
        

chess=setUp()

chess.update_board()
chess.display_board()
print(chess.checkmate())
#liste=chess.get_all_attacks('b')
#print(liste)
#print(f"all possible moves from white Rook: {chess.get_white_pieces()[0].get_moves(chess)}")
#print(f"all possible moves from black rook: {chess.get_black_pieces()[1].get_moves(chess)}")
#print(f"squares that need to be taken in order to preven checkmate: {chess.board}")





                    




        
