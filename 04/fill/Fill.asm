// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here
@SCREEN
D=A
@sum
M=D
@addr
M=0

(LOOP)//paint pixels black or white
@KBD
D=M
@black
D;JNE
@white
0;JMP

(white)
@sum
A=M
M=0
@END
0;JMP

(black)
@sum
A=M
M=-1
@END
0;JMP

//increase position of memory by one
(END)
@1
D=A
@sum
M=M+D

//check if sum<SCREEN+8191
@SCREEN
D=A
@8191
D=D+A
@sum
D=D-M
@LOOP
D;JGE//restart loop if sum>=8191

@SCREEN
D=A
@sum
M=D
@LOOP
0;JMP //restart loop
