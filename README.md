# aldaketa

This project focuses on simulating environmental sensor data for smart monitoring systems in the context of water quality monitoring as critical monitoring system for public health and environmental sustainability. Water supply networks are vulnerable to contamination, and timely detection of anomalies is essential for safe drinking water. Modern water systems use IoT sensors to collect high-frequency data (e.g., every minute) from various points in the distribution network.

The GECCO Industrial Challenges ([2018](https://www.spotseven.de/wp-content/uploads/2018/03/rulesGeccoIc2018.pdf) & [2019](https://www.th-koeln.de/mam/downloads/deutsch/hochschule/fakultaeten/informatik_und_ingenieurwissenschaften/rulesgeccoic2019.pdf)) provide real-world datasets and problem settings for developing and benchmarking algorithms for online anomaly/event/change detection in water quality time series. The datasets from GECCo 2018-2019 are harmonized, concatenated and processed to create a unified synthetic dataset for this project.

The project involves creating a synthetic dataset that mimics real sensor data measurements used in water plants, and prepares the data for future use in a blockchain-based system for secure, decentralized record-keeping.

## Video Demo/Progress Status Links

### **MS 1**

- [Synthetic Dataset Generation (Homework: IoT Data Simulation)](https://drive.google.com/file/d/1i2STo8zj-oua7US0VUT7f-CipsdU9ohW/view?usp=sharing)

- [MS 1: Smart Tracking System Blockchain Ledger (Submission) & Homework: Smart Contract Data Storage](https://drive.google.com/file/d/1fT1l-TnQwg0FcFutXhAwIiXu_CBvB9aP/view?usp=sharing)

## Reference

Moritz, S., Rehbach, F., Chandrasekaran, S., Rebolledo, M., & Thomas Bartz-Beielstein. (2018). GECCO Industrial Challenge 2018 Dataset: A water quality dataset for the 'Internet of Things: Online Anomaly Detection for Drinking Water Quality' competition at the Genetic and Evolutionary Computation Conference 2018, Kyoto, Japan. [Data set]. The Genetic and Evolutionary Computation Conference (GECCO), Kyoto, Japan. Zenodo. [https://doi.org/10.5281/zenodo.3884398](https://doi.org/10.5281/zenodo.3884398)

Moritz, S., Rehbach, F., & Bartz-Beielstein, T. (2019). GECCO Industrial Challenge 2019 Dataset: A water quality dataset for the 'Internet of Things: Online Event Detection for Drinking Water Quality Control' competition at the Genetic and Evolutionary Computation Conference 2019, Prague, Czech Republic. [Data set]. The Genetic and Evolutionary Computation Conference (GECCO), Prague, Czech Republic. Zenodo. [https://doi.org/10.5281/zenodo.4304080](https://doi.org/10.5281/zenodo.4304080)

---

## **MS 2: Blockchain-Verified IoT Water Quality Dashboard**

### Overview

The **Milestone 2 project** is an interactive, blockchain-enhanced water quality monitoring dashboard built using **Streamlit**, **Plotly**, **Altair**, and **Pandas**.  
It integrates IoT sensor data with blockchain-inspired hash validation to ensure **tamper detection**, **traceability**, and **data integrity**.  

This project is part of an academic prototype by [Arnel Imperial](https://github.com/imperionite) for demonstrating how **blockchain concepts** can secure IoT sensor networks in critical infrastructure like water treatment facilities.

### Features

- **Dual visualizations**
  - *IoT Water Quality Dashboard* — high-resolution time series analysis, anomaly detection, and threshold monitoring.
  - *Blockchain-Verified Monitoring* — simulates ledger hashing, tampering detection, and data provenance.
  
- **Water Quality Index (WQI) estimation**
- **Tampering simulation** — see how malicious changes are detected via hash mismatches.
- **Custom alerts and KPI summaries**
- **Export filtered datasets**
- **Interactive charts with Altair & Plotly**

### Istallation

1️⃣ Clone the repository:
```bash
git clone https://github.com/imperionite/aldaketa.git
cd aldaketa
````

2️⃣ Install requirements:

```bash
pip install -r requirements.txt
```

> 📌 If `requirements.txt` isn't available:

```bash
pip install streamlit pandas plotly altair numpy
```

3️⃣ Place your cleaned IoT CSV file (`cleaned_iot_data.csv`) in the project directory.

4️⃣ Run:

```bash
streamlit run main.py
```

### Data Requirements

The app expects:

* A CSV file named `cleaned_iot_data.csv`
* Columns:

  * `timestamp` (parseable datetime)
  * `sensor_id`
  * `data_type`
  * `numeric_value`

### Known Warnings & Workarounds

👉 **Pandas `FutureWarning`: incompatible dtype assignment**
When simulating tampering (e.g. multiplying pH values by 1.2), Pandas warns about mixing `int64` and `float64`.

✅ **Solution implemented in code:**
We explicitly cast `numeric_value` to `float` before modifying:

```python
tampered["numeric_value"] = tampered["numeric_value"].astype(float)
tampered.loc[tampered["data_type"] == "pH", "numeric_value"] *= 1.2
```

This ensures no dtype conflicts and future compatibility.

---

👉 **Large datasets may slow down rendering**
This is inherent to Streamlit’s reactivity + heavy visualizations.

✅ **Workaround:** Use filtering options in sidebar to limit data volume.

### Sample Screenshots

![Image 1](https://drive.google.com/uc?id=1aREWd75C6FWgiJae7wJOM_vzayJ9UuVC)

![Image 1](https://drive.google.com/uc?id=1ASxkLzmkD5rVNMmmmCrrcgdMmXFET96A)

![Image 1](https://drive.google.com/uc?id=1f_eVyloyaxKaQHIDP5AxTgAEsMRy7DG7)

![Image 1](https://drive.google.com/uc?id=1MhDSq-2a0RRIpQ-tX7YPOOKPIJQCsYsw)

![Image 1](https://drive.google.com/uc?id=1F35BA2fsa3t09jflAPm09upyNAkmolD-)

![Image 1](https://drive.google.com/uc?id=1MVcPi4EhK8l6Wcog8aDrqVoAEQ8n-bro)




