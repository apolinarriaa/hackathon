import plotly.express as px

def create_chart(history):
    chart = px.line(
        history,
        x='date',
        y='rate',
        title="Курс USD",
        labels ={"date": "Дата", "rate": "Курс (грн)"},
        markers=True,
    )
    chart.update_traces(line_color="#00ff66")
    chart.update_layout(line_color="plotly_dark")
    return chart
