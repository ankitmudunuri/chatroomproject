# Talk.py
## Local Area Network Chatroom/Encrypted 1-to-1 Communication App

This is just a basic LAN chatroom/1-to-1 chat communication app that I made in Python using the threading, socket, and PyQt5 libraries. It acts as a way to communicate with people over a local network and on a certain port.

## Documentation
To start using it, first go to your command line and navigate to the directory that this repo's files are in. Then, enter ```pip install -r requirements.txt``` to install PyQt5 and rsa libraries. Finally, run the ```main.py``` file using ```python main.py``` and it should launch!

The instructions below explain how to use this app.

### Chatroom
- To host, toggle the host mode checkbox and enter the port number that you want to host on (404 is the default). Press the chatroom button after all of the information is filled out.
- To connect as a client, enter the target IP address of the server that you want to connect to, as well as the port number that the server is hosting on. Enter the nickname that you want to connect as, and make sure the host mode checkbox is not toggled, and then press the chatroom button.

### Encrypted 1-to-1 Chat
- To host, it is the same process as for the chatroom, except instead of clicking on the chatroom button click on "1-to-1".
- To connect as a client, enter the IP address and port number of the host client and make sure that the host checkbox is not toggled. After that, press the 1-to-1 button.

### Chatting
- The UI is fairly simple and reminiscent of early chatrooms (such as Pictochat on the DS, which I grew up with).
- To chat, just type in whatever you want to say into the box that says "Enter text here..." and then press ENTER to send (I will add an actual send button soon once I add some more functionality and iron out some bugs).

### Known Bugs and Issues
- The actual server will not close properly if you exit out of the server hosting screen, thus requiring you to have to restart the app every time you want to host a new server.

## Future Features
- Ability to close the app without having to close the entire terminal (trust me I know its very annoying)
- Ability to host multiple servers from the same instance of the app
- Server can send messages in chatroom
- Server can kick and ban people by nickname or IP
