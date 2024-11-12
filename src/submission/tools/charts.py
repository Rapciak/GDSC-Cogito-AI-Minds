from langchain_core.tools import tool
from typing import Literal
import boto3.session
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Literal
import boto3
import os
import io

@tool('generate_chart')
def generate_chart(chart_type: Literal['scatter','line','bar'], data_json: str, filename: str, x_axis: str, y_axis: str) -> str:
    """
    Generate a Seaborn chart based on input data and save it as an image file.
    
    In bar chart, prioritize passing string column as the y-axis.

    This function creates a chart using Seaborn and matplotlib, based on the specified
    chart type and input data. The resulting chart is saved as an image file.

    Parameters:
    -----------
    chart_type : Literal['scatter', 'line', 'bar']
        The type of chart to generate. Must be one of 'scatter', 'line', or 'bar'.
    data_json : str
        A JSON string containing the data to be plotted. The JSON should be structured
        such that it can be converted into a pandas DataFrame.
    filename : str
        The name of the file (including path if necessary) where the chart image will be saved.
    x_axis : str
        The name of the column in the data to be used for the x-axis.
    y_axis : str
        The name of the column in the data to be used for the y-axis.

    Returns:
    --------
    str
        A message confirming that the chart has been saved, including the filename.

    """

    # Convert JSON input to a pandas DataFrame
    data = json.loads(data_json)
    df = pd.DataFrame(data)

    # Create an array with the colors you want to use
    colors = ["#0070AD", "#12ABDB"]
    
    # Create the Seaborn plot
    plt.figure(figsize=(10, 6))
    if chart_type == "scatter":
        sns.scatterplot(data=df, x=x_axis, y=y_axis)
    elif chart_type == "line":
        sns.lineplot(data=df, x=x_axis, y=y_axis, color=colors[1])
    elif chart_type == "bar":
        sns.barplot(data=df, x=x_axis, y=y_axis, color=colors[1])
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
    
    # Set labels
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    #Rotating Label
    plt.xticks(rotation=90)
    
    # Save the plot to a BytesIO object
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png', dpi=300, bbox_inches='tight')
    plt.close()

    # Reset the pointer of the BytesIO object
    img_data.seek(0)

    # Upload the image to S3
    session = boto3.Session()
    s3 = session.client('s3')
    bucket_name = 'gdsc-bucket-058264136196'
    try:
        s3.upload_fileobj(img_data, bucket_name, filename)
        # Build and return the S3 URL
        s3_url = f'https://{bucket_name}.s3.amazonaws.com/{filename}'
        return s3_url
    except Exception as e:
        return f"An error occurred: {str(e)}"