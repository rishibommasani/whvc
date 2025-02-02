import pandas as pd
import numpy as np
import sys
import plotly.graph_objects as go
from PIL import Image

# Read data
df = pd.read_csv('raw.csv')
# print(df)

GRAY_COLOR = '#E6E6E6'
MAIN_COLOR = '#588157'

# Calculate scores
max_possible_per_row = 1
total_possible = len(df) * max_possible_per_row
company_scores = df.iloc[:, 2:].sum() * 100 / total_possible
print(company_scores)
company_scores = company_scores.round().astype(int)

# Transform to a DataFrame with columns 'Model' and 'Total'
df_transformed = company_scores.to_frame().reset_index()
df_transformed.columns = ['Model', 'Total']

# Add a column with 100
df_transformed['Other'] = 100

# Reshape the data
df = df_transformed.melt(id_vars=['Model'], value_vars=['Total', 'Other'], var_name='Type', value_name='Score')

# Set 'Model' column as the index and sort values
df.set_index('Model', inplace=True)
if 'Total' in df.Type.unique():
    df = df.sort_values(by=['Type', 'Score', 'Model'], ascending=[False, True, False])

# Create ranking
if 'Total' in df.Type.unique():
    rank = df[df.Type == 'Total']['Score'].rank(method='dense', ascending=False).astype(int).tolist()

print(df)
# Define Y and X for generating a bar chart
X = df[df.Type == 'Other']['Score']
Y = df[df.Type == 'Total'].index

# Generate bar chart
fig = go.Figure()

# Constants for circle dimensions and position
circle_radius = 0.17
circle_width_stretch = 10
end_offset = 0
begin_offset = 0

# Add base bars (gray background)
fig.add_trace(go.Bar(
    x=X,
    y=Y,
    orientation='h',
    marker_color=GRAY_COLOR,
    width=0.4,
    showlegend=False
))

# Add rounded ends to gray bars
color = GRAY_COLOR
for i, yi in enumerate(X):
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=yi - (circle_radius * circle_width_stretch) + end_offset,
        y0=i - circle_radius,
        x1=yi + (circle_radius * circle_width_stretch) + end_offset,
        y1=i + circle_radius,
        line=dict(color=color, width=2),
        fillcolor=color,
    )

x = df[df.Type == 'Total']['Score']
COLORS = ['#DAD7CD', '#A3B18A', '#588157', '#3A5A40', '#344E41']
HIGHLIGHT_COLOR = COLORS[4]  # Using the middle green color for highlighted companies
REGULAR_COLOR = COLORS[1]  # Original color for non-highlighted companies

# Add at the top with other imports and constants
HIGHLIGHT_COMPANIES = ['Amazon', 'Anthropic', 'Google', 'Meta', 'OpenAI', 'Microsoft']
HIGHLIGHT_MODE = True  # Toggle this to turn highlighting on/off

# Replace the score bars trace (around line 95) with this:
fig.add_trace(go.Bar(
    x=x,
    y=Y,
    orientation='h',
    marker_color=[
        HIGHLIGHT_COLOR if HIGHLIGHT_MODE and company in HIGHLIGHT_COMPANIES 
        else REGULAR_COLOR 
        for company in Y
    ],
    width=0.4,
    showlegend=False,
    textposition='outside',
    textfont=dict(
        family="CircularStd-Book",
        size=14,
        color=MAIN_COLOR
    )
))

color = MAIN_COLOR
circle_radius = 0.15  # Slightly smaller for the purple bars
# Update the rounded ends code section (around line 115) with this:
for i, (yi, company) in enumerate(zip(x, Y)):
    color = HIGHLIGHT_COLOR if HIGHLIGHT_MODE and company in HIGHLIGHT_COMPANIES else REGULAR_COLOR
    
    # Add circle at the end of each bar
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=yi - (circle_radius * circle_width_stretch) + end_offset,
        y0=i - circle_radius,
        x1=yi + (circle_radius * circle_width_stretch) + end_offset,
        y1=i + circle_radius,
        line=dict(color=color, width=2),
        fillcolor=color,
    )
    
    # Add circle at the beginning of each bar
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=0 - (circle_radius * circle_width_stretch) + begin_offset,
        y0=i - circle_radius,
        x1=0 + (circle_radius * circle_width_stretch) + begin_offset,
        y1=i + circle_radius,
        line=dict(color=color, width=2),
        fillcolor=color,
    )

