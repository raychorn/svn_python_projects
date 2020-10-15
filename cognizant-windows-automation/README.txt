This is an example of how Windows Automation can be done using Python.

You can use the pattern shown in this file to accomplish tasks like the following, using only Windows Automation techniques:

(1). Automate logging into Core.

(a). Wait for user to click on the username field, then issue the username into the field by issuing keystroke messages.

(b). Then wait for user to click on the password field, then issue the password into the field by issuing keystroke messages.

(c). Then wait for the user to click on the login button.

Settling Mode is when you allow the user to perform some interaction you can record, if you wish, such as the mouse moving or a click at a particular screen position.

Listening Mode is when you are capturing Windows Events for later playback.

You can use win32api functions to issue Windows Messages into a particular Window such as the browser.

This will allow you to produce your own little Windows Automation Support App you can use to simulate user actions for the purpose of making the determination as to how a certain bug might be fixed.

You can also produce some Stress Test Code to more fully exorcise Core in ways you might not have access to under normal circumstances.
