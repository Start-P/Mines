import random

class MinesTableManager:
    def create_mines_table(self, mines_amount: int):
        mines_table = [
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
        ]
        x_list = [0, 1, 2, 3, 4]
        for _ in range(mines_amount):
            completed = False
            if not completed:
                x = int(random.choice(x_list))
                except_bomb = len([i for i in mines_table[x] if i == '']) - 1
                if except_bomb < 0:
                    print(x_list, x)
                    x_list.remove(x)
                    continue
                y = int(random.choice(str(except_bomb)))
                #print(x)
                mines_table[x][y] = "💣"
                completed = True
        for x in range(0, 5):
                replaced_mines_table = []
                for y in range(0, 5):
                    table = mines_table[x][y]
                    table = table if table == "💣" else "？"
                    replaced_mines_table.append(table)
                mines_table[x] = replaced_mines_table
        self.already_checked = mines_amount
        self.mines_table = mines_table
        return mines_table
        
    def check_bomb(self, x: int, y: int):
        print(self.already_checked)
        if self.already_checked == 25:
            return mines_table, "GameSet"    
        position = self.mines_table[x][y]
        if position == "💣":
            return False, "Bombed"
        elif position == "💎":
            return False, "Checked"
        else:
            self.already_checked += 1
            self.mines_table[x][y] = "💎"
            return self.mines_table, "Safe"
            
               
                  
    def mask_bomb(self):
        for x in range(0, 5):
            for y in range(0, 5):
                mine = self.mines_table[x][y]
                self.mines_table[x][y] = mine if mine != "💣" else "？"
        return self.mines_table

if __name__ == "__main__":
    mines = MinesTableManager()
    table = mines.create_mines_table(1)
    print(table)
    while True:
        try:
            x = int(input("x >> ")) - 1
            y = int(input("y >> ")) - 1
            checked = mines.check_bomb(x, y)
        except:
            continue
        if type(checked[0]) == list and checked[1] == "Safe":
            for i in mines.mask_bomb():
                print(i)
        else:
            if checked[1] == "Checked":
                print("Already Checked")
                continue
            else:
                print(checked[1])
                break
