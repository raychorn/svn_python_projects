import stackless
import time

sleepingTasklets = []

def Sleep(secondsToWait):
    channel = stackless.channel()
    endTime = time.time() + secondsToWait
    sleepingTasklets.append((endTime, channel))
    sleepingTasklets.sort()
    # Block until we get sent an awakening notification.
    channel.receive()

def ManageSleepingTasklets():
    while 1:
        if len(sleepingTasklets):
            endTime = sleepingTasklets[0][0]
            if endTime <= time.time():
                channel = sleepingTasklets[0][1]
                del sleepingTasklets[0]
                # We have to send something, but it doesn't matter what as it is not used.
                channel.send(None)
        stackless.schedule()

stackless.tasklet(ManageSleepingTasklets)()