import plotly.express as px

def create_chart(history):
    history = history[["rate"]].reset_index(drop=True)
    history["day"] = history.index + 1
    chart = px.line(
        history,
        x='day',
        y='rate',
        title="Курс EUR",
        labels ={"day": "Відкритий день", "rate": "Курс (грн)"},
        markers=True,
    )
    chart.update_traces(line_color="#76ff03")
    chart.update_layout(template="plotly_dark")
    chart.update_xaxes(dtick=1)
    return chart
