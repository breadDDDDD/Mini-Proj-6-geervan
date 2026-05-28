# Student Handout

You are building a Mitsubishi after-sales service assistant.

Your assistant must:

- Answer questions in Bahasa Indonesia or English.
- Use local documents as evidence.
- Return sources.
- Refuse unsafe, off-topic, or prompt-injection queries.
- Log requests.
- Evaluate quality and safety.
- Compare one A/B variant.
- Explain cost and scaling.
- Test the chatbot interactively using Streamlit UI.

## What You Submit

One ZIP file:

```text
mini-project-6-{your-name}.zip
```

Contents:

```text
src/
README.md
eval_report.pdf or eval_report.md
dashboard.png or dashboard.md
architecture.png or architecture.md
cost_analysis.pdf or cost_analysis.md
```

## Recommended Workflow

1. Make a weak baseline work.
2. Add logs.
3. Add evaluation.
4. Improve only one variable.
5. Create cost and demo story.

## Interactive UI

Terminal 1:

```bash
uvicorn src.main:app --reload
```

Terminal 2:

```bash
python -m streamlit run ui/streamlit_app.py
```

Open:

```text
http://localhost:8501
```
