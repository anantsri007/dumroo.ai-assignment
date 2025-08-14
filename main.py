from query_engine import students_df, admin_context, process_query

if __name__ == "__main__":
    print("=== Dumroo Admin NL Query Tool (Gemini) ===")
    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        results = process_query(query, students_df, admin_context)
        print(results.to_string(index=False))
