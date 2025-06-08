import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# قراءة ملف Excel
file_path = r"C:\Users\mosta\Desktop\Echo-Media\ramadan2018.xlsx"
df = pd.read_excel(file_path)

# تنظيف أسماء الأعمدة وتحويل Air Date إلى تاريخ فقط
df.columns = df.columns.str.strip().str.lower()
df["air date"] = pd.to_datetime(df["air date"]).dt.date

# إعداد الصفحة مع تغيير اللون إلى الرمادي
st.set_page_config(page_title="Echo Media Dashboard", layout="centered")
st.markdown("<style>body { background-color: #f0f0f0; }</style>", unsafe_allow_html=True)

# تصميم CSS لإظهار التوقيع في أعلى يسار الصفحة بلون أحمر ثقيل
signature_style = """
<style>
.signature {
    position: absolute;
    top: 10px;
    left: 10px;
    color: red;
    font-weight: bold;
    font-size: 16px;
}
</style>
"""
st.markdown(signature_style, unsafe_allow_html=True)
st.markdown('<div class="signature">Designed by: Mostafa ElBeshbeshy</div>', unsafe_allow_html=True)

# تصميم Sidebar للتنقل بين الصفحات
st.sidebar.markdown("## Navigation")
selected_page = st.sidebar.radio("🔹 Click to Navigate", ["📊 Statistics", "📈 Charts"])

# **صفحة الإحصائيات**
if selected_page == "📊 Statistics":
    st.title("📊 **Echo Media Dashboard**")
    st.markdown("### **Summary of Data**")

    stats = {
        "📌 Total Seconds": f"{df['duration'].sum():,} Seconds",
        "📌 Total Spots": f"{df['spot count'].sum():,} Spots",
        "📌 EQ Spots": f"{round(df['eq spot'].sum(), 2):,}",
        "📌 Number of Channels": f"{df['channel'].nunique():,}",
        "📌 Number of Media Agencies": f"{df['media agency'].nunique():,}",
        "📌 Number of Brands": f"{df['brand'].nunique():,}",
        "📌 Number of Categories": f"{df['sub.category'].nunique():,}",
        "📌 Number of Content": f"{df['content'].nunique():,}",
        "📌 Number of Clients": f"{df['client'].nunique():,}",
    }

    # إضافة تأثير لوني للكروت وجعل النص في المنتصف
    card_style = """
    <style>
    .card {
        background: linear-gradient(to right, #E3F2FD, #FFFFFF);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.1);
        margin-bottom: 12px;
        text-align: center;
    }
    .card h3 {
        color: #333;
        font-size: 20px;
        font-weight: bold;
    }
    .card h2 {
        color: #007BFF;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    for key, value in stats.items():
        st.markdown(f"""
        <div class="card">
            <h3>{key}</h3>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

# **صفحة الرسوم البيانية**
elif selected_page == "📈 Charts":
    st.title("📈 **Interactive Charts**")
    st.markdown("### **Select a Filter to View the Top 10 Results**")

    # اختيار نوع التحليل
    analysis_type = st.selectbox("📊 Select Analysis Type", ["Top 10 Channels", "Top 10 Media Agencies", "Top 10 Brands", "Top 10 Categories"])

    # تحديد العمود المستخدم في الفلترة
    column_mapping = {
        "Top 10 Channels": "channel",
        "Top 10 Media Agencies": "media agency",
        "Top 10 Brands": "brand",
        "Top 10 Categories": "sub.category"
    }
    selected_column = column_mapping[analysis_type]

    # اختيار أعلى 10 عناصر بناءً على إجمالي الثواني
    top_10 = df.groupby(selected_column)["duration"].sum().reset_index()
    top_10_sorted = top_10.sort_values(by="duration", ascending=False).head(10)

    # إنشاء الرسم البياني باستخدام Seaborn بألوان أكثر جاذبية
    st.subheader(f"{analysis_type} by Total Seconds")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="duration", y=selected_column, data=top_10_sorted, palette="coolwarm", ax=ax)
    ax.set_xlabel("Total Seconds")
    ax.set_ylabel(selected_column)
    ax.set_title(f"{analysis_type} by Total Seconds", fontsize=14)
    
    # عرض الرسم البياني
    st.pyplot(fig)