from services.model_router import call_llm


def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def summarize(job_title, jd, criteria, results):
    prompt_template = load_prompt("prompts/summary_prompt.txt")

    candidate_lines = []
    for r in results:
        candidate_lines.append(f"{r['name']}：{r['score']}分，{r.get('recommendation', '未提取')}")

    user_prompt = f"""
岗位名称：
{job_title}

岗位JD：
{jd}

岗位评估标准：
{criteria}

候选人列表：
{chr(10).join(candidate_lines)}

请基于这些候选人结果，输出总结报告。
"""

    messages = [
        {
            "role": "system",
            "content": prompt_template
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    return call_llm(messages)
