import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import subprocess  # <-- To auto-open the saved file on macOS

# Load the dataset
df = pd.read_csv("/Users/anandshukla/Downloads/project/walmart_sales.csv")

# Clean and prepare data
df["unit_price"] = df["unit_price"].replace('[\$,]', '', regex=True).astype(float)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
df["total"] = df["unit_price"] * df["quantity"]

# Group by City and filter non-zero
city_sales = df.groupby("City")["total"].sum()
city_sales = city_sales[city_sales > 0]
city_sales_sorted = city_sales.sort_values(ascending=False)

# Prepare top 10 + others
top_10 = city_sales_sorted[:10]
others = city_sales_sorted[10:].sum()
top_10_with_others = top_10.copy()
top_10_with_others["Others"] = others
top_10_with_others = top_10_with_others.sort_values(ascending=False)

# ---------- Plotting ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Pie Chart
wedges, texts, autotexts = ax1.pie(
    top_10_with_others,
    labels=top_10_with_others.index,
    autopct="%1.1f%%",
    startangle=140,
    textprops={'fontsize': 9}
)
ax1.set_title("Sales Distribution by City", fontsize=14)

# Bar Chart
bars = top_10.sort_values().plot.barh(
    ax=ax2, 
    color='cornflowerblue',
    edgecolor='black'
)
ax2.set_xlabel("Total Sales (USD)")
ax2.set_ylabel("City")
ax2.set_title("Top 10 Cities by Total Sales", fontsize=14)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax2.bar_label(bars.containers[0], fmt='${:,.0f}', label_type='edge', fontsize=8, padding=3)
ax2.invert_yaxis()

# ---------- Save to Reports folder ----------
output_folder = "/Users/anandshukla/Downloads/Reports"
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist
output_path = os.path.join(output_folder, "city_sales_charts.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.tight_layout()
plt.show()

# ---------- Open image automatically (macOS) ----------
subprocess.run(["open", output_path])
