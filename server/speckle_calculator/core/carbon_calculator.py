from specklepy.objects import Base
from typing import Dict, List

from speckle_calculator.core.carbon_repo import (
    TYPE_MATERIAL_MAPPING,
    MATERIAL_PROPERTIES,
)


class CarbonData(Base, chunkable={"results": 500}):
    """Data for carbon data repr"""

    commitId: str
    results: List


def create_carbon_datapoints(objects: List[Base], category: str) -> List[Dict]:
    results = []
    for obj in objects:
        if parameters := getattr(obj, "parameters", None):
            if volume := getattr(parameters, "HOST_VOLUME_COMPUTED", None):
                if material := TYPE_MATERIAL_MAPPING.get(obj.speckle_type):
                    if isinstance(material, dict):
                        material = material.get(category, "Concrete")

                    if material_props := MATERIAL_PROPERTIES.get(material):
                        density = material_props["density"]
                        co_value = material_props["kgCO2e"]
                        co2_value = volume.value * density * co_value
                        results.append(
                            {
                                "parent_id": obj.id,
                                "volume": volume.value,
                                "carbon": co2_value,
                                "material": material,
                                "category": category,
                                "level": obj.level.name
                                if getattr(obj, "level", None)
                                else "N/A",
                            }
                        )

    return results


def calculate_carbon(commit: Base) -> CarbonData:
    """It does the magic."""

    results = []
    for category in commit.get_dynamic_member_names():
        results.extend(create_carbon_datapoints(commit[category], category.lstrip("@")))

    return CarbonData(
        commitId=commit.id,
        results=results,
    )
