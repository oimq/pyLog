# Logging modules
import traceback
from .metadata import *
from datetime import datetime
from copy import deepcopy
import os, pwd

class Logger() :
    def __init__(self, wpath :str =".", isWrite :bool =False) :
        self.name, self.level, self.format = "", 1, "{}"
        self.wpath, self.isWrite, self.cur_datetime = wpath, isWrite, str(datetime.now()).replace(" ", "-")

        self.COLOR = {
            k:"".join([PALLETE[c] for c in v])+"{}"+(PALLETE['END']*len(v))
            for k,v in LOG['DEFAULT']['color'].items()
        }
        for key in LOG['KEYS'] : self.set(key, None)

        self.set_file_name()

    def set_write(self, wpath :str =".") :
        self.wpath, self.isWrite = wpath, True

    def set_file_name(self) :
        self.fname = "log-{0}-{1}-{2}.log".format(pwd.getpwuid(os.getuid())[0], self.name, self.cur_datetime)

    def set(self, key :str, value :any) :
        if key not in LOG['KEYS'] : return print("Sorry, We only handle {} options.".format(LOG['KEYS']))
        try :
            if value == None : 
                value = LOG['DEFAULT'][key]
            if key == "level" :
                # print("Logger : Change the level from {} to {}.".format(LOG['LEVEL'][self.level], LOG['LEVEL'][value]))
                self.level = value
            elif key == "name" :
                self.name = value
                self.set_file_name()
            elif key == "format" :
                self.format = value
        except Exception as e :
            traceback.print_exc()
            return print("ERROR SET : {}".format(e))
        else :
            LOG['DEFAULT'][key] = value 

    def find_level_number(self, lev :str) :
        if   lev in ["i", "info"]     : return 1
        elif lev in ["d", "debug"]    : return 0
        elif lev in ["w", "warning"]  : return 2
        elif lev in ["e", "error"]    : return 3
        elif lev in ["c", "critical"] : return 4

    def log(self, msg :any ="", lev :int =1) :
        if type(lev) == type("") : lev = self.find_level_number(lev)
        if lev < self.level : return

        if   type(msg) == type([]) : msg = ", ".join(msg) 
        elif type(msg) == type(()) : msg = " : ".join(msg)
        elif type(msg) == type("") : pass
        else : return
        
        sstr = self.speak(msg, lev)
        if self.isWrite : self.write(sstr)

    def write(self, sstr :str) :
        try :
            with open(os.path.join(self.wpath, self.fname), 'a') as openfile :
                openfile.write(sstr+"\n")
        except Exception as e :
            print("ERROR WRITE :", e)

    def formatting(self, msg :str, level :int) :
        pstr = deepcopy(self.format)
        if "$time"      in pstr : pstr=pstr.replace("$time", str(datetime.now()))
        if "$name"      in pstr : pstr=pstr.replace("$name", self.name)
        if "$level"     in pstr : pstr=pstr.replace("$level", LOG['LEVEL'][level])
        if "$message"   in pstr : pstr=pstr.replace("$message", msg)
        return pstr
    
    def speak(self, msg :str, level :int) :
        msg = self.formatting(msg, level)
        print(self.COLOR[level].format(msg))
        return msg

    