{{ product_name }} Version {{ product_version }}

This is a very simplistic view of a minimalistic message bus that transmits information from one process to another
through the Windows filesystem.

Place a file in message_box1 and the file will be moved into message_box2 and then on to message_box3.

Why is this useful ?

TCP/IP can be a bit problematic expecially when a required listener does not exist.  REST Web Service communications
between processes can fail when a listener is not available.

Simple Message Bus can resolve issues when a process may not be available all the time. Messages in the form of
small files will collect in a directory until the process that's supposed to handle them comes alive.

Give this demo a try and look at the source code.

Enjoy.
