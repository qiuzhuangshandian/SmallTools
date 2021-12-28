import mmap
import struct
import pprint
import time
import pprint
import numpy as np
from policy1.policy1 import ModelInference as modelinfer1
from policy2.policy2 import ModelInference as modelinfer2

class SimuPolixir:
    def __init__(self) -> None:
        self.typeMode = 19*"f"
        self.size = 4*19
        self.tagName_obs = 'simu_polixir_obs'
        self.mmap_file = mmap.mmap(-1, self.size, access = mmap.ACCESS_READ, tagname = self.tagName_obs)
        self.obsTitles = [
            "30LOAD","30HYA00DU001OUT","30TOTAL-COAL-T/H","30LAB40CT301","30TOTAL-AIR-FLOW","30MSTEAM-FLOW",
            "30HAH10CT609","30LAE12CF101F","30HAH16CT604","30LAE12AA501AI","30HAH21CT604","30LAE11AA501AI",
            "30LAB11CT609","30LAE14CF101F","30HAH16CT610","30LAE14AA501AI","30HAH22CT604","30LAE13AA501AI",
            "30LAB12CT609"
        ]

        self.tagName_action = 'simu_polixir_action'
        self.mmap_file_action = mmap.mmap(-1, 4*5, access = mmap.ACCESS_WRITE, tagname = self.tagName_action)
        self.actionTitles = ["30LAE12AA501AI","30LAE11AA501AI","30LAE14AA501AI","30LAE13AA501AI"]
        self.obsNp = None

        self.tagName_sim_write = 'simu_polixir_obs'
        self.sim_mmap_file = mmap.mmap(-1, 4*4, access = mmap.ACCESS_WRITE, tagname = self.tagName_sim_write)

    def getSimuObs(self):
        self.mmap_file.seek(0)
        info_str = self.mmap_file.read(self.size)
        x = struct.unpack(self.typeMode, info_str)
        simuObs = {}
        for idx, title in enumerate(self.obsTitles):
            simuObs[title] = x[idx]
        
        return simuObs
    
    def getSimuObsNp(self):
        simuObs = self.getSimuObs()
        obsList = []
        obsList = [simuObs[title] for title in self.obsTitles]
        self.obsNp = np.array(obsList)
        print(self.obsNp)
        # return obsNp

    def writeSimuActionByCplusplus(self,action:list):
        self.mmap_file_action.seek(0)
        packX = struct.pack(5*"f",*action)
        self.mmap_file_action.write(packX)

    def writeSimActDirect(self):
        self.sim_mmap_file.seek(0)
        packX = struct.pack(5*"f",*action)
        self.sim_mmap_file.write(packX)

    def closeMmap(self):
        self.mmap_file_action.close()

class DataBuff:
    def __init__(self) -> None:
        self.buff = np.zeros([10,19])
        self.n = 0

    def add(self, data:np.ndarray):
        if self.n < 10:
            self.buff[self.n] = data
            self.n += 1
            return 
        self.buff[0:9] = self.buff[1:10]
        self.buff[9] = data


