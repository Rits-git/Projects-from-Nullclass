import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("D:/nullclass new/assignment - 1/preference_vs_worktype_intern.csv")

# -------------------------
# Apply filters
# -------------------------

# 1. Work Type must be "Intern"
filtered_df = df[df["WorkType"] == "Intern"]

# 2. Latitude < 10
filtered_df = filtered_df[filtered_df["Latitude"] < 10]

# 3. Country name must not start with A, B, C, or D
filtered_df = filtered_df[~filtered_df["Country"].str.startswith(tuple("ABCD"))]

# 4. Job Title must be a single word with fewer than 10 characters
filtered_df = filtered_df[
    (filtered_df["JobTitle"].str.len() < 10) &
    (~filtered_df["JobTitle"].str.contains(" "))
]

# 5. Company Size < 50,000
filtered_df = filtered_df[filtered_df["CompanySize"] < 50000]

# 6. Salary > 9,000
filtered_df = filtered_df[filtered_df["Salary"] > 9000]

# 7. Experience is an even number
filtered_df = filtered_df[filtered_df["Experience"] % 2 == 0]

# 8. Job Posting Date is in an odd-numbered month
filtered_df["JobPostingDate"] = pd.to_datetime(filtered_df["JobPostingDate"])
filtered_df = filtered_df[filtered_df["JobPostingDate"].dt.month % 2 == 1]

# -------------------------
# Time restriction: 3 PM to 5 PM IST
# -------------------------
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist).time()

if current_time >= datetime.strptime("15:00:00", "%H:%M:%S").time() and \
   current_time <= datetime.strptime("17:00:00", "%H:%M:%S").time():

    # Group by Preference and count
    bar_data = filtered_df.groupby("Preference").size().reset_index(name="Count")

    # Sort by count descending
    bar_data = bar_data.sort_values(by="Count", ascending=False)

    # Plot bar chart
    fig = px.bar(
        bar_data,
        x="Preference",
        y="Count",
        color="Preference",
        title="Preference vs Work Type (Intern, Bar Chart)"
    )
    fig.show()
else:
    print("⚠️ Chart can only be displayed between 3 PM and 5 PM IST.")