# Add annotations for scores
for i, (x_val, y_val) in enumerate(zip(x, Y)):
    fig.add_annotation(
        x=110,
        y=y_val,
        text=f'{x_val: .0f}%',
        showarrow=False,
        font=dict(
            family="CircularStd-Book",
            size=16,
            color=MAIN_COLOR
        ),
        xref="x",
        yref="y",
        align="left"
    )

# Add model names
Y_model_name = Y.tolist()
for i, (x_val, y_val) in enumerate(zip(Y_model_name, Y)):
    fig.add_annotation(
        x=-50,
        y=y_val,
        text=f'{x_val}',
        showarrow=False,
        font=dict(
            family="CircularStd-Book",
            size=16,
            color="black"
        ),
        xref="x",
        yref="y",
        xanchor="left",
        align="left"
    )

# Add headers
fig.add_annotation(
    x=109,
    y=16,
    text="Score",
    showarrow=False,
    font=dict(
        family="CircularStd-Bold",
        size=16,
        color="black"
    ),
    xref="x",
    yref="y",
    align="center"
)

fig.add_annotation(
    x=-33,
    y=16,
    text="Company",
    showarrow=False,
    font=dict(
        family="CircularStd-Bold",
        size=16,
        color="black"
    ),
    xref="x",
    yref="y",
    align="center"
)

# Add legend bars
legend_y_position = -2  # Adjust this value to position the legend lower/higher

# Add non-member legend bar
fig.add_trace(go.Bar(
    x=[20],  # Position the legend bar
    y=[legend_y_position],
    orientation='h',
    marker_color=REGULAR_COLOR,
    width=0.4,
    showlegend=False,
    name='Non-member'
))

# Add rounded ends for non-member legend bar
for end in [0]:  # Start and end positions
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=end - (circle_radius * circle_width_stretch),
        y0=legend_y_position - circle_radius,
        x1=end + (circle_radius * circle_width_stretch),
        y1=legend_y_position + circle_radius,
        line=dict(color=REGULAR_COLOR, width=2),
        fillcolor=REGULAR_COLOR,
    )

# Add FMF member legend bar
fig.add_trace(go.Bar(
    x=[20],
    y=[legend_y_position - 1],  # Position below the first legend bar
    orientation='h',
    marker_color=HIGHLIGHT_COLOR,
    width=0.4,
    showlegend=False,
    name='Frontier Model Forum Member'
))

# Add rounded ends for FMF member legend bar
for end in [0]:  # Start and end positions
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=end - (circle_radius * circle_width_stretch),
        y0=(legend_y_position - 1) - circle_radius,
        x1=end + (circle_radius * circle_width_stretch),
        y1=(legend_y_position - 1) + circle_radius,
        line=dict(color=HIGHLIGHT_COLOR, width=2),
        fillcolor=HIGHLIGHT_COLOR,
    )

# Add legend text annotations
fig.add_annotation(
    x=25,
    y=legend_y_position,
    text="Non-member",
    showarrow=False,
    font=dict(
        family="CircularStd-Book",
        size=14,
        color="black"
    ),
    xref="x",
    yref="y",
    align="left"
)

fig.add_annotation(
    x=25,
    y=legend_y_position - 1,
    text="FMF member",
    showarrow=False,
    font=dict(
        family="CircularStd-Book",
        size=14,
        color="black"
    ),
    xref="x",
    yref="y",
    align="left"
)

# Update layout
fig.update_layout(
    barmode='overlay',
    margin=dict(l=100, t=80, b=100, r=155),
    xaxis_range=[-90, 110.5],
    xaxis_dtick=10,
    height=620,
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis_range=[legend_y_position - 2, len(Y) - 0.5],  # Extend y-axis range to show legend
)

# Remove axis labels and grid
fig.update_yaxes(showticklabels=False, showgrid=False, showline=False)
fig.update_xaxes(showgrid=False, showline=False, ticks="", showticklabels=False)

# Add source annotation
fig.add_annotation(
    text="Source: White House Voluntary Commitments Tracking",
    xref="paper",
    yref="paper",
    x=0.20,
    y=1.08,
    showarrow=False,
    font=dict(
        family="CircularStd-Book",
        size=12,
        color="black"
    ),
    align="center"
)

# Export the plot
fig.write_image("voluntary_commitments_scores.pdf", scale=2/1)

# Export data to CSV
df[df.Type == 'Total'].reset_index()[['Model', 'Score']].to_csv('voluntary_commitments_scores.csv', index=False)