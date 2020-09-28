from find_point import amor
from winmine_api import miner

def main():
    lose_time = 0
    while True:
        Darryl = miner()
        Darryl.faster()
        Darryl.click_at(Darryl.height // 2, Darryl.width // 2)
        while not Darryl.win and not Darryl.lose:
            for operation in amor(Darryl.player_map):
                if operation[0]:
                    Darryl.click_at(operation[1] - 1, operation[2] - 1)
                else:
                    Darryl.click_at(operation[1] - 1, operation[2] - 1, button='right')
        if Darryl.lose:
            lose_time += 1
            print('LOSE! %d' % lose_time)
            Darryl.press('f2')
        else:
            print('WIN!')
            break
        Darryl.slower()

if __name__ == '__main__':
    main()
