#!/usr/bin/python3
# ! Watermark telegram bot by uidops

import sys  #* System-specific parameters and functions.
import time  #* Time access and conversions.
import os #* Miscellaneous operating system interfaces.

import telepot  #* Python framework for Telegram Bot API.
import telepot.loop  #* Python framework for Telegram Bot API message loop handler.
from colorama import (  #* Simple cross-platform API for printing colored terminal text.
    Fore, init)
from PIL import Image  #* Python Imaging Library.

init() #TODO: a initialization for use colorama.

print(Fore.GREEN+"Starting ...\n"+Fore.RESET)
api = "1595460418:AAHOf_-PrppgPU_jlQkGuoFo18tPDHAFNvc" #! Telegram Bot API.
bot = telepot.Bot(api) #* a initialization for Telegram Bot.

class ImageProcessor():
    """ Image processor class for watermark handling. """

    def __init__(self, file):
        """ initialization method. """

        self.file_name_origin = file # Picture file name.
        self.logo_file = "logo.png" #! Watermark file name.

        self.logoIm = Image.open(self.logo_file) #* Open watermark image for processing.
        self.logo_width, self.logo_height = self.logoIm.size #* Get the width and height of the watermark image.

        self.im = Image.open(self.file_name_origin) #* Open Picture image for processing.
        self.width, self.height = self.im.size #* Get the width and height of the image.

    def add_watermark(self):
        """ a method for add watermark to picture. """


        if (self.im.size[0] < self.logoIm.size[0]) or (self.im.size[1] < self.logoIm.size[1]): #* Check the image size relative to the watermark to resize.
            self.logoIm = self.logoIm.resize((50, 50)) #! Resize watermark to (50,50). Do not change it.
            seg = (self.width-65, self.height-66) #! Change position. Do not change it.

        else:
            if self.im.size[1] >= 1000: #* Check the image size relative to the watermark to resize.
                self.logoIm = self.logoIm.resize((150, 150)) #! Resize watermark to (150,150). Do not change it.
                seg = (self.width-156, self.height-156) #! Change position. Do not change it.

            else:
                self.logoIm = self.logoIm.resize((70, 70)) #! Resize watermark to (70,70). Do not change it.
                seg = (self.width-76, self.height-76) #! Change position. Do not change it.

        self.im.paste(self.logoIm, seg, self.logoIm) #TODO: Paste watermark to picture in our position.
        self.file_name = "{}_logo.{}".format(".".join(self.file_name_origin.split(".")[:-1]), self.file_name_origin.split(".")[-1]) #* New image file name.
        self.im.save(self.file_name) #* Save image to a file for sharing.

    def get_output_name(self):
        """ Returns the file name """
        return self.file_name


def robot_handler(msg):
    """ Telegram Bot handler funcation. """

    user_id = msg["chat"]["id"] #* Get chat ID.
    msg_id = msg["message_id"] #* Get message ID.

    if ("photo" in msg.keys()): #* Check if the received data is really a file or something.
        media_id = msg["photo"][-1]["file_id"] #* Get file ID for downloading,
        file_name = "./temp/{}.jpg".format(media_id) #* Generate a name for saving file based on file ID.

    elif ("document" in msg.keys() and (msg["document"]["mime_type"] == "image/png" or msg["document"]["mime_type"] == "image/jpeg")): #* Check if the received data is really a file or something.
        media_id = msg["document"]["file_id"] #* Get file ID for downloading.
        if msg["document"]["mime_type"] == "image/png": #* Check that the image format [jpeg or png].
            file_name = "./temp/{}.png".format(media_id) #* Generate a name for saving file based on file ID and image format.

        elif msg["document"]["mime_type"] == "image/jpeg": #* Check that the image format [jpeg or png].
            file_name = "./temp/{}.jpg".format(media_id) #* Generate a name for saving file based on file ID and image format.


    else:
        bot.sendMessage(chat_id=user_id, text="message or file not supported", reply_to_message_id=msg_id) #* Sending a message that the data sent is not an image.
        return 0 #* Return 0 and exit from funcation.


    bot.download_file(file_id=media_id, dest=file_name) #* Download file from Telegram server.
    img = ImageProcessor(file_name) #* Initialization image processing,
    img.add_watermark() #* add watermark to picture.

    if "document" in msg.keys(): #* Check that the picture should be sent as a file or photo.
        bot.sendDocument(chat_id=user_id, document=open(img.get_output_name(), "rb"), reply_to_message_id=msg_id) #* Send file to client.

    else:
        bot.sendPhoto(chat_id=user_id, photo=open(img.get_output_name(), "rb"), reply_to_message_id=msg_id) #* Send photo to client.



if __name__ == "__main__": #* Check to see it is entered as a library.
    if ! os.path.isdir("temp"):
        os.mkdir("temp")

    try:
        me = bot.getMe() #* Get information about the robot.
    except telepot.exception.UnauthorizedError:
        print(Fore.RED+"UnauthorizedError"+Fore.RESET)
        sys.exit(1)

    """ Print information"""

    for i in me.keys():
        print(Fore.MAGENTA+"\t{}: {}{}".format(i, Fore.LIGHTBLUE_EX ,me[i])+Fore.RESET)

    telepot.loop.MessageLoop(bot, robot_handler).run_as_thread() #! Run a robot loop to receive and process messages and execute them as threads. Do not change it

    print (Fore.CYAN+"\nCtrl+C for shutdown..."+Fore.RESET)

    try:
        while 1:
            for file in os.scandir("./temp"):
                os.remove(file.path)
            time.sleep(18000) #! Sleep for 5h.

    except KeyboardInterrupt: #* Prevent error when receiving Interrupt signal.
        sys.exit("\n") #* Print a new line and exit from script.

