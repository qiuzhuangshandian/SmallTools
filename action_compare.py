import pandas as pd
import pickle
from revive.computation.inference import VirtualEnv
from revive.computation.inference import PolicyModel
import onnxruntime
import yaml
import numpy as np
import matplotlib.pyplot as plt
import os
import torch

def get_yaml_cfg(file_path):
    fr = open(file_path, mode='r', encoding='utf-8')
    yamlCfg = yaml.load(fr,Loader=yaml.FullLoader)
    fr.close()
    return yamlCfg

class GraphParse:
    def __init__(self, cfg:dict) -> None:
        self.cfg = cfg
        self.act_title = self.cfg["act_node"]
        self.graph_cfg = self.get_graph_cfg()["metadata"]

    def get_graph_cfg(self):
        graph_file_path = self.cfg["graph_yaml_path"]
        return get_yaml_cfg(graph_file_path)

    def get_in_nodes_by_out_node(self,node_name:str):
        if node_name not in list(self.graph_cfg["graph"].keys()):
            print(f"{node_name} is not a output node")
            return None
        return self.graph_cfg["graph"][node_name]

    def get_all_output_nodes(self):
        return list(self.graph_cfg["graph"].keys())

    def get_total_used_dims(self):
        total_used_nodes = []
        for out_node in self.graph_cfg["graph"]:
            total_used_nodes.append(out_node)
            total_used_nodes += self.graph_cfg["graph"][out_node]
        total_used_nodes = list(set(total_used_nodes))
        return total_used_nodes

    def get_feature_titles_by_node_name(self,node_name):
        columns_cfg = self.graph_cfg["columns"]
        feature_titles = []
        for column in columns_cfg:
            key = list(column.keys())[0]
            if column[key]["dim"] == node_name:
                feature_titles.append(key)
        if len(feature_titles) == 0:
            return None
        return feature_titles

    def get_act_titles(self):
        return self.get_feature_titles_by_node_name(self.act_title)

    def get_tmp_var_key_titles(self):
        output_nodes = list(self.graph_cfg["graph"].keys())
        total_input_nodes = []
        for out_node in output_nodes:
            total_input_nodes += self.graph_cfg["graph"][out_node]
        total_input_nodes = set(total_input_nodes)
        output_nodes = set(output_nodes)
        tmp_var_nodes = output_nodes & total_input_nodes
        result = {}
        for node_name in tmp_var_nodes:
            groups = node_name.split("_")
            if len(groups) > 1 and groups[0] == "next":
                continue
            result[node_name] = self.get_feature_titles_by_node_name(node_name)
        return result

    def get_obs_key_titles(self):
        output_nodes = list(self.graph_cfg["graph"].keys())
        total_input_nodes = []
        for out_node in output_nodes:
            total_input_nodes += self.graph_cfg["graph"][out_node]
        total_input_nodes = set(total_input_nodes)
        result = {}
        for output_node in output_nodes:
            groups = output_node.split("_")
            if len(groups) <= 1:
                continue
            if groups[0] != "next":
                continue
            tmp_obs_node = "_".join(groups[1:])
            if tmp_obs_node in total_input_nodes:
                result[tmp_obs_node] = self.get_feature_titles_by_node_name(tmp_obs_node)
        return result

    def get_static_var_key_titles(self):
        output_titles = list(self.graph_cfg["graph"].keys())

        def isNextStepObs(x):
            groups = x.split("_")
            if len(groups) >= 2 and groups[0] == "next":
                return True
            return False

        result = {}
        for out_node in output_titles:
            input_nodes = self.graph_cfg["graph"][out_node]
            for input_node in input_nodes:
                if input_node in output_titles:
                    continue
                if "next_"+input_node in output_titles:
                    continue
                if isNextStepObs(input_node):
                    continue
                features = self.get_feature_titles_by_node_name(input_node)
                if features is None:
                    continue
                result[input_node] = features
        return result

    def isActTitle(self,nodeName:str):
        if nodeName == self.act_title:
            return True
        return False

    def get_all_init_key_titles(self):
        output_titles = list(self.graph_cfg["graph"].keys())
        print("output_titles:",output_titles)

        def isNextStepObs(x):
            groups = x.split("_")
            if len(groups) >= 2 and groups[0] == "next":
                return True
            return False

        result = {}
        for title in output_titles:
            input_titles = self.graph_cfg["graph"][title]
            for input_title in input_titles:
                if isNextStepObs(input_title):
                    continue
                if input_title in output_titles:
                    continue
                features = self.get_feature_titles_by_node_name(input_title)
                if features is None:
                    continue
                result[input_title] = features
        return result

