import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import subprocess

# Load dataset (correct path!)
df = pd.read_csv("/Users/anandshukla/Downloads/project/walmart_sales.csv")

# Clean data
df["unit_price"] = df["unit_price"].replace(r'[\$,]', '', regex=True).astype(float)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
df["total"] = df["unit_price"] * df["quantity"]

# Group by city
city_sales = df.groupby("City")["total"].sum().sort_values(ascending=False)
top_10 = city_sales.head(10)
others = city_sales[10:].sum()
top_10_with_others = top_10.copy()
if others > 0:
    top_10_with_others["Others"] = others

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# --- Pie Chart ---
colors = plt.cm.tab20.colors
ax1.pie(
    top_10_with_others,
    labels=None,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    textprops={'fontsize': 9}
)
ax1.set_title("Sales Distribution by City", fontsize=14)
ax1.legend(top_10_with_others.index, loc="upper left", bbox_to_anchor=(1, 1))

# --- Bar Chart ---
sorted_top_10 = top_10.sort_values()
bars = ax2.barh(sorted_top_10.index, sorted_top_10.values, color='skyblue', edgecolor='black')
ax2.set_xlabel("Total Sales (USD)")
ax2.set_title("Top 10 Cities by Total Sales")
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Use index for bar annotation to avoid conversion issues
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width + 1000, bar.get_y() + bar.get_height() / 2,
             f"${width:,.0f}", va='center', fontsize=8)

ax2.invert_yaxis()

# Save and open
output_folder = "/Users/anandshukla/Downloads/Reports"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "city_sales_analysis.png")

plt.tight_layout()
plt.savefig(output_path, dpi=300)
plt.show()

subprocess.run(["open", output_path])
