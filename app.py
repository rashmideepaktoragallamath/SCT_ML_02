import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Smart Retail Customer Analytics Dashboard",
    page_icon="🛍",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/Mall_Customers.csv")

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("🎛 Dashboard Filters")

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + list(df["Gender"].unique())
)

if gender != "All":
    df = df[df["Gender"] == gender]

    


st.sidebar.markdown("---")
st.sidebar.write(f"👥 Total Customers: {len(df)}")
# -----------------------------
# TITLE
# -----------------------------
st.title("🛍 Smart Retail Customer Analytics Dashboard")
st.write("Interactive Customer Analytics and Segmentation Dashboard")

st.markdown("---")

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Customers", len(df))

with col2:
    st.metric(
        "💰 Avg Income",
        round(df["Annual Income (k$)"].mean(), 1)
    )

with col3:
    st.metric(
        "🛒 Avg Spending Score",
        round(df["Spending Score (1-100)"].mean(), 1)
    )

with col4:
    st.metric(
        "👨 Average Age",
        round(df["Age"].mean(), 1)
    )

st.markdown("---")

# -----------------------------
# DATASET PREVIEW
# -----------------------------
st.subheader("📋 Customer Dataset")

st.dataframe(df)

st.markdown("---")

# -----------------------------
# DATASET INFORMATION
# -----------------------------
left, right = st.columns(2)

with left:
    st.subheader("Dataset Shape")
    st.write(df.shape)

with right:
    st.subheader("Dataset Columns")
    st.write(df.columns.tolist())

st.markdown("---")

# -----------------------------
# CUSTOMER ANALYTICS
# -----------------------------
st.header("📊 Customer Analytics")

# Age Distribution
fig_age = px.histogram(
    df,
    x="Age",
    nbins=20,
    title="Age Distribution"
)

st.plotly_chart(fig_age, use_container_width=True)
# -----------------------------
# ELBOW METHOD
# -----------------------------

st.markdown("---")
st.header("🎯 Elbow Method for Optimal Clusters")

# Features for clustering
X = df[[
    "Annual Income (k$)",
    "Spending Score (1-100)"
]]

# Calculate WCSS
wcss = []

for i in range(1, 11):

    kmeans = KMeans(
        n_clusters=i,
        init="k-means++",
        random_state=42,
        n_init=10
    )

    kmeans.fit(X)

    wcss.append(kmeans.inertia_)

# Interactive Elbow Plot

fig_elbow = px.line(
    x=range(1, 11),
    y=wcss,
    markers=True,
    title="Elbow Method",
    labels={
        "x": "Number of Clusters (K)",
        "y": "WCSS"
    }
)

st.plotly_chart(
    fig_elbow,
    use_container_width=True
)

st.info(
    """
The Elbow Method helps identify the optimal number
of customer segments for K-Means clustering.
The 'bend' in the curve indicates a suitable value of K.
    """
)


# -----------------------------
# K-MEANS CLUSTERING
# -----------------------------

st.markdown("---")
st.header("🧠 Customer Segmentation")


# Features

X = df[[
    "Annual Income (k$)",
    "Spending Score (1-100)"
]]

# Train Model

kmeans = KMeans(
    n_clusters=5,
    init="k-means++",
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X)

score = silhouette_score(
    X,
    df["Cluster"]
)

score = silhouette_score(
    X,
    df["Cluster"]
)

st.metric(
    "📊 Silhouette Score",
    round(score, 3)
)

cluster_names = {
    0: "Regular Customers",
    1: "Premium Customers",
    2: "Smart Shoppers",
    3: "Careful Wealthy",
    4: "Budget Customers"
}

df["Customer Segment"] = df["Cluster"].map(cluster_names)
# Interactive Scatter Plot

fig_cluster = px.scatter(

    df,

    x="Annual Income (k$)",

    y="Spending Score (1-100)",

   color="Customer Segment",

    hover_data=[
        "CustomerID",
        "Gender",
        "Age"
    ],

    title="Customer Segments"
)

