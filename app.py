import streamlit as st
import json
import random

# إعداد الصفحة
st.set_page_config(
    page_title="تدريب مقابلة - وظيفة قانوني",
    page_icon="⚖️",
    layout="wide"
)

# تحميل البيانات
@st.cache_data
def load_data():
    try:
        with open("data/questions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("ملف البيانات غير موجود. تأكد من وجود data/questions.json")
        return []
    except json.JSONDecodeError:
        st.error("ملف البيانات غير صالح. تأكد من صحة تنسيق JSON")
        return []

# تحميل الأسئلة
data = load_data()

if not data:
    st.warning("لا توجد بيانات. يرجى إضافة الأسئلة إلى ملف data/questions.json")
    st.stop()

# استخراج الفئات
categories = [item["category"] for item in data]

# ------------------- الشريط الجانبي -------------------
st.sidebar.title("⚖️ تدريب المقابلة")
st.sidebar.markdown("**وظيفة قانوني - هيئة الخدمة والإدارة العامة**")
st.sidebar.markdown("---")

# اختيار الفئة
selected_category = st.sidebar.selectbox(
    "اختر المحور:",
    ["جميع الأسئلة"] + categories
)

# وضع التدريب (إخفاء الإجابة)
training_mode = st.sidebar.checkbox("وضع التدريب (إخفاء الإجابات)", value=True)

# وضع عشوائي
random_mode = st.sidebar.checkbox("عرض سؤال عشوائي", value=False)

# البحث
search_query = st.sidebar.text_input("بحث عن سؤال:")

# عداد الأسئلة
st.sidebar.markdown("---")
st.sidebar.caption("💡 نصيحة: استخدمي وضع التدريب لإخفاء الإجابات واختبار نفسك.")

# ملاحظات شخصية
st.sidebar.markdown("---")
st.sidebar.subheader("📝 ملاحظاتي")
notes = st.sidebar.text_area("اكتبي ملاحظاتك هنا:")
if st.sidebar.button("حفظ الملاحظات"):
    st.sidebar.success("تم حفظ الملاحظات مؤقتًا (ستفقد عند إغلاق الجلسة).")

# ------------------- الصفحة الرئيسية -------------------
st.title("📚 التدرب على أسئلة مقابلة وظيفة قانوني")
st.markdown("---")

# تصفية البيانات حسب الفئة المختارة
if selected_category == "جميع الأسئلة":
    filtered_data = data
else:
    filtered_data = [item for item in data if item["category"] == selected_category]

# تطبيق البحث
if search_query:
    temp_data = []
    for cat in filtered_data:
        filtered_questions = [
            q for q in cat["questions"]
            if search_query.lower() in q["question"].lower()
        ]
        if filtered_questions:
            temp_data.append({"category": cat["category"], "questions": filtered_questions})
    filtered_data = temp_data

# إذا تم تفعيل الوضع العشوائي
if random_mode and filtered_data:
    all_questions = []
    for cat in filtered_data:
        for q in cat["questions"]:
            all_questions.append((cat["category"], q))
    if all_questions:
        random_category, random_q = random.choice(all_questions)
        st.subheader(f"🎲 سؤال عشوائي من محور: {random_category}")
        st.markdown(f"**{random_q['question']}**")
        if training_mode:
            if st.button("إظهار الإجابة", key="random_answer"):
                st.success(random_q["answer"])
        else:
            st.write(random_q["answer"])
        st.stop()

# عرض عدد الأسئلة
total_questions = sum(len(cat["questions"]) for cat in filtered_data)
st.info(f"عدد الأسئلة المعروضة: **{total_questions}**")

# شريط تقدم
progress_bar = st.progress(0)
answered_count = 0

# عرض الأسئلة حسب الفئة
for cat in filtered_data:
    st.subheader(f"📂 {cat['category']}")
    for idx, q in enumerate(cat["questions"]):
        # عرض السؤال
        st.markdown(f"**{idx+1}. {q['question']}**")

        if training_mode:
            # زر لإظهار الإجابة - استخدام مفتاح فريد
            button_key = f"btn_{cat['category']}_{idx}_{random.randint(0,100000)}"
            if st.button("إظهار الإجابة", key=button_key):
                st.success(q["answer"])
            else:
                st.write("🙈 الإجابة مخفية")
        else:
            st.write(q["answer"])

        st.markdown("---")
        answered_count += 1
        progress_bar.progress(answered_count / total_questions)

# إضافة نصائح عامة
with st.expander("💡 نصائح عامة للمقابلة"):
    st.markdown("""
    - **كوني واثقة وهادئة**، فالمقابلة حوار مهني.
    - **احفظي الأرقام والنسب** المهمة (نسب الاشتراكات، شروط التقاعد، المدد).
    - **استخدمي المصطلحات القانونية الدقيقة** دون تلعثم.
    - **أظهري اطلاعك على آخر التعديلات** (مثل نظام تخفيض الاشتراكات 45/2024، ونظام الشمول 14 وتعديلاته، وتعليمات السلف 2025).
    - **جهزي أمثلة واقعية** من تدريبك أو دراستك.
    - **التزمي بالصدق والشفافية** في الإجابات.
    - **استخدمي لغة الجسد الإيجابية** (الجلوس المعتدل، التواصل البصري، الابتسامة الخفيفة).
    """)

# معلومات عن الكفايات
with st.expander("📋 الكفايات الوظيفية لوظيفة قانوني (هيئة الخدمة والإدارة العامة)"):
    st.markdown("""
    تعتمد هيئة الخدمة والإدارة العامة في تقييم المتقدمين لوظيفة قانوني على عدة كفايات أساسية، منها:
    - **الكفاية القانونية**: المعرفة بالتشريعات والقدرة على التفسير والتحليل القانوني.
    - **كفاية الصياغة القانونية**: إعداد المذكرات والآراء والردود بدقة.
    - **كفاية الاتصال الفعال**: التواصل مع المراجعين والزملاء بوضوح واحترام.
    - **كفاية حل المشكلات**: القدرة على تحليل المواقف واتخاذ القرارات.
    - **كفاية النزاهة والمساءلة**: الالتزام بالسرية والمهنية ومكافحة الفساد.
    - **كفاية إدارة المعرفة**: استخدام التقنية وتنظيم المعلومات.
    - **كفاية العمل الجماعي**: التعاون مع فريق العمل.
    """)

st.markdown("---")
st.caption("تم التطوير بواسطة متدربة قانونية - لأغراض التدريب الشخصي")