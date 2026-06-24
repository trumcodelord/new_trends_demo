import streamlit as st
import pandas as pd
from .dataset_metrics import render_dataset_metrics
from .source_topic_distribution import render_source_topic_distribution
from .source_topic_heatmap import render_source_topic_heatmap
from .article_timeline_plot import render_article_timeline_plot

def render_dataset_overview(article_df: pd.DataFrame, metrics):
    render_dataset_metrics(article_df, metrics)
    render_source_topic_distribution(article_df, metrics)
    render_source_topic_heatmap(article_df)
    render_article_timeline_plot(article_df)
    


