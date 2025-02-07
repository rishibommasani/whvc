import pandas as pd
import plotly.graph_objects as go

# Create custom colorscale from the provided colors
colors = ['#DAD7CD', '#A3B18A', '#588157', '#3A5A40', '#344E41']
custom_colorscale = [[i/(len(colors)-1), color] for i, color in enumerate(colors)]

df = pd.read_csv('../data/aggregate.csv', index_col=0)
df.drop(columns=['Average'], inplace=True)
df = df * 100

# Calculate averages
column_avg = df.mean()
row_avg = df.mean(axis=1)

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    z=df.values,
    x=df.columns,
    y=df.index,
    text=[[f'{val:.0f}%' for val in row] for row in df.values],
    texttemplate='%{text}',
    textfont={'size': 10},
    colorscale=custom_colorscale,  # Use custom colorscale
    zmin=0,
    zmax=100,
    showscale=False,  # Hide the color scale
    xgap=1,  # Add 1 pixel gap between columns
    ygap=1,  # Add 1 pixel gap between rows
))

# Add row averages on the right
for i, (idx, avg) in enumerate(row_avg.items()):
    # Add white rectangle
    fig.add_shape(
        type='rect',
        x0=len(df.columns)-0.5,
        y0=i-0.5,
        x1=len(df.columns)+0.5,
        y1=i+0.5,
        fillcolor='white',
        line=dict(width=0),
    )
    
    # Add average score annotation
    fig.add_annotation(
        x=len(df.columns),
        y=i,
        text=f'{avg:.0f}%',
        showarrow=False,
        font=dict(
            size=10,
            color="black"
        ),
    )

# Add column averages at the bottom
for i, avg in enumerate(column_avg):
    # Add white rectangle
    fig.add_shape(
        type='rect',
        x0=i-0.5,
        y0=len(df.index)-0.5,
        x1=i+0.5,
        y1=len(df.index)+0.5,
        fillcolor='white',
        line=dict(width=0),
    )
    
    # Add average score annotation
    fig.add_annotation(
        x=i,
        y=len(df.index),
        text=f'{avg:.0f}%',
        showarrow=False,
        font=dict(
            size=10,
            color="black"
        ),
    )

# Calculate and add the overall average in the bottom-right corner
overall_avg = df.values.mean()
fig.add_shape(
    type='rect',
    x0=len(df.columns)-0.5,
    y0=len(df.index)-0.5,
    x1=len(df.columns)+0.5,
    y1=len(df.index)+0.5,
    fillcolor='white',
    line=dict(width=0),
)
fig.add_annotation(
    x=len(df.columns),
    y=len(df.index),
    text=f'{overall_avg:.0f}%',
    showarrow=False,
    font=dict(
        size=10,
        color="black"
    ),
)

# Update layout
fig.update_layout(
    title={
        'text': 'AI Company Voluntary Commitments',
        'x': 0.5,
        'y': 0.98,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='',
    yaxis_title='',
    width=1470,
    height=350,
    xaxis={
        'side': 'top',
        'range': [-0.5, len(df.columns) + 0.5],
        'ticktext': list(df.columns) + ['Average'],
        'tickvals': list(range(len(df.columns))) + [len(df.columns)],
        'constrain': 'domain',
        'tickangle': 0  # Make labels horizontal
    },
    yaxis={
        'autorange': 'reversed',
        'range': [len(df.index) - 0.5, -0.5],
        'scaleanchor': 'x',
        'scaleratio': 0.4,
        'tickmode': 'array',
        'ticktext': df.index,
        'tickvals': list(range(len(df.index))),
    },
    margin=dict(t=80, r=50, b=50, l=250)  # Increased top margin and left margin
)

# Update font sizes
fig.update_layout(
    font=dict(size=12),
    xaxis=dict(tickfont=dict(size=10)),
    yaxis=dict(tickfont=dict(size=10))
)

# Show figure
fig.show()