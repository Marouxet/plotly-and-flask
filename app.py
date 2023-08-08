from flask import Flask, render_template
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route("/")
def home_test():
  


    # Grafico 1 - Scatter usando Plotly Express
    # Referencia: https://plotly.com/python/line-and-scatter/

    # iris is a pandas DataFrame
    df = px.data.iris() 
    # Build the figure
    fig1 = px.scatter(df, x="sepal_width", y="sepal_length") 
    # Convert it as JSON using PlotlyJSONEncoder
    graph1JSON = json.dumps(fig1, cls=PlotlyJSONEncoder) 



    # Gráfico 2 - con menus desplegables usando Plotly Graph Objects (go)
    # Referencia: https://plotly.com/python/dropdowns/
    # load dataset
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv")
    # create figure
    fig2 = go.Figure()

    # Add surface trace
    fig2.add_trace(go.Surface(z=df.values.tolist(), colorscale="Viridis"))

    # Update plot sizing
    fig2.update_layout(
        width=800,
        height=900,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        template="plotly_white",
    )

    # Update 3D scene options
    fig2.update_scenes(
        aspectratio=dict(x=1, y=1, z=0.7),
        aspectmode="manual"
    )

    # Add dropdown
    fig2.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["type", "surface"],
                        label="3D Surface",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "heatmap"],
                        label="Heatmap",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    # Add annotation
    fig2.update_layout(
        annotations=[
            dict(text="Trace type:", showarrow=False,
            x=0, y=1.085, yref="paper", align="left")
        ]
    )

    # Convertir a json
    graph2JSON = json.dumps(fig2, cls=PlotlyJSONEncoder) 


    # Grafico 3 - Un grafico customizado hecho para Clustering que ya guardamos como Json y sólamente leemos el archivo JSON 
    # Esto puede ser bueno para hacer la construcción del gráfico previa a que se cargue el sitio web

    with open('pre_drawn_plotly_chart.json', 'r') as f:
        graph3JSON = json.load(f)

   # En el return de la función usamos render_template y pasamos los objetos json como argumentos.
    return render_template(
                "layout.html", 
                title = "Testing plotly on Flask", 
                graph1JSON = graph1JSON,
                graph2JSON = graph2JSON,
                graph3JSON = graph3JSON
    )


if __name__ == "__main__":
    app.run()