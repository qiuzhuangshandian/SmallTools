import os
import sys
current_dir = os.path.split(os.path.realpath(__file__))[0]
new_path = current_dir[0:current_dir.rfind("/")]
sys.path.append(new_path)
from data_apis.crp_webservice_api import CrpDataApi

import datetime
import time

class CollectData:
    def __init__(self,interval:int=30,saveDir:str="./data") -> None:
        self.collector = CrpDataApi()
        self.save_dir = saveDir
        self.interval = interval  #s
        self.current_record_day = None
        self.current_record_minute = None
        self.current_fw = None
        self.current_fw_day = None
        self.current_fw_name = None
        self.init_dir_save()
        self.indicator_point = "CRP_TP_NJHX_0300_04_PAS100011_wr"   #"评价指标"

    def init_dir_save(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def write_titles(self,customTitle:list=[]):
        self.current_fw = open(self.current_fw_name,"w",encoding="utf-8")
        titles = ["time"]+self.collector.get_obs_titles()+customTitle
        titles = ",".join(titles)
        self.current_fw.write(titles+"\n")
        self.current_fw.flush()
        self.current_fw.close()
    
    def _write_line(self,data:list):
        self.current_fw = open(self.current_fw_name,"a",encoding="utf-8")
        line_store = ",".join(data)
        self.current_fw.write(line_store+"\n")
        self.current_fw.flush()
        self.current_fw.close()

    def build_file_name_by_time(self):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d")
        return now_time+".csv"
    
    def build_file_name_by_time_minute(self):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return now_time+".csv"

    def is_same_day(self):
        if self.current_record_day == None:
            return False
        now_day = datetime.datetime.now().strftime("%Y-%m-%d")
        if now_day == self.current_record_day:
            return True
        return False
    
    def is_same_minute(self):
        if self.current_record_minute == None:
            return False
        now_minute = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if now_minute == self.current_record_minute:
            return True
        return False

    def close_current_file(self):
        self.current_fw.close()
    def open_current_file(self):
        self.current_fw = open(self.current_fw_name,"a",encoding="utf-8")

    def set_current_record_day(self):
        self.current_record_day = datetime.datetime.now().strftime("%Y-%m-%d")

    def change_current_fw(self,new_file_name):
        if self.current_fw != None and not self.current_fw.closed:
            self.current_fw.close()
        file_path = os.path.join(self.save_dir,new_file_name)
        # self.current_fw = open(file_path,"w",encoding="utf-8")
        self.current_fw_name = file_path

    def get_indicator(self):
        indicator = self.collector.read_point_data_8093(self.indicator_point)
        return indicator

    def collect_all_time(self):
        while True:
            if not self.is_same_day():
                new_file_name = self.build_file_name_by_time_minute()
                self.change_current_fw(new_file_name)
                self.write_titles([self.indicator_point])
                self.set_current_record_day()
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = self.collector.get_current_obs_value()
            data = [now_time]+list(map(str,data))
            indicator = str(self.get_indicator())
            data.append(indicator)
            self._write_line(data)
            print(data)
            time.sleep(self.interval)

    def write_custom_data_line(self,data,custom_titles:list=[]):
        if self.current_record_day is None:
            new_file_name = self.build_file_name_by_time_minute()
            self.change_current_fw(new_file_name)
            self.write_titles(custom_titles)
            self.set_current_record_day()
        elif not self.is_same_day():
            new_file_name = self.build_file_name_by_time_minute()
            self.change_current_fw(new_file_name)
            self.write_titles(custom_titles)
            self.set_current_record_day()
        self._write_line(data)

    def collect_custom_time(self):
        pass

    def collect(self,mode:str):
        funcs = {
            "all_time":self.collect_all_time,
            "custom_time":self.collect_custom_time
        }
        if mode not in funcs.keys():
            return
        funcs[mode]()


if __name__=="__main__":
    collect = CollectData()
    collect.collect("all_time")