class ActionCompare:
    def __init__(self,cfg:dict) -> None:
        self.cfg = cfg
        self.venv = None
        self.policy = None
        self.data = None
        self.graphParser = GraphParse(self.cfg)
        self.initEnv()
        self.initPolicy()
        self.init_data()
        self.input_x = {}
        self.policy_input_x = {}
        self.obs={}
        self.collection = {}

    def init_data(self):
        self.data = pd.read_csv(self.cfg["expert_data_csv"]).iloc[self.cfg["start_pos"]:self.cfg["start_pos"]+self.cfg["length"],:]

    def initEnv(self):
        fr = open(self.cfg["env_path"],"rb")
        self.venv = pickle.load(fr)
        fr.close()
        self.env_list = self.venv.env_list

    def initPolicy(self):
        device = torch.device("cpu")
        if self.cfg["model_type"] == "pkl":
            fr = open(self.cfg["policy_path"],"rb")
            self.policy = pickle.load(fr)
            fr.close()
            self.policy._policy_model.node.to(torch.device("cpu"))
            
        if self.cfg["model_type"] == "onnx":
            self.policy = onnxruntime.InferenceSession(self.cfg["policy_path"])

        if self.cfg["model_type"] == "pt":
            self.policy = torch.load(self.cfg["policy_path"], map_location=device)
            self.policy = PolicyModel(self.policy)

    def envStep(self, input_x):
        res = self.venv.infer_one_step(input_x, deterministic=True)
        return res

    def doAction(self,input_feed,output_names:list):
        if self.cfg["model_type"] == "pkl" or self.cfg["model_type"] == "pt":
            for k in input_feed:
                input_feed[k] = np.expand_dims(input_feed[k],axis=0)
            res = self.policy.infer(input_feed)
        else:
            input_feed = {k:v.astype(np.float32) for k,v in input_feed.items()}
            res = self.policy.run(input_feed=input_feed,output_names=output_names)
        return res[0]

    def build_input_x(self):
        pass

    def init_policy_input_x(self):
        policy_input_nodes = self.graphParser.get_in_nodes_by_out_node(self.cfg["act_node"])
        for node in policy_input_nodes:
            titles = self.graphParser.get_feature_titles_by_node_name(node)
            self.policy_input_x[node] = self.data[titles].values[0]

    def init_collection(self):
        # checkList = self.cfg["check_nodes"]
        checkList = self.graphParser.get_all_output_nodes()
        print(checkList)
        self.collection = {}
        for item in checkList:
            if self.graphParser.get_feature_titles_by_node_name(item) is None:
                assert "next_" in item
                item  = item[5:]
            titles = self.graphParser.get_feature_titles_by_node_name(item)
            self.collection[item] = {}
            for title in titles:
                self.collection[item][title] = []

    def updateCollection(self):
        # checkList = self.cfg["check_nodes"]
        # checkList = self.graphParser.get_all_output_nodes()
        checkList = self.collection.keys()
        for item in checkList:
            titles = self.graphParser.get_feature_titles_by_node_name(item)
            for idx, title in enumerate(titles):
                self.collection[item][title].append(self.step_res[item][idx].tolist())

    def update_policy_input_x(self,idx:int):
        obs_key_titles = self.graphParser.get_obs_key_titles()
        obs_nodes = list(obs_key_titles.keys())
        policy_input_nodes = self.graphParser.get_in_nodes_by_out_node(self.cfg["act_node"])
        for policy_input_node in policy_input_nodes:
            if self.cfg["replay"]:
                tmp_titles = self.graphParser.get_feature_titles_by_node_name(policy_input_node)
                self.policy_input_x[policy_input_node] = self.data[tmp_titles].values[idx]
                continue
            if policy_input_node in obs_nodes:
                self.policy_input_x[policy_input_node] = self.step_res["next_"+policy_input_node]
            tmp_titles = self.graphParser.get_feature_titles_by_node_name(policy_input_node)
            self.policy_input_x[policy_input_node] = self.data[tmp_titles].values[idx]

    def updateInputX(self, idx:int):
        obs_key_titles = self.graphParser.get_obs_key_titles()
        for obs_node in list(obs_key_titles.keys()):
            if self.cfg["replay"]:
                tmp_titles = self.graphParser.get_feature_titles_by_node_name(obs_node)
                self.input_x[obs_node] = self.data[tmp_titles].values[idx]
            else:
                self.input_x[obs_node] = self.step_res["next_"+obs_node]
        static_node_titles = self.graphParser.get_static_var_key_titles()
        static_nodes = list(static_node_titles.keys())
        for node in static_nodes:
            titles = self.graphParser.get_feature_titles_by_node_name(node)
            self.input_x[node] = self.data[titles].values[idx]

    def addActToInputX(self,act):
        self.input_x[self.cfg["act_node"]] = act

    def initInputX(self):
        obs_nodes_titles = self.graphParser.get_obs_key_titles()
        obs_nodes = list(obs_nodes_titles.keys())
        for obs_node in obs_nodes:
            titles = self.graphParser.get_feature_titles_by_node_name(obs_node)
            self.input_x[obs_node] = self.data[titles].values[0]
        static_node_titles = self.graphParser.get_static_var_key_titles()
        static_nodes = list(static_node_titles.keys())
        for node in static_nodes:
            titles = self.graphParser.get_feature_titles_by_node_name(node)
            self.input_x[node] = self.data[titles].values[0]

    def do_juto(self,feature, v_list,v2_list):
        if 1:
            return v_list
        import random
        from scipy.signal import savgol_filter
        g_values = []
        max_v,min_v = max(v2_list),min(v2_list)
        for i in range(len(v_list)):
            e = v2_list[i] - v_list[i]
            tmp_v = v_list[i]
            if abs(e) > (max_v - min_v) * 0.9:
                tmp_v = v_list[i]+random.uniform(0.5,0.6)*e
            g_values.append(tmp_v)
            # if abs(e) > (max_v - min_v) * 0.7 and feature == "valid_wind_speed_mean":
            #     tmp_v = v_list[i]+0.8*e
            # g_values.append(tmp_v)
        # if feature=="valid_wind_speed_mean":
        g_values = savgol_filter(g_values,5,2)
        return g_values

    def plot_result(self):
        if not os.path.exists(self.cfg["fig_save_path"]):
            os.makedirs(self.cfg["fig_save_path"])
        print("begin plot")
        for node,content in self.collection.items():
            for feature,values in content.items():
                raw_data = self.data[[feature]][0:self.cfg["length"]].values
                plt.plot(raw_data,c="g",label="raw")
                plt.plot(values,c="firebrick",label="policy")
                plt.title(node+"_"+feature)
                plt.legend()
                plt.savefig(os.path.join(self.cfg["fig_save_path"],node+"_"+feature+".png"))
                plt.close()

    # def show_compare_res(self):
    #     target_t = self.data[["target_t"]].values
    #     raw_data_diff_mean = np.abs((self.data[["t_next"]][0:self.cfg["length"]].values- target_t)).mean()
    #     policy_data_diff_mean = np.abs((np.array(self.collection["t_next"]["t_next"])-target_t)).mean()
    #     print("raw t mean:",raw_data_diff_mean, "policy t mean:",policy_data_diff_mean)
    #     print("improve rate:{}%".format(100*(raw_data_diff_mean - policy_data_diff_mean)/raw_data_diff_mean))


    def runCompare(self):
        self.init_collection()
        self.init_policy_input_x()
        self.initInputX()
        for idx in range(self.cfg["length"]-1):
            act = self.doAction(self.policy_input_x, output_names=[self.cfg["act_node"]])
            self.addActToInputX(act)
            self.step_res = self.envStep(self.input_x)
            self.updateCollection()
            self.update_policy_input_x(idx+1)
            self.updateInputX(idx+1)
        self.plot_result()
        # self.show_compare_res()

if __name__=="__main__":
    cfg = {
        "policy_path"    : "./models/policy.pt",
        "env_path"       : "./models/env.pkl",
        "expert_data_csv": "./revive_data/1214/revive_data.csv",
        "graph_yaml_path": "./models/graph_2.yaml",
        "fig_save_path"  : "./compare_figure4/",
        "act_node"       : "action",
        "model_type"     : "pt",
        "check_nodes"    : ["action","nacelle_pos_mod360","pitch","generator_speed","torque","wind_speed","wind_dir","air_temp"],
        "start_pos"      : 100000,
        "length"         : 1000,
        "replay"         : True
    }
    obj = ActionCompare(cfg)
    obj.runCompare()

    # 4500