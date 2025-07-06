import streamlit as st

# --- Visualization Selector ---
viz_choice = st.radio(
    "Select Visualization",
    [
        "Visualization 1: IoT Water Quality Dashboard",
        "Visualization 2: Blockchain-Verified Monitoring",
    ],
)

# --- Unified Title & Intro ---
st.title("💧 IoT & Blockchain-Enabled Water Quality Dashboard")

st.markdown("""
This data visualization project provides comprehensive water quality monitoring using IoT sensor networks,
augmented with blockchain verification for data integrity and security.  
Select a visualization mode below to explore trends, scores, and tamper detection features.
""")

if viz_choice == "Visualization 1: IoT Water Quality Dashboard":
    import pandas as pd
    import numpy as np
    import altair as alt

    st.markdown("""
    **Mode:** IoT Water Quality Dashboard  
    This mode provides detailed analysis of sensor readings, descriptive statistics, and trends over time.  
    Ideal for diagnostics, performance tracking, and evaluating interventions.
    """)

    # --- Load Data ---
    @st.cache_data(ttl=300)
    def load_data():
        csv_file = "cleaned_iot_data.csv"
        df = pd.read_csv(csv_file, parse_dates=["timestamp"])
        df.set_index("timestamp", inplace=True)
        return df

    df = load_data()

    # --- Compute Actual Sampling Interval ---
    time_diffs = df.index.to_series().sort_values().diff().dropna()
    mode_interval = time_diffs.mode().iloc[0]
    interval_seconds = int(mode_interval.total_seconds())

    # --- Sidebar Controls ---
    st.sidebar.header("Parameter Selection")
    parameters = df["data_type"].unique().tolist()
    selected_params = st.sidebar.multiselect(
        "Select Parameters to Visualize", parameters, default=parameters
    )

    st.sidebar.markdown("""
    Explore trends from a high-resolution monitoring session.
    Use the controls above to isolate parameters of interest.
    """)

    agg_option = st.sidebar.selectbox(
        "Aggregate Data By", options=["Raw (No aggregation)", "Minute", "Hour"], index=0
    )

    st.sidebar.markdown("### Thresholds for Reference")
    thresholds = {}
    for param in selected_params:
        param_values = df[df["data_type"] == param]["numeric_value"]
        min_val, max_val = int(param_values.min()), int(param_values.max())
        if min_val < max_val:
            thresholds[param] = st.sidebar.slider(
                f"{param} Range", min_val, max_val, (min_val, max_val)
            )
        else:
            st.sidebar.markdown(f"Only one unique value ({min_val}) for `{param}`.")
            thresholds[param] = (min_val, max_val)

    smoothing = st.sidebar.checkbox("Show Moving Average (window=3)", value=False)

    # --- Data Filtering ---
    filtered_df = df[df["data_type"].isin(selected_params)].copy()

    def aggregate_df(df, agg_option):
        if agg_option == "Raw (No aggregation)":
            return df
        elif agg_option == "Minute":
            return (
                df.groupby(["data_type", pd.Grouper(freq="T")])["numeric_value"]
                .mean()
                .reset_index()
                .set_index("timestamp")
            )
        elif agg_option == "Hour":
            return (
                df.groupby(["data_type", pd.Grouper(freq="H")])["numeric_value"]
                .mean()
                .reset_index()
                .set_index("timestamp")
            )
        else:
            return df

    agg_df = aggregate_df(filtered_df, agg_option)

    st.subheader("📈 Key Metrics")
    kpi_cols = st.columns(len(selected_params))
    for idx, param in enumerate(selected_params):
        param_df = agg_df[agg_df["data_type"] == param]
        if not param_df.empty:
            latest = param_df.sort_index().iloc[-1]
            average = param_df["numeric_value"].mean()
            kpi_cols[idx].metric(
                label=param,
                value=f"{latest['numeric_value']:.2f}",
                delta=f"Avg: {average:.2f}",
            )
        else:
            kpi_cols[idx].metric(label=param, value="N/A", delta="No data")

    st.subheader("📈 Descriptive Statistics")
    desc_stats = []
    for param in selected_params:
        param_df = filtered_df[filtered_df["data_type"] == param]["numeric_value"]
        stats = {
            "Parameter": param,
            "Count": param_df.count(),
            "Mean": param_df.mean(),
            "Std": param_df.std(),
            "Min": param_df.min(),
            "25%": param_df.quantile(0.25),
            "50%": param_df.median(),
            "75%": param_df.quantile(0.75),
            "Max": param_df.max(),
            "Unique": param_df.nunique(),
        }
        desc_stats.append(stats)
    desc_df = pd.DataFrame(desc_stats)
    st.dataframe(
        desc_df.set_index("Parameter").style.format(
            "{:.2f}", subset=["Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
        )
    )

    st.subheader("📈 Automated Insights")
    flat_params = []
    for param in selected_params:
        unique_vals = filtered_df[filtered_df["data_type"] == param][
            "numeric_value"
        ].nunique()
        if unique_vals == 1:
            flat_params.append(param)

    for param in selected_params:
        param_df = filtered_df[filtered_df["data_type"] == param]["numeric_value"]
        if param in flat_params:
            st.info(
                f"**{param}** remained constant at {param_df.iloc[0]:.2f} throughout the session."
            )
        else:
            st.markdown(
                f"- **{param}** fluctuated between {param_df.min():.2f} and {param_df.max():.2f} (mean: {param_df.mean():.2f}, std: {param_df.std():.2f})."
            )

    st.subheader("📈 Parameter Trends Over Time")
    for param in selected_params:
        if param in flat_params:
            st.info(f"No variation detected for {param}; skipping plot.")
            continue

        param_df = agg_df[agg_df["data_type"] == param].sort_index()
        if param_df.empty:
            st.info(f"No data for {param} in dataset.")
            continue

        chart_df = param_df.copy()
        if smoothing:
            chart_df["smoothed"] = (
                chart_df["numeric_value"].rolling(window=3, min_periods=1).mean()
            )

        rolling_mean = chart_df["numeric_value"].rolling(window=5, min_periods=1).mean()
        rolling_std = chart_df["numeric_value"].rolling(window=5, min_periods=1).std()
        chart_df["anomaly"] = (
            np.abs(chart_df["numeric_value"] - rolling_mean) > 2 * rolling_std
        )

        base = (
            alt.Chart(chart_df.reset_index())
            .mark_line(point=True)
            .encode(
                x=alt.X("timestamp:T", title="Timestamp"),
                y=alt.Y("numeric_value:Q", title=param),
                tooltip=["timestamp:T", "numeric_value:Q"]
                + (["smoothed:Q"] if smoothing else []),
            )
            .properties(title=f"{param} Over Time", height=300)
        )

        chart = base
        if smoothing:
            smooth_line = (
                alt.Chart(chart_df.reset_index())
                .mark_line(color="red")
                .encode(x="timestamp:T", y="smoothed:Q")
            )
            chart += smooth_line

        anomaly_points = (
            alt.Chart(chart_df.reset_index())
            .mark_point(color="orange", size=60, filled=True)
            .encode(
                x="timestamp:T",
                y="numeric_value:Q",
                tooltip=["timestamp:T", "numeric_value:Q"],
            )
            .transform_filter(alt.datum.anomaly)
        )
        chart += anomaly_points

        lower, upper = thresholds[param]
        rules = (
            alt.Chart(
                pd.DataFrame(
                    {
                        "threshold": [lower, upper],
                        "label": ["Lower Limit", "Upper Limit"],
                    }
                )
            )
            .mark_rule(strokeDash=[4, 2], color="orange")
            .encode(y="threshold:Q", tooltip=["label:N", "threshold:Q"])
        )

        st.altair_chart(chart + rules, use_container_width=True)
        st.caption(f"""
        This chart shows fluctuations in {param} over the monitoring period.
        Outliers (orange dots) represent values significantly different from recent trends.
        Dashed lines indicate thresholds for reference.
        """)

    st.subheader("📊 Session Summary")
    st.markdown(
        f"""
        - **Monitoring Duration:** {df.index.min().strftime("%Y-%m-%d %H:%M:%S")} to {df.index.max().strftime("%Y-%m-%d %H:%M:%S")}
        - **Monitored Parameters:** {", ".join(selected_params)}
        - **Total Records Displayed:** {len(filtered_df)}
        - **Approximate Sampling Rate:** ~{interval_seconds} seconds
        - **Aggregation Level:** {agg_option}
        """
    )

    with st.expander("📂 View & Export Raw Sensor Data"):
        st.dataframe(filtered_df)
        csv = filtered_df.to_csv().encode("utf-8")
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_iot_data.csv",
            mime="text/csv",
        )

