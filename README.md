# Variable brainfuck
Variable brainfuck (henceforth known as VBF) is a brainfuck (henceforth known as BF)-like language with variables and comments that compiles to brainfuck.

As of version 1.0:

* Variables are simply unique, named cells that can be moved to by specifying their single-character name anywhere outside of a comment.
* Comments run from a first instance of a `#` character to the next following newline character. BF commands inside comments are not executed. (Implementation detail: they are converted to their Unicode full-width equivalents)
* The compiler can be given a comma-separated list of variable names and locations that they will be definitely placed in.
* Variables will only be placed in locations `0` to `N-1` where N is the number of variables used in the program.
* Manual positioning of the pointer is allowed, but care must be taken to ensure that the pointer is at the same location between any two variable selections.

TODO:

* Let variables be at negative positions.
* Allow more useful location restrictions: for example
 * specify that a variable must have `K` empty cells to the left and/or right (for example for an array)
 * specify that a variable must be the left/right-most variable on the tape (for example for unbounded arrays)
 * specify that a variable should be a constant
+ Warn the programmer when a loop between two variable selections may end in a different position than it started.
+ Static analysis to re-use cells for variables that are never referenced again
+ Better than `O(n!)` running time (probably not possible in general).
