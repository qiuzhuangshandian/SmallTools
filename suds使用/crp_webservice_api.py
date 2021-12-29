from suds.client import Client
import time
import numpy as np
import pprint
import collections

figPoints = [
    "CRP_TP_NJHX_0300_04_NXXC001",
    "CRP_TP_NJHX_0300_04_NXXC002",
    "CRP_TP_NJHX_0300_04_NXXC003",
    "CRP_TP_NJHX_0300_04_NXXC004",
    "CRP_TP_NJHX_0300_04_NXXC005",
    "CRP_TP_NJHX_0300_04_NXXC006",
    "CRP_TP_NJHX_0300_04_NXXC007",
    "CRP_TP_NJHX_0300_04_NXXC008",
    "CRP_TP_NJHX_0300_04_NXXC009",
    "CRP_TP_NJHX_0300_04_NXXC010",
    "CRP_TP_NJHX_0300_05_NXXC001",
    "CRP_TP_NJHX_0300_05_NXXC002",
    "CRP_TP_NJHX_0300_05_NXXC003",
    "CRP_TP_NJHX_0300_05_NXXC004",
    "CRP_TP_NJHX_0300_05_NXXC005",
    "CRP_TP_NJHX_0300_05_NXXC006",
    "CRP_TP_NJHX_0300_05_NXXC007",
    "CRP_TP_NJHX_0300_05_NXXC008",
    "CRP_TP_NJHX_0300_05_NXXC009",
    "CRP_TP_NJHX_0300_05_NXXC010"
]

obsPoints = collections.OrderedDict()
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_MW1"] = "化工园_#4机组_发电机功率"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_39M01ABPIC"] = "化工园_#4机组_4A循环水泵变频器转速"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_06TE01A"] = "化工园_#4机组_4A送风机入口空气温度"
obsPoints["CRP_TP_NJHX_0300_04_JSNH_PUBSYS04_AO040007_AC"] = "化工园_#4机组_一级工业供热流量_AC"
obsPoints["CRP_TP_NJHX_0300_04_JSNH_PUBSYS04_AO040007B_AC"] = "化工园_#4机组_二级供热供热流量_AC"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI001"] = "化工园_#4机组_4A循环水泵电流"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI096"] = "化工园_#4机组_4B循环水泵电流"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_39PT03"] = "化工园_#4机组_循环水泵出口母管压力"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE03A"] = "化工园_#4机组_4A凝汽器循环冷却水进口温度1"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE15A"] = "化工园_#4机组_4A凝汽器循环冷却水出口温度1"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE15B"] = "化工园_#4机组_4B凝汽器循环冷却水出口温度"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_39LT11"] = "化工园_#4机组_冷却塔水位"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE251"] = "化工园_#4机组_汽机低压缸排汽温度(前右)"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE252"] = "化工园_#4机组_汽机低压缸排汽温度(后左)"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_33PT01"] = "化工园_#4机组_凝汽器真空"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_26LT08A"] = "化工园_#4机组_热井水位A"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_26FT31"] = "化工园_#4机组_轴加出口凝水流量"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_STEAM_FLOW"] = "化工园_#4机组_主蒸汽流量"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_26TE28"] = "化工园_#4机组_凝水温度"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI253"] = "化工园_#4机组_6KV4A段母线AB相间电压"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI256"] = "化工园_#4机组_6KV4B段母线AB相间电压"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE01"] = "化工园_#4机组_主蒸汽母管温度1"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_23PT02"] = "化工园_#4机组_主蒸汽压力2"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_02TE32A"] = "化工园_#4机组_高再出口温度(A侧)2"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_1IECV1POS"] = "中压缸上画的第一个阀开度"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_1LCVPOS"] = "中压缸上画的虚线（第二个阀开度）"

obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT72"] = "化工园_#4机组_一级减温器喷水流量1"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT78A"] = "化工园_#4机组_二级减温器喷水流量(A侧)1"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT78B"] = "化工园_#4机组_二级减温器喷水流量(B侧)1"

obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT45A"] = "化工园_#4机组_再热器事故喷水流量A"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT44B"] = "化工园_#4机组_再热器微量喷水流量B"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT45B"] = "化工园_#4机组_再热器事故喷水流量B"
obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT44A"] = "化工园_#4机组_再热器微量喷水流量A"

# obsPoints["CRP_TP_NJHX_0300_04_PAS100011_wr"] = "评价指标"


# obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_1IECV1POS"] = "中压缸上画的第一个阀开度"
# obsPoints["CRP_TP_NJHX_0300_04_SIS_U04DCS_1LCVPOS"] = "中压缸上画的虚线（第二个阀开度）"

# obsPoints = {
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_MW1"            :"化工园_#4机组_发电机功率",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_39M01ABPIC"     :"化工园_#4机组_4A循环水泵变频器转速",      # action
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_06TE01A"        :"化工园_#4机组_4A送风机入口空气温度",
#     "CRP_TP_NJHX_0300_04_JSNH_PUBSYS04_AO040007_AC" :"化工园_#4机组_一级工业供热流量_AC",
#     "CRP_TP_NJHX_0300_04_JSNH_PUBSYS04_AO040007B_AC":"化工园_#4机组_二级供热供热流量_AC",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI001"      :"化工园_#4机组_4A循环水泵电流",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI096"      :"化工园_#4机组_4B循环水泵电流",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_39PT03"         :"化工园_#4机组_循环水泵出口母管压力",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE03A"        :"化工园_#4机组_4A凝汽器循环冷却水进口温度1",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE15A"        :"化工园_#4机组_4A凝汽器循环冷却水出口温度1",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE15B"        :"化工园_#4机组_4B凝汽器循环冷却水出口温度",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_39LT11"         :"化工园_#4机组_冷却塔水位",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE251"        :"化工园_#4机组_汽机低压缸排汽温度(前右)",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE252"        :"化工园_#4机组_汽机低压缸排汽温度(后左)",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_33PT01"         :"化工园_#4机组_凝汽器真空",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_26LT08A"        :"化工园_#4机组_热井水位A",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_26FT31"         :"化工园_#4机组_轴加出口凝水流量",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_STEAM_FLOW"     :"化工园_#4机组_主蒸汽流量",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_26TE28"         :"化工园_#4机组_凝水温度",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI253"      :"化工园_#4机组_6KV4A段母线AB相间电压",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI256"      :"化工园_#4机组_6KV4B段母线AB相间电压",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE01"         :"化工园_#4机组_主蒸汽母管温度1",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_23PT02"         :"化工园_#4机组_主蒸汽压力2",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_02TE32A"        :"化工园_#4机组_高再出口温度(A侧)2",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_1IECV1POS"      :"中压缸上画的第一个阀开度",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_1LCVPOS"        :"中压缸上画的虚线（第二个阀开度）",

#     # 加和为过热总减温水流量 
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT72"         :"化工园_#4机组_一级减温器喷水流量1",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT78A"        :"化工园_#4机组_二级减温器喷水流量(A侧)1",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT78B"        :"化工园_#4机组_二级减温器喷水流量(B侧)1",

#     # 加和为再热总减温水流量
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT45A"        :"化工园_#4机组_再热器事故喷水流量A",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT44B"        :"化工园_#4机组_再热器微量喷水流量B",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT45B"        :"化工园_#4机组_再热器事故喷水流量B",
#     "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT44A"        :"化工园_#4机组_再热器微量喷水流量A"
# }

excelPoints = [
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_MW1",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_39M01ABPIC",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_06TE01A",
    "CRP_TP_NJHX_0300_04_JSNH_PUBSYS04_AO040007_AC",
    "CRP_TP_NJHX_0300_04_JSNH_PUBSYS04_AO040007B_AC",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI001",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI096",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_39PT03",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE03A",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE15A",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_39TE15B",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_39LT11",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE251",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE252",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_33PT01",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_26LT08A",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_26FT31",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_STEAM_FLOW",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_26TE28",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI253",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_ECS_AI256",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_23TE01",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_23PT02",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_02TE32A",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_1IECV1POS",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_1LCVPOS",

    "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT72",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT78A",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT78B",

    "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT45A",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT44B",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT45B",
    "CRP_TP_NJHX_0300_04_SIS_U04DCS_27FT44A"
]

indicator_point =  "CRP_TP_NJHX_0300_04_PAS100011_wr"    #"评价指标"

