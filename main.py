import os
from pushbullet import Pushbullet


class PB:
    def __init__(self, api_token):
        self.api_token = api_token

    def authorise(self):
        return Pushbullet(self.api_token)

    def send(self, title, body):
        self.authorise().push_note(title, body)
        return 0

    def receive_latest(self):
        tempPushes = self.authorise().get_pushes()
        for i in tempPushes:
            if i.get('type') == "note":
                if i.get('body').split(" ")[0] == "/cmd":
                    return i.get('body')

    def get_cmd(self):
        msg = self.receive_latest()
        cmd = msg.split(" ")
        cmd.pop(0)
        return " ".join(cmd)

    def execute_cmd(self):
        return os.system(self.get_cmd() + " > dude.txt")

    def send_user(self):
        with open("dude.txt", 'r') as op:
            final_string = op.readlines()
            final_string=''.join(final_string)
            self.send("Output of "+self.get_cmd()+" :", final_string)


if __name__ == "__main__":
    First = PB("o.7BKpFMfwXEiPD3UFIovsDPyU4S3Nwx7W")
    First.send_user()