class SimuControl:
    def __init__(self) -> None:
        self.simu = SimuPolixir()
        self.server = modelinfer2()
        self.dataBuf = DataBuff()
        # Algo : BC
        # Revive : 6
        # Mode: Easy
        # static_obs:20, obs:60, act:2, obs_transition:3
        # static_obs: 10*2 [主蒸汽流量,汽水分离器出口温度]
        # obs: 10*6  [一级减温水调节阀开度,一级减温出口温度,二级减温水调节阀开度,二级减温出口温度,末级过热器出口温度,末级过热器出口温度与目标温度差值]
        # act: 2 [下一时刻一级减温水调节阀开度,下一时刻二级减温水调节阀开度]
        self.target_temperature = 570
        self.static_title = ["30MSTEAM-FLOW","30HAH10CT609"]
        self.static_title_index = self.getIndexByTitle(self.static_title, self.simu.obsTitles)
        self.obs_title_A = ["30LAE12AA501AI","30HAH16CT604","30LAE11AA501AI","30HAH21CT604","30LAB11CT609"]
        self.obs_title_A_index = self.getIndexByTitle(self.obs_title_A, self.simu.obsTitles)
        self.obs_diff_title_A = ["diff"]
        self.finalTemperature_title_A = ["30LAB11CT609"]
        self.finalTemperature_title_A_index = self.getIndexByTitle(self.finalTemperature_title_A, self.simu.obsTitles)

        self.obs_title_B = ["30LAE14AA501AI","30HAH16CT610","30LAE13AA501AI","30HAH22CT604","30LAB12CT609"]
        self.obs_title_B_index = self.getIndexByTitle(self.obs_title_B, self.simu.obsTitles)
        self.obs_diff_title_B = ["diff"]
        self.finalTemperature_title_B = ["30LAB12CT609"]
        self.finalTemperature_title_B_index = self.getIndexByTitle(self.finalTemperature_title_B, self.simu.obsTitles)
        self.action = []

    def getIndexByTitle(self,title1:list, title2:list):
        index = []
        for item1 in title1:
            for i,item2 in enumerate(title2):
                if item1 == item2:
                    index.append(i)
        return index

    def getInputData_A(self):
        self.simu.getSimuObsNp()
        self.dataBuf.add(self.simu.obsNp)
        if self.dataBuf.n < 10:
            return [False]
        static_obs = self.dataBuf.buff[...,self.static_title_index]
        obs = self.dataBuf.buff[..., self.obs_title_A_index]
        finalTemperature_diff = self.dataBuf.buff[..., self.finalTemperature_title_A_index] - self.target_temperature
        obs = np.concatenate([obs,finalTemperature_diff],axis=-1)

        static_obs = static_obs.reshape(-1)
        obs = obs.reshape(-1)

        return [True, {"static_obs" : static_obs, "obs" : obs}]

    def getInputData_B(self):
        static_obs = self.dataBuf.buff[...,self.static_title_index]
        obs = self.dataBuf.buff[..., self.obs_title_B_index]
        finalTemperature_diff = self.dataBuf.buff[..., self.finalTemperature_title_B_index]- self.target_temperature
        obs = np.concatenate([obs,finalTemperature_diff],axis=-1)

        static_obs = static_obs.reshape(-1)
        obs = obs.reshape(-1)

        return [True, {"static_obs" : static_obs, "obs" : obs}]

    def infer(self):
        inputdata = self.getInputData_A()
        # pprint.pprint(inputdata)
        if not inputdata[0]:
            print("getInputData result is false!")
            print("self.dataBuf.n = ",self.dataBuf.n,"less than 10, wait...")
            return None
        res_a = self.server.policy_infer(inputdata[1])

        inputdata = self.getInputData_B()
        # pprint.pprint(inputdata)
        if not inputdata[0]:
            print("getInputData result is false!")
            print("self.dataBuf.n = ",self.dataBuf.n,"less than 10, wait...")
            return None
        res_b = self.server.policy_infer(inputdata[1])
        # action = [50,50,50,50]
        action = res_a.tolist()+res_a.tolist()
        return action

if __name__=="__main__":
    # simu = SimuPolixir()
    # obs = simu.getSimuObsNp()
    # pprint.pprint(obs)
    # simu.writeSimuAction([1]+[1.0,2.1,3.4,5.3])
    control_switch = True
    controller = SimuControl()
    while True:
        print("*"*80)
        action = controller.infer()
        if action == None:
            time.sleep(1)
            continue
        cmd = [1] if control_switch else [-1]
        cmd = cmd+action
        print("write cmd is:",cmd)
        controller.simu.writeSimuActionByCplusplus([1]+action)
        print("*"*80)
        time.sleep(5)

