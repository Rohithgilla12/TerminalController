import os  # Python module for mimicking actions done by native operating system
from pushbullet import Pushbullet  # Install this module using "sudo pip install pushbullet.py"
import pyscreenshot as ImageGrab
import requests
import json
from bs4 import BeautifulSoup


class PB:  # This class contains all the functions required
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
            return 0  # 0 indicates sent successfully
        except:
            print("unable to send the output to pushhbullet")
            return -1  # -1 indicates sent unsuccessfully

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
            msg = self.receive_latest()
        password = msg.split(" ")
        password.pop(0)
        return " ".join(password)

    def execute_cmd(self):
        """
        For executing the command received
        """
        cmd = self.get_cmd()
        if cmd == None:
            return 9741

        if self.get_cmd().split(" ")[0] == "bye":
            self.send("password Required", "enter your password in this format /pass your password")
            password = self.get_pass()
            return os.system('echo %s|sudo -S poweroff > templog.txt' % (password))

        if self.get_cmd().split(" ")[0] == "comeback":
            self.send("password Required", "enter your password in this format /pass your password")
            password = self.get_pass()
            return os.system('echo %s|sudo -S reboot > templog.txt' % (password))

        if self.get_cmd().split(" ")[0] == "sudo":
            self.send("password Required", "enter your password in this format /pass your password")
            password = self.get_pass()
            cmd1 = cmd.split(" ")
            del (cmd1[0])
            cmd = " ".join(cmd1)
            return os.system('echo %s|sudo -S %s > templog.txt' % (password, cmd))

        if self.get_cmd() == "temp":
            send_url = 'http://freegeoip.net/json'
            r = requests.get(send_url)
            j = json.loads(r.text)
            lat = j['latitude']
            lon = j['longitude']
            url2 = "http://www.synergyenviron.com/tools/weather-info/" + str(lat) + "," + str(lon)
            r = requests.get(url2)
            soup = BeautifulSoup(r.content, 'html.parser')
            currTemp = str(soup.find('h4').text)
            command = 'echo '+'"The current temperature is : '+currTemp+'"'+" > templog.txt"
            print(command)
            return os.system(command)

        if self.get_cmd() == "ss":
            im = ImageGrab.grab()
            im.save("dude.png")
            return os.system('echo "ss" > templog.txt')
        else:
            return os.system(str(self.get_cmd()) + " > templog.txt")  # Executes and writes into the file templog.txt

    def send_output(self, cmd):
        """
        Sends the output from the command
        executed to pushbullet using the send function
        """
        k = self.execute_cmd()
        if k == 0:
            with open("templog.txt", 'r') as op:
                final_string = op.readlines()
                final_string = ''.join(final_string)
                print(final_string)
                if final_string == "ss\n":
                    op = open('dude.png', 'rb')
                    filedata = self.authorise().upload_file(op, "dude.png")
                    self.authorise().push_file(**filedata)
                else:
                    self.send("Output of " + cmd + " :", final_string)
        elif k == 9741:
            print("-")  # if no new / latest command that is not yet executed is not found

        else:
            self.send("Output of " + self.get_cmd() + " :", "command not found / unsuccesful exit")


if __name__ == "__main__":
    First = PB("API Token")  # API token from https://www.pushbullet.com/#settings
    cmd = First.get_cmd()
    First.send_output(cmd)
