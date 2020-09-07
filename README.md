# GO
Go game, ruleset here:
https://www.britgo.org/intro/intro2.html
to launch navigate to the location where you have cloned 
the GO repo and type python go_game/game.py -h
for help which will result in the following

```buildoutcfg
usage: game.py [-h] --black-player-name BLACK_PLAYER_NAME --white-player-name
               WHITE_PLAYER_NAME --board-size BOARD_SIZE

Go Game! Black player always goes first!

optional arguments:
  -h, --help            show this help message and exit
  --black-player-name BLACK_PLAYER_NAME
                        Player one name
  --white-player-name WHITE_PLAYER_NAME
                        Player two name
  --board-size BOARD_SIZE
                        Number of squares on each side of board (9, 13 or 19)
(base) Arnas-MBP:go_game arnafriend$ 

```

An example game launch would then be:
python go_game/game.py --black-player-name arna --white-player-name Sean --board-size 13

For 
```buildoutcfg

```