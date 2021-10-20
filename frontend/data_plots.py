import os

import pandas as pd
import plotly.express as px
from specklepy.api.operations import receive
from specklepy.api.credentials import StreamWrapper

from devtools import debug
from specklepy.objects.base import Base


def get_report_commit(url_path: str) -> Base:
    url = os.environ.get("SPECKLE_SERVER_URL") + url_path
    wrap = StreamWrapper(url)
    client = wrap.get_client()
    client.authenticate(os.environ.get("SPECKLE_TOKEN"))

    commit = client.commit.get(wrap.stream_id, wrap.commit_id)
    return receive(commit.referencedObject, wrap.get_transport())


def create_plots(url_path: str):
    try:
        data = get_report_commit(url_path)
        results = data.results
    except Exception:
        return

    figures = {}

    df = pd.DataFrame.from_dict(results)

    other = df.groupby("level").sum().sort_values("carbon", ascending=False).index[23:]
    df_merged = df.replace(other, "Other")

    figures["volume-pie-level"] = px.pie(
        df_merged,
        values="volume",
        names="level",
        color="level",
        title="Volume by Level (m3)",
    )

    figures["carbon-pie-level"] = px.pie(
        df_merged,
        values="carbon",
        names="level",
        color="level",
        title="Carbon by Level (kgCO2e)",
    )

    figures["carbon-bar-level"] = px.bar(
        df_merged,
        x="level",
        y="carbon",
        color="level",
        title="Embodied Carbon by Level (kgCO2e)",
    )

    figures["carbon-pie-material"] = px.pie(
        df,
        values="carbon",
        names="material",
        color="material",
        title="Embodied Carbon By Material (kgCO2e)",
    )

    figures["carbon-pie-category"] = px.pie(
        df,
        values="carbon",
        names="category",
        color="category",
        title="Embodied Carbon by Category (kgCO2e)",
    )

    figures["carbon-bar-category"] = px.bar(
        df,
        x="category",
        y="carbon",
        color="category",
        title="Embodied Carbon by Category (kgCO2e)",
    )

    figures["volume-pie-material"] = px.pie(
        df,
        values="volume",
        names="material",
        color="material",
        title="Volume by Material (m3)",
    )
    figures["volume-pie-category"] = px.pie(
        df,
        values="volume",
        names="category",
        color="category",
        title="Volume by Category (m3)",
    )

    figures["volume-bar-category"] = px.bar(
        df,
        x="category",
        y="volume",
        color="category",
        title="Volume by Category (m3)",
    )

    return figures
