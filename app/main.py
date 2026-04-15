import streamlit as st
from utils.file_parser import parse_docx
from utils.text_cleaner import clean_text
from core.analyzer import analyze
from core.scorer import extract_score
from core.ranker import rank
from core.summarizer import summarize
from utils.docx_exporter import export
import re

st.set_page_config(page_title="AI Talent Assessment System", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7fbff 0%, #ffffff 28%, #f8fbf8 100%);
        color: #1f2937;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #153b63;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #4b5563;
        margin-top: 0;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid rgba(148,163,184,0.20);
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(15,23,42,0.05);
        height: 100%;
    }
    button[kind="primary"] {
        border-radius: 14px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #2563eb, #0f766e) !important;
        border: none !important;
    }
    div[data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #9cc3de;
        background: #f9fdff;
        border-radius: 16px;
    }
    .small-note {
        color: #6b7280;
        font-size: 0.88rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">AI Talent Assessment System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">批量上传 Word 简历，粘贴岗位标准，自动匹配岗位 JD，输出多维评分、排名、总结，并可一键下载 Word 报告。</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("### 参数设置")
    st.text_input(
        "API Base URL",
        value="https://dashscope.aliyuncs.com/compatible-mode/v1",
        disabled=True
    )
    st.caption("千问模型接口使用阿里云兼容地址")
    st.markdown("---")
    st.markdown("上传格式仅支持 .docx")
    st.markdown("建议同一批简历对应同一个岗位")

col1, col2 = st.columns([1.15, 0.85], gap="large")

with col1:
    st.markdown("### 1）输入岗位信息")
    job_title = st.text_input("岗位名称", placeholder="例如：HRBP实习生 / AI产品经理 / 数据分析实习生")
    jd = st.text_area("岗位JD", height=180, placeholder="请输入岗位职责、要求、加分项等")
    criteria = st.text_area(
        "岗位评估标准",
        height=180,
        placeholder=(
            "例如：\n"
            "1. 技能维度：Python、数据处理、Prompt设计\n"
            "2. 经验维度：有实习或项目落地经历\n"
            "3. 软技能：沟通表达清晰，主动性强\n"
            "4. 风险项：没有项目经历、无法独立完成任务的优先级降低"
        )
    )

with col2:
    st.markdown("### 2）上传 Word 简历")
    uploaded_files = st.file_uploader(
        "请上传候选人 Word 简历（仅支持 .docx，可多选）",
        type=["docx"],
        accept_multiple_files=True
    )
    st.markdown(
        "<div class='small-note'>支持格式：.docx；不建议上传 pdf / 图片 / 压缩包。</div>",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

analyze_clicked = st.button("开始批量评估", type="primary")

if "results" not in st.session_state:
    st.session_state.results = []
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "word_bytes" not in st.session_state:
    st.session_state.word_bytes = None

if analyze_clicked:
    if not job_title.strip():
        st.warning("请先输入岗位名称。")
        st.stop()
    if not jd.strip():
        st.warning("请先输入岗位JD。")
        st.stop()
    if not uploaded_files:
        st.warning("请至少上传一份 Word 简历。")
        st.stop()

    with st.spinner("AI正在分析中，请稍候..."):
        results = []

        for file in uploaded_files:
            resume_text = clean_text(parse_docx(file))
            analysis = analyze(job_title, jd, criteria, resume_text)
            score = extract_score(analysis)

            recommendation = "未提取"
            m = re.search(r"推荐建议[:：]\s*(.+)", analysis)
            if m:
                recommendation = m.group(1).strip().split("\n")[0]

            results.append({
                "name": file.name,
                "analysis": analysis,
                "score": score,
                "recommendation": recommendation
            })

        ranked = rank(results)
        summary = summarize(job_title, jd, criteria, ranked)
        word_file = export(ranked, summary, job_title, jd, criteria)

        st.session_state.results = ranked
        st.session_state.summary = summary
        st.session_state.word_bytes = word_file

    st.success("分析完成，请先查看页面结果，再决定是否下载 Word 报告。")

if st.session_state.results:
    ranked = st.session_state.results
    summary = st.session_state.summary

    st.markdown("## 3）结果总览")

    top = ranked[0]
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="small-note">推荐候选人</div>
                <div style="font-size:1.25rem;font-weight:800;color:#153b63;">{top['name']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="small-note">最高总分</div>
                <div style="font-size:1.8rem;font-weight:900;color:#0f766e;">{top['score']}/100</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="small-note">推荐建议</div>
                <div style="font-size:1.25rem;font-weight:800;color:#b45309;">{top.get('recommendation','未提取')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 3.1 候选人排名")
    for idx, r in enumerate(ranked, start=1):
        with st.container(border=True):
            left, right = st.columns([0.78, 0.22])
            with left:
                st.markdown(f"#### {idx}. {r['name']}")
                st.caption(f"总分：{r['score']}/100 · 推荐建议：{r.get('recommendation', '未提取')}")
            with right:
                st.metric("总分", f"{r['score']}")

            st.markdown("**评估正文**")
            st.markdown(r["analysis"])

    st.markdown("### 3.2 全局总结")
    st.markdown(summary)

    st.markdown("### 3.3 下载结果")
    if st.session_state.word_bytes:
        st.download_button(
            label="下载 Word 报告",
            data=st.session_state.word_bytes,
            file_name="AI_Talent_Assessment_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
else:
    st.info("请先填写岗位名称、JD、评估标准，并上传多份 Word 简历，然后点击“开始批量评估”。")
