import json
import streamlit as st

# ====================== 全局页面配置 ======================
st.set_page_config(page_title="IVE开放日智能咨询聊天机器人", page_icon="🎓", layout="wide")

# ====================== 全套美化CSS（浅蓝渐变背景） ======================
page_bg_css = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
.block-container {
    max-width: 1400px;
    margin: 0 auto;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
/* 全局浅蓝渐变背景 */
.stApp {
    background: linear-gradient(180deg, #ffffff 0%, #d0edfb 100%);
    background-attachment: fixed;
}
.stMainBlockContainer, .stColumn, div[data-testid="stVerticalBlock"] {
    background-color: rgba(255,255,255,0.75);
    border-radius: 12px;
    padding: 12px;
}
.stSidebar {
    background-color: rgba(255,255,255,0.88);
}
h1 {color:#0078d4 !important; font-size:36px !important; font-weight:bold; text-align:center;}
h2 {color:#105cb6 !important; font-size:26px !important;}
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #0078d4, transparent);
}
.stTextInput>div, .stTextArea>div {border-radius:10px !important; border:1px #cce4f6 solid;}
div[data-testid="stAlert"] {border-radius:10px; box-shadow:0 2px 8px #e0edf9;}
img {border-radius:8px; box-shadow:0 1px 6px #d1e3f2; transition:0.3s;}
img:hover {transform:scale(1.02);}
div[data-testid="stImage"]:first-of-type {
    box-shadow: 0 4px 12px #b9d6f2 !important;
}
/* 快捷按钮样式：浅白边框匹配截图 */
.stButton>button {
    background-color: #ffffff !important;
    color:#222222 !important;
    border:1px solid #cccccc !important;
    border-radius: 8px !important;
    padding: 10px 8px;
    box-shadow: none;
    width:100%;
    margin:4px 0;
}
.stButton>button:hover {
    background-color: #f0f7ff !important;
    border-color:#0078d4 !important;
    transform: translateY(-1px);
    transition: 0.2s;
}
.stSidebar h2, .stSidebar h3 {color:#0078d4;}
.stSidebar hr {border-color:#b8d8f0;}
.stSidebar li {
    margin: 8px 0;
    padding: 4px;
    border-radius: 6px;
}
.stSidebar li:hover {
    background-color: #e3f0fc;
}
a:hover {color:#0066cc !important; font-weight:bold;}
.st-radio [data-baseweb="radio"]:has(input:checked) div {background:#d0edfb;}
div[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    padding: 10px !important;
}
.stChatMessage[data-testid="user"] {
    background: #e3f0fc !important;
}
.stChatMessage[data-testid="assistant"] {
    background: #d0e8fb !important;
}
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-thumb {
    background: #a8c8e8;
    border-radius: 4px;
}
::-webkit-scrollbar-track {
    background: #f0f7ff;
}
</style>
'''
st.markdown(page_bg_css, unsafe_allow_html=True)

# ====================== 会话持久存储 ======================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "fill_text" not in st.session_state:
    st.session_state.fill_text = ""
if "message_board" not in st.session_state:
    st.session_state.message_board = []

# ====================== 加载本地知识库 ======================
def load_knowledge():
    with open("ive_trilingual.json", "r", encoding="utf-8") as f:
        return json.load(f)
knowledge = load_knowledge()

# ====================== 三语文字库 ======================
ui_text = {
    "page_title": {
        "zh": "IVE开放日智能咨询聊天机器人",
        "cant": "IVE開放日智能諮詢聊天機械人",
        "en": "IVE Open Day Intelligent Consultation Chatbot"
    },
    "sidebar_header": {
        "zh": "设置面板 | 官方参考链接",
        "cant": "設定面板 | 官方參考連結",
        "en": "Settings | Official Reference Links"
    },
    "lang_label": {
        "zh": "选择使用语言",
        "cant": "選擇使用語言",
        "en": "Select Language"
    },
    "quick_title": {
        "zh": "快捷常用问题（点击直接提问）",
        "cant": "快捷常用問題（點擊直接提問）",
        "en": "Quick Questions (Click to Ask)"
    },
    "bot_intro_title": {
        "zh": "🤖 机器人系统介绍",
        "cant": "🤖 機械人系統介紹",
        "en": "🤖 Bot System Introduction"
    },
    "bot_intro_content": {
        "zh": """你好！欢迎使用IVE开放日咨询机器人😊，你可以咨询沙田IVE的IT课程、学制时长、校区分布、升学路径、实习安排、学生宿舍、奖学金资助等问题，点击下方快捷按钮即可快速提问。
本系统基于VTC官方公开资料开发，覆盖高级文凭HD招生、内地生申请、毕业留港计划全部资讯。""",
        "cant": """你好！歡迎使用IVE開放日諮詢機械人😊，你可以查詢沙田IVE嘅IT課程、學制時長、校區分佈、升學路徑、實習安排、學生宿舍、獎學金資助等問題，點擊下方快捷按鈕即可快速提問。
本系統基於VTC官方公開資料開發，覆蓋高級文憑HD招生、內地生申請、畢業留港計劃全部資訊。""",
        "en": """Hello! Welcome to IVE Open Day consultation bot 😊, you can inquire about Sha Tin IVE IT programmes, study duration, campus info, articulation paths, internships, student hostels and scholarships.
This system is built on official VTC public documents, covering HD admission, mainland student application & post-grad stay scheme."""
    },
    "msg_title": {
        "zh": "📝 用户留言反馈区",
        "cant": "📝 用戶留言反饋區",
        "en": "📝 User Message Board"
    },
    "msg_input": {
        "zh": "输入你的建议、反馈或咨询需求...",
        "cant": "輸入你嘅建議、反饋或諮詢需求...",
        "en": "Enter your suggestions, feedback or enquiries..."
    },
    "msg_empty": {
        "zh": "暂无用户留言，快来留下你的反馈吧！",
        "cant": "暫無用戶留言，快啲留下你嘅反饋啦！",
        "en": "No messages yet, leave your feedback!"
    },
    "gallery_title": {
        "zh": "🏫 IVE 各院校实景一览",
        "cant": "🏫 IVE 各分校實景一覽",
        "en": "🏫 IVE Campus Gallery"
    },
    "input_placeholder": {
        "zh": "请输入你的咨询问题，或点击上方快捷提问按钮",
        "cant": "請輸入你嘅諮詢問題，或點擊上方快捷提問按鈕",
        "en": "Enter your question or click quick buttons above"
    },
    "history_title": {
        "zh": "📌 本次咨询对话记录",
        "cant": "📌 本次諮詢對話記錄",
        "en": "📌 Chat History"
    },
    "empty_history": {
        "zh": "暂无问答记录，输入问题开始咨询",
        "cant": "暫無問答記錄，輸入問題開始諮詢",
        "en": "No chat history yet, type your question to start"
    },
    "footer": {
        "zh": "VTC 职业训练局 · IVE 资讯咨询系统 ©2026",
        "cant": "VTC 職業訓練局 · IVE 資訊諮詢系統 ©2026",
        "en": "VTC Vocational Training Council · IVE Consult System ©2026"
    },
    "lang_tip": {
        "zh": "🇨🇳 简体中文模式",
        "cant": "🇭🇰 粵語模式",
        "en": "🇬🇧 English Mode"
    }
}
# 5个快捷提问（三语）
quick_questions = {
    "zh": ["沙田IVE有什么IT课程", "高级文凭要读几年", "IVE开放日需要预约吗", "读完HD可以升本科吗", "IVE课程有强制实习吗"],
    "cant": ["沙田IVE有咩IT課程", "高級文憑要讀幾年", "IVE開放日需要預約嗎", "讀完HD可以升本科嗎", "IVE課程有強制實習嗎"],
    "en": ["What IT programmes in Sha Tin IVE", "How long is HD programme", "Need reservation for open day", "Can I articulate to university after HD", "Is internship compulsory for IVE courses"]
}
img_captions = {
    "zh": ["IVE 校园正门1","IVE 屯门分校正门","IVE 白色教学大楼","IVE 钟楼校舍","IVE 跨楼连廊校区"],
    "cant": ["IVE 校園正門1","IVE 屯門分校正門","IVE 白色教學大樓","IVE 鐘樓校舍","IVE 跨樓連廊校區"],
    "en": ["IVE Campus Gate 1","IVE Tuen Mun Campus Gate","IVE White Teaching Block","IVE Clock Tower Campus","IVE Connected Corridor Campus"]
}

# ====================== 问答匹配函数 ======================
def match_answer(user_q, lang):
    user_q = user_q.strip()
    default_ans = {
        "zh": "暂时未查询到相关内容，你可以更换关键词重新提问。",
        "cant": "暫時查唔到相關內容，你可以轉關鍵字重新提問。",
        "en": "No relevant information found, please try different keywords."
    }[lang]
    best_ans = default_ans
    max_overlap = 0
    for item in knowledge:
        query_text = item[f"{lang}_q"]
        answer_text = item[f"{lang}_a"]
        overlap_count = len(set(user_q) & set(query_text))
        if overlap_count > max_overlap:
            max_overlap = overlap_count
            best_ans = answer_text
    return best_ans

# ====================== 侧边栏 完整17条官方链接 ======================
with st.sidebar:
    st.header("🎛️ " + ui_text["sidebar_header"]["zh"])
    with st.container():
        st.subheader(ui_text["lang_label"]["zh"])
        lang_choice = st.radio("", ["普通话", "粵語", "English"], label_visibility="collapsed")
    if lang_choice == "普通话":
        lang = "zh"
    elif lang_choice == "粵語":
        lang = "cant"
    else:
        lang = "en"
    st.info(ui_text["lang_tip"][lang])
    st.success("✅ 知识库加载完成")
    st.divider()
    st.subheader(ui_text["sidebar_header"][lang])
    link_data = {
        "zh": [
            ("IVE 分校与高级文凭总览", "https://www.ive.edu.hk/study/tc/programmes/"),
            ("VTC 高级文凭通用介绍", "https://www.vtc.edu.hk/admission/sc/higher-diploma/?tab=s6"),
            ("沙田IVE IT114126 数据AI课程主页", "https://www.vtc.edu.hk/admission/sc/programme/it114126-higher-diploma-in-data-science-and-ai/"),
            ("IT114126 课程大纲英文页", "http://www.vtc.edu.hk/admission/en/programme/it114126-higher-diploma-in-data-science-and-ai/curriculum/"),
            ("HKIIT 课程手册 PDF", "https://hkiit.edu.hk/sites/default/files/2025-12/HKIIT%20booklet2627.pdf.pdf"),
            ("DSE 收生标准公告", "https://www.vtc.edu.hk/home/sc/media-newsroom/press-releases/VTC-Central-Admission-Scheme-Launches-Next-Wednesday-Offering-Diverse-Industry-aligned-Programmes.html"),
            ("本地生 HD 学费页面", "https://www.vtc.edu.hk/admission/sc/tuition-fees-s6/?tab=higher-diploma"),
            ("非本地生学费及奖学金", "https://miao.vtc.edu.hk/sc/nls-admission/fees-and-scholarships"),
            ("非本地生入学要求（高考）", "https://miao.vtc.edu.hk/sc/nls-admission/general-entrance-requirements"),
            ("VTC 宿舍政策总页", "https://halls.vtc.edu.hk/tc/application/accommodation-policy/"),
            ("非本地生住宿说明", "https://miao.vtc.edu.hk/life-at-vtc/accommodation"),
            ("VTC 奖学金介绍", "https://www.vtc.edu.hk/admission/sc/scholarships/"),
            ("HD 衔接本科升学页面", "https://www.vtc.edu.hk/admission/sc/articulation"),
            ("开放日活动公告页", "https://www.vtc.edu.hk/admission/sc/events"),
            ("VPAS 毕业生留港计划主页", "https://vpas.vtc/tc/applicants"),
            ("VPAS 常见问题", "https://vpas.vtc.edu.hk/sc/faq"),
            ("内地及国际生事务主页", "https://miao.vtc.edu.hk/sc")
        ],
        "cant": [
            ("IVE 分校同高級文憑總覽", "https://www.ive.edu.hk/study/tc/programmes/"),
            ("VTC 高級文憑通用介紹", "https://www.vtc.edu.hk/admission/sc/higher-diploma/?tab=s6"),
            ("沙田IVE IT114126 數據AI課程主頁", "https://www.vtc.edu.hk/admission/sc/programme/it114126-higher-diploma-in-data-science-and-ai/"),
            ("IT114126 課程大綱英文頁", "http://www.vtc.edu.hk/admission/en/programme/it114126-higher-diploma-in-data-science-and-ai/curriculum/"),
            ("HKIIT 課程手冊 PDF", "https://hkiit.edu.hk/sites/default/files/2025-12/HKIIT%20booklet2627.pdf.pdf"),
            ("DSE 收生標準公告", "https://www.vtc.edu.hk/home/sc/media-newsroom/press-releases/VTC-Central-Admission-Scheme-Launches-Next-Wednesday-Offering-Diverse-Industry-aligned-Programmes.html"),
            ("本地生 HD 學費頁面", "https://www.vtc.edu.hk/admission/sc/tuition-fees-s6/?tab=higher-diploma"),
            ("非本地生學費及獎學金", "https://miao.vtc.edu.hk/sc/nls-admission/fees-and-scholarships"),
            ("非本地生入學要求（高考）", "https://miao.vtc.edu.hk/sc/nls-admission/general-entrance-requirements"),
            ("VTC 宿舍政策總頁", "https://halls.vtc.edu.hk/tc/application/accommodation-policy/"),
            ("非本地生住宿說明", "https://miao.vtc.edu.hk/life-at-vtc/accommodation"),
            ("VTC 獎學金介紹", "https://www.vtc.edu.hk/admission/sc/scholarships/"),
            ("HD 銜接本科升學頁面", "https://www.vtc.edu.hk/admission/sc/articulation"),
            ("開放日活動公告頁", "https://www.vtc.edu.hk/admission/sc/events"),
            ("VPAS 畢業生留港計劃主頁", "https://vpas.vtc/tc/applicants"),
            ("VPAS 常見問題", "https://vpas.vtc.edu.hk/sc/faq"),
            ("內地及國際生事務主頁", "https://miao.vtc.edu.hk/sc")
        ],
        "en": [
            ("Overview of IVE Campuses & Higher Diplomas", "https://www.ive.edu.hk/study/tc/programmes/"),
            ("General Introduction to VTC Higher Diplomas", "https://www.vtc.edu.hk/admission/sc/higher-diploma/?tab=s6"),
            ("Sha Tin IVE IT114126 Data AI Programme Page", "https://www.vtc.edu.hk/admission/sc/programme/it114126-higher-diploma-in-data-science-and-ai/"),
            ("IT114126 Curriculum Outline (English)", "http://www.vtc.edu.hk/admission/en/programme/it114126-higher-diploma-in-data-science-and-ai/curriculum/"),
            ("HKIIT Programme Handbook PDF", "https://hkiit.edu.hk/sites/default/files/2025-12/HKIIT%20booklet2627.pdf.pdf"),
            ("DSE Admission Standard Announcement", "https://www.vtc.edu.hk/home/sc/media-newsroom/press-releases/VTC-Central-Admission-Scheme-Launches-Next-Wednesday-Offering-Diverse-Industry-aligned-Programmes.html"),
            ("Local Student HD Tuition Fee Page", "https://www.vtc.edu.hk/admission/sc/tuition-fees-s6/?tab=higher-diploma"),
            ("Non-local Student Fees & Scholarships", "https://miao.vtc.edu.hk/sc/nls-admission/fees-and-scholarships"),
            ("Non-local Admission Requirements (Gaokao)", "https://miao.vtc.edu.hk/sc/nls-admission/general-entrance-requirements"),
            ("VTC Hall Accommodation Policy", "https://halls.vtc.edu.hk/tc/application/accommodation-policy/"),
            ("Accommodation Guide for Non-local Students", "https://miao.vtc.edu.hk/life-at-vtc/accommodation"),
            ("VTC Scholarship Information", "https://www.vtc.edu.hk/admission/sc/scholarships/"),
            ("HD Articulation to Undergraduate Degrees", "https://www.vtc.edu.hk/admission/sc/articulation"),
            ("Info Day Event Announcement Page", "https://www.vtc.edu.hk/admission/sc/events"),
            ("VPAS Graduate Stay Scheme Homepage", "https://vpas.vtc/tc/applicants"),
            ("VPAS Frequently Asked Questions", "https://vpas.vtc.edu.hk/sc/faq"),
            ("Mainland & International Student Affairs", "https://miao.vtc.edu.hk/sc")
        ]
    }
    for name, url in link_data[lang]:
        st.markdown(f"- [{name}]({url})")

# ====================== 主页面内容（无左侧快捷栏） ======================
# 1. 页面居中大标题
st.markdown(f"<h1>🎓 {ui_text['page_title'][lang]}</h1>", unsafe_allow_html=True)
st.divider()

# 2. 机器人系统介绍（单独整块，无并排）
st.subheader(ui_text["bot_intro_title"][lang])
st.info(ui_text["bot_intro_content"][lang])
st.divider()

# 3. 快捷常用问题 横向均分5列平铺（你截图样式）
st.subheader(ui_text["quick_title"][lang])
q_list = quick_questions[lang]
# 5等分横向分栏
col_q1, col_q2, col_q3, col_q4, col_q5 = st.columns(5)
with col_q1:
    if st.button(q_list[0]):
        st.session_state.fill_text = q_list[0]
with col_q2:
    if st.button(q_list[1]):
        st.session_state.fill_text = q_list[1]
with col_q3:
    if st.button(q_list[2]):
        st.session_state.fill_text = q_list[2]
with col_q4:
    if st.button(q_list[3]):
        st.session_state.fill_text = q_list[3]
with col_q5:
    if st.button(q_list[4]):
        st.session_state.fill_text = q_list[4]
st.divider()

# 4. 咨询输入框
user_input = st.text_input(
    "",
    value=st.session_state.fill_text,
    placeholder=ui_text["input_placeholder"][lang]
)
st.session_state.fill_text = ""

# 5. 对话气泡渲染
if user_input.strip():
    reply = match_answer(user_input, lang)
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    with st.chat_message("assistant", avatar="🎓"):
        st.write(reply)
    st.session_state.chat_history.append((user_input, reply))
    st.divider()

# 6. 留言反馈区（垂直按钮无分栏，无报错）
st.subheader(ui_text["msg_title"][lang])
msg_text = st.text_area("", placeholder=ui_text["msg_input"][lang], height=100)
# 独立按钮文字，规避字典取值报错
submit_label = "提交留言"
clear_label = "清空全部留言"
if lang == "en":
    submit_label = "Submit Message"
    clear_label = "Clear All Messages"
btn_submit = st.button(submit_label)
btn_clear = st.button(clear_label)
if btn_submit:
    if msg_text.strip():
        st.session_state.message_board.append(msg_text.strip())
        st.success("留言提交成功！" if lang == "zh" else "Message submitted successfully!")
if btn_clear:
    st.session_state.message_board = []
    st.warning("已清空所有留言" if lang == "zh" else "All messages cleared!")
st.divider()
# 展示留言列表
if len(st.session_state.message_board) == 0:
    st.info(ui_text["msg_empty"][lang])
else:
    for idx, msg in enumerate(st.session_state.message_board, 1):
        if lang == "zh":
            st.write(f"📝 留言{idx}：{msg}")
        else:
            st.write(f"📝 Message {idx}: {msg}")
        st.divider()

# 7. IVE校园图库（本地img文件夹图片）
st.subheader(ui_text["gallery_title"][lang])
try:
    campus_imgs = [
        "img/campus1.jpg",
        "img/campus2.jpg",
        "img/campus3.jpg",
        "img/campus4.jpg",
        "img/campus5.jpg"
    ]
    col_g1, col_g2 = st.columns(2)
    cap = img_captions[lang]
    with col_g1:
        st.image(campus_imgs[0], width=580, caption=cap[0])
        st.image(campus_imgs[1], width=580, caption=cap[1])
        st.image(campus_imgs[2], width=580, caption=cap[2])
    with col_g2:
        st.image(campus_imgs[3], width=580, caption=cap[3])
        st.image(campus_imgs[4], width=580, caption=cap[4])
except:
    st.warning("校园图片缺失，请检查img文件夹内campus1~5.jpg文件")
st.divider()

# 8. 历史对话记录
st.subheader("📌 " + ui_text["history_title"][lang])
history_data = st.session_state.chat_history
if len(history_data) == 0:
    st.info(ui_text["empty_history"][lang])
else:
    for q,a in history_data:
        if lang == "zh":
            st.write(f"👤 用户：{q}")
            st.write(f"🤖 IVE咨询：{a}")
        else:
            st.write(f"👤 User: {q}")
            st.write(f"🤖 IVE Bot: {a}")
        st.divider()

# 底部版权文本
st.divider()
st.caption(ui_text["footer"][lang])

# 启动弹窗（无不存在的welcome_msg键，彻底消除KeyError）
st.toast("🎓 IVE Open Day Chatbot Ready", icon="🎓")