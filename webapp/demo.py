#!/usr/bin/env python3

"""
Create a gradio web application that takes a single text box.
The text input contains a source sentence, target sentence, and a sequence of word alignment points of the form x-y, where x is a word index in the source sentence and y is a word index in the target sentence (0-indexed). It will then create an HTML table,
where the source words are columns and the target words are rows, and the alignment points are marked with an X.
"""

import gradio as gr
import numpy as np

import pandas as pd

def align(text):
    source, target, alignment = text.split(" ||| ")
    source_words = source.split()
    target_words = target.split()
    alignment = [tuple(map(int, point.split("-"))) for point in alignment.split()]
    data = [["X" if (i, j) in alignment else "" for j in range(len(source_words))] for i, target_word in enumerate(target_words)]
    df = pd.DataFrame(data, columns=source_words, index=target_words)
    return df.to_html(classes="table table-condensed table-bordered table-hover")

iface = gr.Interface(fn=align, inputs="textbox", outputs="html")
iface.launch()
