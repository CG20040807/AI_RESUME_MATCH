import time
from services.qwen_client import call_qwen
from services.deepseek_client import call_deepseek

MODEL_PRIORITY = ["qwen", "deepseek"]


def safe_call(func, messages, retries=2, sleep_seconds=1):
    last_error = None
    for _ in range(retries):
        try:
            return func(messages)
        except Exception as e:
            last_error = e
            time.sleep(sleep_seconds)
    raise last_error


def call_llm(messages):
    for model in MODEL_PRIORITY:
        try:
            if model == "qwen":
                return safe_call(call_qwen, messages)
            if model == "deepseek":
                return safe_call(call_deepseek, messages)
        except Exception:
            continue

    return "系统繁忙，请稍后再试。"