elif viz_choice == "Visualization 2: Blockchain-Verified Monitoring":
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import hashlib
    import numpy as np

    st.markdown("""
    **Mode:** Blockchain-Verified Monitoring  
    This mode emphasizes data integrity, provenance, and tamper detection, using blockchain principles.
    Explore WQI scores, hash validations, and tampering simulations to understand data security.
    """)

    # --- Load Data ---
    @st.cache_data
    def load_data():
        df = pd.read_csv("cleaned_iot_data.csv", parse_dates=["timestamp"])
        df.set_index("timestamp", inplace=True)
        df["ledger_hash"] = df.apply(
            lambda row: hashlib.sha256(
                f"{row['sensor_id']}{row['data_type']}{row['numeric_value']}{row.name}".encode()
            ).hexdigest(),
            axis=1,
        )

        def wqi(row):
            score = 100
            if row["data_type"] == "pH" and (
                row["numeric_value"] < 6.5 or row["numeric_value"] > 8.5
            ):
                score -= 30
            if row["data_type"] == "Turbidity (NTU)" and row["numeric_value"] > 5:
                score -= 25
            if row["data_type"] == "Temperature (°C)" and (
                row["numeric_value"] < 5 or row["numeric_value"] > 35
            ):
                score -= 10
            if (
                row["data_type"] == "Conductivity (µS/cm)"
                and row["numeric_value"] > 1500
            ):
                score -= 15
            if row["data_type"] == "ClO2 MS1 (mg/L)" and not (
                0.2 <= row["numeric_value"] <= 0.8
            ):
                score -= 20
            return max(score, 0)

        df["WQI_score"] = df.apply(wqi, axis=1)
        return df

    df = load_data()

    st.sidebar.title("📌 Controls")
    sensor_choices = df["sensor_id"].unique().tolist()
    type_choices = df["data_type"].unique().tolist()
    sensors = st.sidebar.multiselect(
        "Sensor(s)", sensor_choices, default=sensor_choices
    )
    types = st.sidebar.multiselect("Data Type(s)", type_choices, default=type_choices)
    date_range = st.sidebar.date_input(
        "Date Range", [df.index.min().date(), df.index.max().date()]
    )

    filtered = df[(df.index.date >= date_range[0]) & (df.index.date <= date_range[1])]
    filtered = filtered[
        filtered["sensor_id"].isin(sensors) & filtered["data_type"].isin(types)
    ]

    st.subheader("📈 Water Quality Index (WQI) Overview")
    st.markdown(
        "WQI summarizes overall water quality. 90+ is Good, 70-89 Moderate, below 70 Poor."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("📉 Avg WQI", f"{filtered['WQI_score'].mean():.1f}")
    col2.metric("⚠️ Alerts (>10% drop)", (filtered["WQI_score"] < 90).sum())
    col3.metric("🔒 Blockchain Hashes", f"{filtered['ledger_hash'].nunique()} Unique")

    avg_wqi = filtered["WQI_score"].mean()
    if avg_wqi >= 90:
        wqi_status = "Good"
        gauge_color = "green"
    elif avg_wqi >= 70:
        wqi_status = "Moderate"
        gauge_color = "orange"
    else:
        wqi_status = "Poor"
        gauge_color = "red"

    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_wqi,
            title={"text": f"Avg WQI ({wqi_status})"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": gauge_color},
                "steps": [
                    {"range": [0, 70], "color": "red"},
                    {"range": [70, 90], "color": "orange"},
                    {"range": [90, 100], "color": "green"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": avg_wqi,
                },
            },
            number={"suffix": f" ({wqi_status})", "font": {"color": gauge_color}},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_gauge, use_container_width=False)
    st.caption(
        "Gauge shows average WQI for selected data. Status is shown in the number and title."
    )

    st.subheader("🔗 Blockchain Integrity Trace")
    filtered = filtered.copy()
    filtered["block_id"] = (filtered.reset_index(drop=True).index // 10) + 1
    filtered["validation_node"] = filtered["block_id"].apply(
        lambda x: f"Node-{x % 3 + 1}"
    )
    st.dataframe(
        filtered.head(10)[
            [
                "sensor_id",
                "data_type",
                "numeric_value",
                "ledger_hash",
                "block_id",
                "validation_node",
            ]
        ]
    )

    st.subheader("📈 Sensor Readings Over Time")
    fig = px.line(
        filtered,
        x=filtered.index,
        y="numeric_value",
        color="data_type",
        hover_data=["sensor_id", "WQI_score", "block_id"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Tampered Data Detection")
    st.markdown(
        "Simulate a data breach: pH values artificially increased by 20%. Blockchain hashes reveal tampering."
    )
    tampered = filtered.copy()
    tampered["numeric_value"] = tampered["numeric_value"].astype(float)
    tampered.loc[tampered["data_type"] == "pH", "numeric_value"] *= 1.2
    tampered["tampered_hash"] = tampered.apply(
        lambda row: hashlib.sha256(
            f"{row['sensor_id']}{row['data_type']}{row['numeric_value']}{row.name}".encode()
        ).hexdigest(),
        axis=1,
    )
    tampered["tampered"] = tampered["ledger_hash"] != tampered["tampered_hash"]

    if tampered["tampered"].any():
        st.error("📈 Tampering Detected! Hash mismatch found.")
        st.dataframe(
            tampered[tampered["tampered"]][
                [
                    "sensor_id",
                    "data_type",
                    "numeric_value",
                    "ledger_hash",
                    "tampered_hash",
                ]
            ]
        )
    else:
        st.success("✅ No tampering detected.")

    st.subheader("🚨 Set Custom Alert Threshold")
    alert_type = st.selectbox("Choose Data Type for Alerts", type_choices)
    threshold = st.slider(
        "Threshold value",
        float(filtered["numeric_value"].min()),
        float(filtered["numeric_value"].max()),
        step=0.5,
    )
    alert_df = filtered[
        (filtered["data_type"] == alert_type) & (filtered["numeric_value"] > threshold)
    ]
    st.markdown(
        f"**Alert: {len(alert_df)} readings exceed {threshold} in {alert_type}**"
    )
    if not alert_df.empty:
        st.dataframe(alert_df[["sensor_id", "numeric_value", "WQI_score"]].head(10))

    st.subheader("📈 Sensor Uptime & Activity")
    activity_df = (
        filtered.reset_index()
        .groupby(["sensor_id", pd.Grouper(key="timestamp", freq="h")])
        .size()
        .reset_index(name="readings")
    )
    fig_activity = px.bar(
        activity_df,
        x="timestamp",
        y="readings",
        color="sensor_id",
        barmode="group",
        labels={"readings": "Readings per Hour"},
        title="Sensor Activity",
    )
    st.plotly_chart(fig_activity, use_container_width=True)

    with st.expander("📈 Why Blockchain for IoT Data?"):
        st.markdown("""
        - **Immutability**: Once recorded, data cannot be altered undetectably.
        - **Traceability**: Each reading includes a timestamp and identity.
        - **Tamper Detection**: Any post-recording change results in hash mismatch.
        - **Audit-Ready**: Ensures data integrity for compliance and research.
        """)

    with st.expander("📂 View & Export Raw Sensor Data"):
        st.dataframe(filtered)
        csv = filtered.to_csv().encode("utf-8")
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_iot_data.csv",
            mime="text/csv",
        )

    st.subheader("📊 Session Summary")
    st.markdown(
        f"""
        - **Monitoring Duration:** {df.index.min().strftime("%Y-%m-%d %H:%M:%S")} to {df.index.max().strftime("%Y-%m-%d %H:%M:%S")}
        - **Monitored Parameters:** {", ".join(types)}
        - **Total Records Displayed:** {len(filtered)}
        """
    )


st.markdown("---")
st.markdown(
    "An open-source project built by [Arnel Imperial](https://github.com/imperionite) for Applications Development and Emerging Technologies course in MMDC. "
    "Source code available on [GitHub](https://github.com/imperionite/aldaketa)."
)
