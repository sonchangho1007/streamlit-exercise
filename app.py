# app.py -- 우리 반 성적 분석 대시보드 (화면)
import streamlit as st
import json
import os
from utils import (total_score, average_score, to_grade, grade_to_gpa,
                   subject_average, subject_top, grade_distribution,
                   rank_list, pass_rate)

st.set_page_config(page_title="성적 분석 대시보드", layout="wide")

DB_FILE = "students.json"

def load_students():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [
        {"이름": "김민준", "국어": 92,  "영어": 85, "수학": 78},
        {"이름": "이서연", "국어": 88,  "영어": 90, "수학": 95},
        {"이름": "박도윤", "국어": 60,  "영어": 55, "수학": 72},
        {"이름": "최지우", "국어": 100, "영어": 80, "수학": 90},
        {"이름": "정하준", "국어": 45,  "영어": 60, "수학": 58},
    ]

def save_students(students_list):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(students_list, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"데이터 저장 실패: {e}")

# 처음 실행 시 샘플 학생 데이터를 세션에 넣어 둔다. (다시 실행돼도 유지)
if "students" not in st.session_state:
    st.session_state.students = load_students()

students = st.session_state.students

# 상단 배너 이미지 (banner.png 파일을 함께 둘 것)
st.image("banner.png", width="stretch")
st.title("우리 반 성적 분석 대시보드")

# --- 상단 요약 지표 ---
col1, col2, col3 = st.columns(3)
col1.metric("응시 인원", f"{len(students)}명")

if students:
    avgs = [average_score(stu) for stu in students]
    overall = sum(avgs) / len(avgs)
else:
    overall = 0.0

col2.metric("전체 평균", f"{overall:.2f}")
col3.metric("합격률", f"{pass_rate(students):.1f}%")

SUBJECTS = ["국어", "영어", "수학"]

tab1, tab2, tab3, tab4 = st.tabs(["학생입력", "학생별 성적지표", "과목별 통계", "석차,학점분포"])

# --- Tab 1 : 학생 추가 ---
with tab1:
    st.header("학생 추가")
    name = st.text_input("이름")
    kor = st.number_input("국어", 0, 100, 0)
    eng = st.number_input("영어", 0, 100, 0)
    mat = st.number_input("수학", 0, 100, 0)
    if st.button("추가"):
        if name.strip():
            new_stu = {"이름": name.strip(), "국어": kor, "영어": eng, "수학": mat}
            st.session_state.students.append(new_stu)
            save_students(st.session_state.students)
            st.success(f"{name} 학생을 추가했습니다.")
            st.rerun()
        else:
            st.error("이름을 입력해주세요.")

# --- Tab 2 : 학생별 성적표 ---
with tab2:
    st.header("학생별 성적표")
    if students:
        table = []
        for stu in students:
            avg = average_score(stu)
            grade = to_grade(avg)
            table.append({
                "이름": stu["이름"],
                "국어": stu["국어"], "영어": stu["영어"], "수학": stu["수학"],
                "총점": total_score(stu),
                "평균": round(avg, 2),
                "학점": grade,
                "평점": grade_to_gpa(grade),
            })
        st.table(table)
    else:
        st.write("등록된 학생이 없습니다.")

# --- Tab 3 : 과목별 통계 ---
with tab3:
    st.header("과목별 통계")
    if students:
        cols = st.columns(3)
        for i in range(len(SUBJECTS)):
            subject = SUBJECTS[i]
            with cols[i]:
                st.subheader(subject)
                st.write(f"평균: {subject_average(students, subject):.2f}")
                st.write(f"최고: {subject_top(students, subject)}")

        chart_data = []
        for subject in SUBJECTS:
            chart_data.append({"과목": subject, "평균": subject_average(students, subject)})
        st.bar_chart(chart_data, x="과목", y="평균", horizontal=True, height=400)
    else:
        st.write("등록된 학생이 없습니다.")

# --- Tab 4 : 석차 & 학점 분포 ---
with tab4:
    st.header("석차")
    if students:
        ranked = rank_list(students)
        rank_table = []
        rank = 1
        for stu in ranked:
            rank_table.append({"석차": rank, "이름": stu["이름"], "총점": total_score(stu)})
            rank = rank + 1
        st.table(rank_table)
    else:
        st.write("등록된 학생이 없습니다.")

    st.header("학점 분포")
    if students:
        dist = grade_distribution(students)
        dist_data = [{"학점": g, "인원": dist[g]} for g in ["A", "B", "C", "D", "F"]]
        st.bar_chart(dist_data, x="학점", y="인원", horizontal=True, height=400)
    else:
        st.write("등록된 학생이 없습니다.")

