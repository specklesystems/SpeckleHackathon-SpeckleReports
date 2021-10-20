TYPE_MATERIAL_MAPPING = {
    "Objects.BuiltElements.Beam:Objects.BuiltElements.Revit.RevitBeam": "Concrete",
    "Objects.BuiltElements.Ceiling:Objects.BuiltElements.Revit.RevitCeiling": "Concrete",
    "Objects.BuiltElements.Column:Objects.BuiltElements.Revit.RevitColumn": "Concrete",
    "Objects.BuiltElements.Floor:Objects.BuiltElements.Revit.RevitFloor": "Concrete",
    "Objects.BuiltElements.Revit.RevitRailing": "Steel",
    "Objects.BuiltElements.Roof:Objects.BuiltElements.Revit.RevitRoof.RevitRoof:Objects.BuiltElements.Revit.RevitRoof.RevitExtrusionRoof": "Steel",
    "Objects.BuiltElements.Roof:Objects.BuiltElements.Revit.RevitRoof.RevitRoof:Objects.BuiltElements.Revit.RevitRoof.RevitFootprintRoof": "Timber",
    "Objects.BuiltElements.Wall:Objects.BuiltElements.Revit.RevitWall": "Timber",
    "Objects.BuiltElements.Revit.FamilyInstance": {
        "Windows": "Glass",
        "Furniture": "Timber",
        "Other": "Concrete",
    },
    "Objects.BuiltElements.Revit.RevitStair": "Concrete",
}


MATERIAL_PROPERTIES = {
    "Aluminium": {"density": 2700, "kgCO2e": 9.16},
    "Concrete": {"density": 2400, "kgCO2e": 0.12},
    "Steel": {"density": 7800, "kgCO2e": 1.46},
    "Timber": {"density": 650, "kgCO2e": 0.72},
    "Glass": {"density": 2500, "kgCO2e": 0.91},
}