class CrpDataApi:
    def __init__(self) -> None:
        self.read_url = "http://10.61.16.108:8094/WebService.asmx?wsdl"
        self.write_url = "http://10.61.16.108:8093/WebService.asmx?wsdl"
        self.client_read = Client(self.read_url)
        self.client_write = Client(self.write_url)
        self.service_read = self.client_read.service["WebServiceSoap12"]
        self.service_write = self.client_write.service["WebServiceSoap12"]
        self.factory_read = self.client_read.factory
        self.factory_write = self.client_write.factory
        self.obs_points = obsPoints
    
    def get_obs_titles(self):
        return list(self.obs_points.keys())

    def read_point_data(self,point:str):
        return self.service_read.GetRealValue(point)
    
    def read_point_data_8093(self,point:str):
        return self.service_write.GetRealValue(point)

    def write_point_data(self,points,values,times):
        return self.service_write.SendMultiPoint(points,values,times)

    def build_crp_string_array(self,points:list):
        tmp_points = self.factory_write.create("ArrayOfString")
        for point in points:
            tmp_points.string.append(point)
        return tmp_points

    def build_crp_double_array(self,values:list):
        tmp_values = self.factory_write.create("ArrayOfDouble")
        for value in values:
            tmp_values.double.append(value)
        return tmp_values

    def build_crp_int_array(self,time_points:list):
        tmp_times = self.factory_write.create("ArrayOfInt")
        for time_point in time_points:
            tmp_times.int.append(time_point)
        return tmp_times

    def read_point_data_list_with_time(self,points):
        return self.service_read.GetRealTimeValueList(points)
    
    def read_point_data_list_without_time(self,points):
        data = self.service_read.GetRealValueList(points)
        return data.double

    def get_current_obs_value(self):
        points = list(self.obs_points.keys())
        crp_points = self.build_crp_string_array(points)
        data = self.read_point_data_list_without_time(crp_points)
        return data

    def read_point_data_list_8093(self,points):
        return self.service_write.GetRealTimeValueList(points)

    def get_realtime_obs(self):
        points = excelPoints
        crp_points = self.build_crp_string_array(points)
        crp_data = self.read_point_data_list(crp_points)
        def get_value(item):
            item = str(item)
            return float(item.split(",")[-1])
        crp_data = {points[i]:get_value(item) for i,item in enumerate(crp_data.string)}
        strtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        crp_data["time_point"] = strtime
        return crp_data

    def show_current_obs(self):
        points = list(self.obs_points.keys())
        data = self.get_current_obs_value()
        data_dict = collections.OrderedDict()
        for idx, obs_value in enumerate(data):
            tmp_key = points[idx]+"-"+self.obs_points[points[idx]]
            data_dict[tmp_key] = obs_value
        indicator = self.read_point_data_8093(indicator_point)
        print("*"*100)
        for k,v in data_dict.items():
            print(k,":",v)
        print(indicator_point+"-指标值:",indicator)
        print("*"*100)
    
    def get_index_by_point_name(self,name):
        titles = self.get_obs_titles()
        for i,item in enumerate(titles):
            if name == item:
                return i
        return None
            
def write_test():
    crp = CrpDataApi()
    points_w = crp.build_crp_string_array(figPoints[0:5])
    values_w = crp.build_crp_double_array([16.234,1.234,34.5,1.234,1.234])
    times_now = [int(time.time()) for _ in range(5)]
    times_w = crp.build_crp_int_array(times_now)
    result = crp.write_point_data(points_w, values_w, times_w)
    print("write result:",result)

    print("read api 1:")
    for point in figPoints:
        data = crp.read_point_data(point)
        print(point,data)
    print("*"*50)
    for point in excelPoints:
        data = crp.read_point_data(point)
        print(data)

    print("read api 2:")
    for point in figPoints:
        data = crp.read_point_data_8093(point)
        print(point,data)
    print("*"*50)
    for point in excelPoints:
        data = crp.read_point_data_8093(point)
        print(data)

def get_single_point_data():
    crp = CrpDataApi()
    data = crp.read_point_data(excelPoints[-1])
    print(data)

def get_points_list_values_test():
    crp = CrpDataApi()
    points_r = crp.build_crp_string_array(excelPoints)
    data = crp.read_point_data_list_with_time(points_r)
    print(data)
    # print(data)
    # data = crp.read_point_data_list_8093(points_r)
    # print(data.string)
    # print(data.string[0], type(data.string[0]))

def get_points_list_values_test_without_time():
    crp = CrpDataApi()
    points_r = crp.build_crp_string_array(excelPoints)
    data = crp.read_point_data_list_without_time(points_r)
    print(data,type(data))


def test_get_obs():
    crp = CrpDataApi()
    data = crp.get_realtime_obs()
    for k,v in data.items():
        print(k,":",v)

def show_obs():
    crp = CrpDataApi()
    crp.show_current_obs()
if __name__=="__main__":
    write_test()
    # test_get_obs()
    # get_points_list_values_test()
    # get_points_list_values_test_without_time()
    # show_obs()


