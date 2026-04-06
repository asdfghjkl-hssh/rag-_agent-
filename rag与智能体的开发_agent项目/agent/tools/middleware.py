from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model
from langchain_community.callbacks.uptrain_callback import handler
from langgraph.runtime import Runtime
from langgraph.types import Command
from langchain.tools.tool_node import ToolCallRequest

from utils.logger_handler import logger


@wrap_tool_call
def monitor_tool(request,handler):# 工具执行的监控
    logger.info(f"[工具执行]工具名称：{request.tool_call['name']}")
    logger.info(f"[工具执行]工具参数：{request.tool_call['args']}")
    try:
        result=handler(request)
        logger.info(f"[工具执行]成功，结果：{result}")
        return result
    except Exception as e:
        logger.error(f"[工具执行]工具执行失败：{e}")
        raise e
@before_model
def log_before_model(state,runtime):  # 在模型执行前输出日志
    logger.info(f"[模型执行]模型名称：{len(state['messages'])}条消息")
    return None
# def report_prompt_switch():  # 动态切换提示词
#     pass