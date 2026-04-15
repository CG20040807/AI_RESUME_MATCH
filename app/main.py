import streamlit as st
from utils.file_parser import parse_docx
from utils.text_cleaner import clean_text
from core.analyzer import analyze
from core.scorer import extract_score
from core.ranker import rank
from core.summarizer import summarize
from utils.docx_exporter import export

st.title("AI招聘系统（多模型容灾版）")

job_title = st.text_input("岗位")
jd = st.text_area("JD")
criteria = st.text_area("评估标准")
files = st.file_uploader("上传简历", type=["docx"], accept_multiple_files=True)

if st.button("开始分析"):
    results = []

    for file in files:
        text = clean_text(parse_docx(file))
        analysis = analyze(job_title, jd, criteria, text)
        score = extract_score(analysis)

        results.append({
            "name": file.name,
            "analysis": analysis,
            "score": score
        })

    ranked = rank(results)
    summary = summarize(job_title, jd, criteria, ranked)

    for r in ranked:
        st.write(r["name"], r["score"])
        st.markdown(r["analysis"])

    st.markdown("### 总结")
    st.write(summary)

    file = export(ranked, summary)
    st.download_button("下载报告", file, "report.docx")