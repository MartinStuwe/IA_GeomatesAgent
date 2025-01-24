# geomates
This is a clone of the 'geometry friends' competition that was run at IJCAI for several years. This 2D physical simulation game is intended to challenge autonomous agents in a multi-agent setting.

## Gameplay
Two players -- disc and rectangle -- jointly need to collect diamonds in a 2d platform environment. Players are controlled by one autonomous agent (or human). The disc player has the ability to jump up, while the rectangle can shape its shape by adjusting its height/width ratio. Both players can move left and right and are subject to gravity.

Levels are defined in levels.lisp, see there for how to design your own levels.

## Principle of Operation
The game is implemented as a server that connects to agents and the GUI using TCP/IP sockets, sending scene information as s-expressions. The GUI is written in JavaScript and should run in any modern web browser.
For convenience of testing, you can connect to the server by telnet to control an agent. See documentation inside geomates.lisp for all the glory details.

## Requirements
The game requires a 3.0 version of the box2d library to be installed. As of 2025, 2.x versions are still widely shipped with package management systems. This are incompatible with 3.x versions and will not work! Therefore, [download the original](https://github.com/erincatto/box2d) repository and build the library yourself.

Additionally, [SBCL](https://sbcl.org) as LISP compiler is required. If you have ACT-R installed, you probably already have SBCL.

### Windows
You may experience issues compiling box2d and need to use linux virtualization.
Download [Docker](https://www.docker.com) and use the provided Dockerfile to run the game environment by <pre><code>docker run -p 8000:8000 -p 45678:45678 geomates:latest sbcl --script geomates.lisp</code></pre>. Note that you cannot provide own levels or change game parameters.

### Linux
Just follow the instructions for building below. In case you don't have clang installed, change the compiler to gcc in the Makefile.

### MacOS
Just follow the instructions for building below. Make sure to have developer tools installed. You can install telnet using [homebrew](https://brew.sh): <pre><code>brew install telnet</code></pre>

## Building
Only a single dynamic liberary needs to be build that wraps around box2d's static library. To do so, edit the Makefile to adjust the paths to where box2s include files and the static library can be found (box2d does not need to be installed system-wide).

## Running the game
```sbcl --script geomates.lisp```

Then, open viewer.html in a web browser and start your agents. Once both agents have connected, the game starts. It ends when all levels have been played. The list of levels is loaded from levels.lisp.

## Author and License 

The game is distributed as open source software as is. Author is Diedrich Wolter, address all requests to him. Geomates employs two Lisp packages provided under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) for open source software: [base64](https://github.com/massung/base64) and [sha1](https://github.com/massung/sha1).
