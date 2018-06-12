import os  # Python module for mimicking actions done by native operating system
from pushbullet import Pushbullet  # Install this module using "sudo pip install pushbullet.py"
import pyscreenshot as ImageGrab


class PB:                           # This class contains all the functions required
    def __init__(self, api_token):
        """
        Constructor , get your API token from https://www.pushbullet.com/#settings

        """
        self.api_token = api_token

    def authorise(self):
        """
        This authorisation is required for sending /receiving messages

        """
        return Pushbullet(self.api_token)  # Returns auth keys

    def send(self, title, body):
        """
        # Sending a message to pushbullet (can be read from any device)

        """
        try:
            self.authorise().push_note(title, body)  # Sending message
            return 0                                # 0 indicates sent successfully
        except :
            print("unable to send the output to pushhbullet") 
            return -1                               # -1 indicates sent unsuccessfully

    def receive_latest(self):
        """
        For retriving the latest message

        """
        temp_pushes = self.authorise().get_pushes()
        for i in temp_pushes:
            if i.get('type') == "note":
                
                    return i.get('body')
                

    def get_cmd(self):
        """
        Parsing the latest message for retrieving the command

        """
        msg = self.receive_latest()
        if msg.split(" ")[0] == "/cmd":
            cmd = msg.split(" ")
            cmd.pop(0)
            return " ".join(cmd)

    def get_pass(self):
        msg = self.receive_latest()
        while msg.split(" ")[0] != "/pass":
            msg=self.receive_latest
        password=msg.split(" ")
        password.pop(0)
        return " ".join(password)    

    def execute_cmd(self):
        """
        For executing the command received
        """
        cmd =self.get_cmd()
        if cmd == None :
            return 9741
        # try :
        #     if self.get_cmd().split(" ")[0]=="sudo" :
        #         self.send("password Required","enter your password in this format /pass your password")
        #         password = self.get_pass()
        if self.get_cmd() == "ss":
            im =ImageGrab.grab()
            im.save("dude.png")
            return os.system('echo "ss" > templog.txt')
        else:
            return os.system(str(self.get_cmd()) + " > templog.txt")  # Executes and writes into the file templog.txt

    def send_output(self):
        """
        Sends the output from the command
        executed to pushbullet using the send function
        """
        k=self.execute_cmd()
        if k == 0:
            with open("templog.txt", 'r') as op:
                final_string = op.readlines()
                final_string = ''.join(final_string)
                print(final_string)
                if final_string == "ss\n":
                    op = open('dude.png', 'rb')
                    filedata=self.authorise().upload_file(op, "dude.png")
                    self.authorise().push_file(**filedata)
                else:
                    self.send("Output of "+self.get_cmd()+" :", final_string)
        elif k==9741 :
            print("No command found \n we did not find any latest command(which is not executed yet,all the latest commands found have been executed)")
        else :
            self.send("Output of "+self.get_cmd()+" :", "command not found / unsuccesful exit")        


if __name__ == "__main__":
    First = PB("o.yESJys6QUq8EgFI9UuD0X7NnPouz1Cbk")  # API token from https://www.pushbullet.com/#settings
    First.send_output()








