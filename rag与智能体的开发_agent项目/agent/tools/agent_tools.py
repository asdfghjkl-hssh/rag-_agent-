import os
import random

from rag.rag_service import RagSummarizeService
from langchain_core.tools import tool
from utils.config_handler import agent_config
from utils.logger_handler import logger
from utils.path_tool import get_file_path
rag_service=RagSummarizeService()

user_id=["003","004","005","006","007","008","009","010"]
#月份列表
month_list=["1月","2月","3月","4月","5月","6月","7月","8月",
            "9月","10月","11月","12月"]
#定义一个空字典
external_data={}
@tool(description="RAG服务，用于总结内容")
def rag_summarize(query: str) -> str:
    return rag_service.rag_summarize(query)
@tool(description="天气预报服务")
def get_weather(city: str) -> str:
    return f"{city},天气晴天"
#获取城市服务
@tool(description="获取所在的城市")
def get_city() -> str:
    #使用random
    return "驻马店市"

#获取用户的id，以字符串返回
@tool(description="获取用户的id，以字符串返回")
def get_user_id() -> str:
    return random.choice(user_id)
#获取月份
@tool(description="获取日期")
def get_month() -> str:
    return "今天是2026年3月30号"
def generate_external_record():
    if not external_data:
        external_data_path=get_file_path(agent_config["external-data-data"])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"[外部数据]文件{external_data_path}不存在")
        with open(external_data_path,"r",encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr=line.strip().split(",")
                user_ids = arr[0].replace('"', "")
                # 户型 (索引1)
                house_type = arr[1].replace('"', "")
                # 用户标签 (索引2)
                user_tag = arr[2].replace('"', "")
                # 地面类型 (索引3)
                floor_type = arr[3].replace('"', "")
                # 使用数据 (索引4)
                usage_data = arr[4].replace('"', "").replace('\\n', '\n')  # 还原换行符
                # 耗材状态 (索引5)
                consumable_status = arr[5].replace('"', "").replace('\\n', '\n')
                # 备注 (索引6)
                remark = arr[6].replace('"', "")
                # 记录日期 (索引7)
                record_date = arr[7].replace('"', "")
                if user_ids not in external_data:
                    external_data[user_ids] = {}
                external_data[user_ids][record_date]={
                    "house_type": house_type,
                    "user_tag": user_tag,
                    "floor_type": floor_type,
                    "usage_data": usage_data,
                    "consumable_status": consumable_status,
                    "remark": remark,
                }

#从外部记录中获取用户记录中的时间
@tool(description="从外部记录中获取用户记录中的时间")
def get_user_time(user_ids: str, record_date: str) -> str:
    generate_external_record()
    try:
        return external_data[user_ids][record_date]
    except KeyError:
        logger.warning(f"[外部数据]用户{user_ids}在{record_date}月份没有记录")
        return ""

