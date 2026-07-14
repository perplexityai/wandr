"""Re-export shim for fda_drug_lineage_relaxed.

`MoleculeDiscovererJudgment` lives subtask-local at
`drug_molecules/molecule_discoverers/schemas/judgment.py` per the suite-wide
schema-locality convention. The other three classes are reused unchanged from the
sibling strict task (FDA approval check, drug-molecule mapping, PhD institution).
"""

from fda_drug_lineage.schemas.judgment import (
    FDAApprovalJudgment,
)
from fda_drug_lineage.drug_molecules.schemas.judgment import (
    DrugMoleculeJudgment,
)
from fda_drug_lineage.drug_molecules.molecule_sole_discoverers.scientist_phds.schemas.judgment import (
    ScientistPhDJudgment,
)
from drug_molecules.molecule_discoverers.schemas.judgment import (
    MoleculeDiscovererJudgment,
)

__all__ = [
    "DrugMoleculeJudgment",
    "FDAApprovalJudgment",
    "MoleculeDiscovererJudgment",
    "ScientistPhDJudgment",
]