fig_cluster.add_scatter(
    x=kmeans.cluster_centers_[:, 0],
    y=kmeans.cluster_centers_[:, 1],
    mode="markers",
    marker=dict(
        size=18,
        symbol="x"
    ),
    name="Cluster Centers"
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True

)
st.write("### Customer Segment Distribution")

segment_count = df["Customer Segment"].value_counts()

st.bar_chart(segment_count)



st.subheader("📋 Cluster Summary")

cluster_summary = df.groupby(
    "Cluster"
)[
    [
        "Age",
        "Annual Income (k$)",
        "Spending Score (1-100)"
    ]
].mean()

cluster_summary["Customer Segment"] = cluster_summary.index.map(cluster_names)

cluster_summary = cluster_summary[
    [
        "Customer Segment",
        "Age",
        "Annual Income (k$)",
        "Spending Score (1-100)"
    ]
]

st.dataframe(
    cluster_summary.round(2)

    
)
# Download Segmented Dataset

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Segmented Dataset",
    data=csv,
    file_name="customer_segments.csv",
    mime="text/csv"
)
st.subheader("📍 Cluster Centers")

centers = pd.DataFrame(
    kmeans.cluster_centers_,
    columns=[
        "Annual Income (k$)",
        "Spending Score (1-100)"
    ]
)

st.dataframe(
    centers.round(2)
)





# -----------------------------
# CUSTOMER SEGMENT INSIGHTS
# -----------------------------

st.markdown("---")
st.subheader("💡 Customer Segment Insights")

segment_insights = {

    "Premium Customers":
    """
    ⭐ High Income + High Spending

    Recommendation:
    Offer VIP memberships, luxury products,
    and exclusive discounts.
    """,

    "Regular Customers":
    """
    👥 Average Income + Average Spending

    Recommendation:
    Loyalty programs and seasonal offers.
    """,

    "Smart Shoppers":
    """
    🛍 Low Income + High Spending

    Recommendation:
    Cashback offers and promotional campaigns.
    """,

    "Careful Wealthy":
    """
    💰 High Income + Low Spending

    Recommendation:
    Premium awareness campaigns and personalized marketing.
    """,

    "Budget Customers":
    """
    💵 Low Income + Low Spending

    Recommendation:
    Discount coupons and affordable product bundles.
    """
}

for segment in cluster_names.values():

    st.success(segment)

    st.write(
        segment_insights[segment]
    )


# Income Distribution
fig_income = px.histogram(
    df,
    x="Annual Income (k$)",
    nbins=20,
    title="Annual Income Distribution"
)

st.plotly_chart(fig_income, use_container_width=True)

# Spending Score Distribution
fig_spending = px.histogram(
    df,
    x="Spending Score (1-100)",
    nbins=20,
    title="Spending Score Distribution"
)

st.plotly_chart(fig_spending, use_container_width=True)

# Gender Distribution
gender_count = df["Gender"].value_counts()

fig_gender = px.pie(
    values=gender_count.values,
    names=gender_count.index,
    title="Gender Distribution"
)

st.plotly_chart(fig_gender, use_container_width=True)

# -----------------------------
# LIVE CUSTOMER PREDICTOR
# -----------------------------

st.markdown("---")
st.header("🔮 Live Customer Segment Predictor")

income = st.slider(
    "Annual Income (k$)",
    0,
    150,
    60
)

spending = st.slider(
    "Spending Score",
    0,
    100,
    50
)
if st.button("Predict Customer Segment"):

    prediction = kmeans.predict(
        [[income, spending]]
    )[0]

    segment = cluster_names[prediction]

    st.success(
        f"Predicted Segment: {segment}"
    )
    st.write(
        segment_insights[segment]
    )

    st.markdown("---")

st.caption("Dataset loaded successfully")
   


# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.caption(
    "Developed by Rashmi Deepak Toragallamath"
)