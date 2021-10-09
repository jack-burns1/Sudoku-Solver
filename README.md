# Jack Burns
# April, 2021
# sudoku.py
# README

Run program with: python3 sudoku.py [input.txt]
                  Program can only run with input file

Input Format: The board must be written in plain text. Numbers are represented
              as numbers, and blanks are represented with '-'. There can be no
              spaces between characters. Every line of the sudoku board ends
              with a newline.

The program will output the time it took to solve the puzzle in seconds, the
correct solution to the problem in the same format as the input, the list of
values that replace the blanks (in order), 

ex. input.txt
6-87-21--
4---1---2
-254-----
7-1-8-4-5
-8-----7-
5-9-6-3-1
-----675-
2---9---8
--68-52-3

ex. output

-----Elapsed Time-------
0.015490498000000002  seconds
------Completed Puzzle:-------
698752134
473618592
125439867
761983425
382541976
549267381
834126759
257394618
916875243
------------------------------
-Values used in the solution (in order of how the appear):-
93669284254152438571396978341437376915631489297
----------------------------------------------------------

This program implements backtracking with a few adjustments. These include
forward checking and variable ordering. In order to improve this, we can 
include conflict-directed backjumping in this implementation. This program
works with all valid sudoku boards including (according to the internet)
the World's hardest sudoku:

8--------
--36-----
-7--9-2--
-5---7---
----457--
---1---3-
--1----68
--85---1-
-9----4--
