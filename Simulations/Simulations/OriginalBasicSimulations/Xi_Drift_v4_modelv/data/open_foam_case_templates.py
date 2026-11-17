# Recreate OpenFOAM case templates after state reset

openfoam_case_templates = {
    "system/controlDict": """
application     scalarTransportFoam;

startFrom       latestTime;
startTime       0;
stopAt          endTime;
endTime         1;
deltaT          1;

writeControl    timeStep;
writeInterval   1;
purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;
timeFormat      general;
timePrecision   6;
""",
    "system/fvSchemes": """
ddtSchemes
{
    default         Euler;
}

divSchemes
{
    default         none;
    div(phi,U)      Gauss upwind;
    div(phi,scalar) Gauss upwind;
}

laplacianSchemes
{
    default         Gauss linear corrected;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         corrected;
}
""",
    "system/fvSolution": """
solvers
{
    "(.*)"
    {
        solver          PCG;
        preconditioner  DIC;
        tolerance       1e-06;
        relTol          0.1;
    }
}

SIMPLE
{
    nNonOrthogonalCorrectors 0;
}

relaxationFactors
{
    fields
    {
        "(.*)" 1.0;
    }
    equations
    {
        "(.*)" 1.0;
    }
}
""",
    "constant/transportProperties": """
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "constant";
    object      transportProperties;
}

DT      DT [0 2 -1 0 0 0 0] 0.01;
""",
    "constant/thermophysicalProperties": """
thermoType
{
    type            heRhoThermo;
    mixture         pureMixture;
    transport       const;
    thermo          hConst;
    equationOfState rhoConst;
    specie          specie;
    energy          sensibleInternalEnergy;
}

mixture
{
    specie
    {
        nMoles          1;
        molWeight       28.9;
    }
    thermodynamics
    {
        Cp              1000;
        Hf              0;
    }
    transport
    {
        mu              1e-05;
        Pr              0.7;
    }
}
"""
}

import os

# Create OpenFOAM case directory and write templates
openfoam_case_root = "/mnt/data/openfoam_case_templates"
os.makedirs(openfoam_case_root, exist_ok=True)

for relative_path, content in openfoam_case_templates.items():
    full_path = os.path.join(openfoam_case_root, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip())

openfoam_case_root
