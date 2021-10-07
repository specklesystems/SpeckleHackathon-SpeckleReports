from collections import defaultdict
from specklepy.objects import Base
from typing import Dict, List
from itertools import chain

from speckle_calculator.core.carbon_repo import (
    TYPE_MATERIAL_MAPPING,
    MATERIAL_PROPERTIES,
)


class CarbonDataPoint(Base):
    """Data for carbon data repr"""

    parent_id: str
    volume: float
    carbon: float


class CarbonData(Base):
    """Data for carbon data repr"""

    commitId: str
    results: Dict[str, List[CarbonDataPoint]]


def calculate_carbon(commit: Base) -> CarbonDataPoint:
    """It does the magic."""

    results = defaultdict(list)

    nested_categories = [
        getattr(commit, attr_name) for attr_name in commit.get_dynamic_member_names()
    ]
    objects = list(chain(*nested_categories))

    for object in objects:
        if parameters := getattr(object, "parameters", None):
            if volume := getattr(parameters, "HOST_VOLUME_COMPUTED", None):
                if material := TYPE_MATERIAL_MAPPING.get(object.speckle_type):
                    if material_props := MATERIAL_PROPERTIES.get(material):
                        density = material_props["density"]
                        co_value = material_props["kgCO2e"]
                        co2_value = volume.value * density * co_value
                        data_point = CarbonDataPoint(
                            parent_id=object.id,
                            volume=volume.value,
                            carbon=co2_value,
                        )
                        results[material].append(data_point)

    carbon_data = CarbonData(
        commitId="fb25cae6af",
        results=results,
    )

    return carbon_data
