"""
StyleMI Streamlit dashboard.
Run with: streamlit run frontend/app.py --server.port 8501
"""
import os
import requests
import streamlit as st
import pandas as pd
import plotly.express as px

API_URL = os.getenv("STYLEMI_API_URL", "http://localhost:8000")

st.set_page_config(page_title="StyleMI", page_icon="", layout="wide")
st.title("StyleMI - Fashion Recommendation Engine")
st.caption("Outfit suggestions powered by CLIP embeddings, weather, and ensemble ML.")

tabs = st.tabs(["Upload", "Recommend", "History", "Analytics", "Preferences"])

with tabs[0]:
    st.subheader("Upload an outfit")
    uploaded = st.file_uploader("Outfit image", type=["jpg", "jpeg", "png", "webp"])
    col1, col2, col3 = st.columns(3)
    with col1:
        occasion = st.selectbox("Occasion", ["casual", "formal", "athletic", "evening", "business", "party"])
    with col2:
        season = st.selectbox("Season", ["summer", "winter", "spring", "autumn", "all"])
    with col3:
        user_id = st.number_input("User ID", min_value=1, value=1)
    if uploaded and st.button("Upload"):
        files = {"file": (uploaded.name, uploaded.getvalue())}
        data = {"occasion": occasion, "season": season, "user_id": user_id}
        r = requests.post(f"{API_URL}/api/outfits/upload", files=files, data=data, timeout=60)
        if r.ok:
            st.success(f"Uploaded outfit #{r.json()['id']}")
            st.json(r.json())
            st.image(uploaded, width=300)
        else:
            st.error(r.text)

with tabs[1]:
    st.subheader("Get recommendations")
    c1, c2, c3, c4 = st.columns(4)
    with c1: r_user = st.number_input("User", min_value=1, value=1, key="ru")
    with c2: r_occ = st.selectbox("Occasion", ["casual", "formal", "athletic", "evening", "business", "party"], key="ro")
    with c3: r_city = st.text_input("City", "New York")
    with c4: r_topk = st.slider("Top-K", 1, 10, 5)
    seed = st.number_input("Seed outfit (optional)", value=0, step=1)
    if st.button("Recommend"):
        payload = {"user_id": int(r_user), "occasion": r_occ, "city": r_city, "top_k": int(r_topk)}
        if seed > 0:
            payload["seed_outfit_id"] = int(seed)
        r = requests.post(f"{API_URL}/api/recommend/", json=payload, timeout=30)
        if r.ok:
            recs = r.json()["recommendations"]
            df = pd.DataFrame(recs)
            st.dataframe(df, use_container_width=True)
            if not df.empty:
                fig = px.bar(df, x="outfit_id", y="score", color="occasion", title="Top recommendations")
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("Score components"):
                    comps = pd.json_normalize(df["components"])
                    comps["outfit_id"] = df["outfit_id"]
                    st.dataframe(comps, use_container_width=True)
        else:
            st.error(r.text)

with tabs[2]:
    st.subheader("Recommendation history")
    h_user = st.number_input("User ID", min_value=1, value=1, key="hu")
    if st.button("Load history"):
        r = requests.get(f"{API_URL}/api/recommend/history/{int(h_user)}", timeout=30)
        if r.ok:
            st.dataframe(pd.DataFrame(r.json()), use_container_width=True)
        else:
            st.error(r.text)

with tabs[3]:
    st.subheader("Beta-test analytics")
    metrics_path = "ml_pipeline/results/metrics.csv"
    if os.path.exists(metrics_path):
        df = pd.read_csv(metrics_path)
        st.dataframe(df, use_container_width=True)
        fig = px.bar(df, x="metric", y="value", title="Recommendation accuracy")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run python ml_pipeline/beta_simulation.py to generate metrics.")

with tabs[4]:
    st.subheader("User preferences")
    p_user = st.number_input("User ID", min_value=1, value=1, key="pu")
    colors = st.text_input("Favorite colors (comma-separated)", "blue,white,black")
    styles = st.text_input("Favorite styles", "minimalist,classic")
    avoid = st.text_input("Avoid tags", "neon,leopard")
    if st.button("Save preferences"):
        payload = {"user_id": int(p_user), "favorite_colors": [c.strip() for c in colors.split(",") if c.strip()], "favorite_styles": [s.strip() for s in styles.split(",") if s.strip()], "avoid_tags": [a.strip() for a in avoid.split(",") if a.strip()]}
        r = requests.post(f"{API_URL}/api/users/preferences", json=payload, timeout=20)
        st.success("Saved") if r.ok else st.error(r.text)
