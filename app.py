from flask import Flask, render_template

app = Flask(__name__)
from flask import Flask, render_template
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Flask(__name__)


@app.route("/")
def home():
    # Generate a Plotly figure
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Chart 1", "Chart 2"])

    # Add sample traces to the figure
    fig.add_trace(
        go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode="lines", name="Line Chart"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(x=["A", "B", "C"], y=[10, 20, 15], name="Bar Chart"), row=1, col=2
    )

    # Convert the figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Render the HTML template with the Plotly figure
    return render_template("index.html", plot_html=plot_html)


if __name__ == "__main__":
    app.run(debug=True)
