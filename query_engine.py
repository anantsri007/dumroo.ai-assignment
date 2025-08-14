import pandas as pd
import json
from langchain_google_genai import ChatGoogleGenerativeAI

# ==== CONFIGURATION ====

# Your Gemini API Key (can also be stored in environment variables for security)
GEMINI_API_KEY = "AIzaSyBA61S-IBFPpMTqc2X2y_RTGXzZOLgA3hw"  # <- replace with your actual key

# Load student data
with open("students.json", "r") as f:
    data = json.load(f)
students_df = pd.DataFrame(data)

# Admin access scope
admin_context = {
    "assigned_grades": [8],
    "assigned_classes": ["A"],
    "region": "North"
}

# ==== FUNCTIONS ====

def apply_scope_filter(df, context):
    """Restrict dataset to admin's allowed grade/class/region."""
    return df[
        (df["grade"].isin(context["assigned_grades"])) &
        (df["class"].isin(context["assigned_classes"])) &
        (df["region"] == context["region"])
    ]

def query_to_filter(query, df_columns):
    """Convert a natural language question into a Pandas filter expression using Gemini."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",     # ✅ current working model
        temperature=0,
        google_api_key=GEMINI_API_KEY
    )

    prompt = (
        f"The dataset columns are: {', '.join(df_columns)}.\n"
        f"For the user's query: '{query}',\n"
        "Respond ONLY with a valid pandas DataFrame boolean filter expression as in df.query(). "
        "Example: submission_status == 'not_submitted' and grade == 8\n"
        "Do not include code or explanations."
    )

    response = llm.invoke(prompt)
    return response.content.strip().split("\n")[0]

def process_query(query, df, context):
    """Main function to process a user’s question and return filtered results."""
    filtered_df = apply_scope_filter(df, context)
    try:
        filter_expr = query_to_filter(query, df.columns.tolist())
        return filtered_df.query(filter_expr)
    except Exception as e:
        print(f"Error parsing filter: {e} — returning all scoped rows.")
        return filtered_df
