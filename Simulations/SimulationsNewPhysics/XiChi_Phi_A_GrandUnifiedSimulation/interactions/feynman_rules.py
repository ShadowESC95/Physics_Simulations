# interactions/feynman_rules.py

def feynman_propagators():
    """
    Returns simplified symbolic propagators for fields.
    """
    return {
        "Ξ": "i / (k² - m_Ξ² + iε)",
        "χ": "i / (k² - m_χ² + iε)",
        "φ": "i / (k² - m_φ² + iε)",
        "Aμ": "-i η_{μν} / (k² - m_A² + iε)",
        "Gμν": "i P_{μν,αβ}(k) / (k² - m_G² + iε)"
    }

def feynman_vertices():
    """
    Returns simplified symbolic vertex factors.
    """
    return {
        "Ξχχ": "-i λ_χ",
        "ΞR": "-i λ_R",
        "φAμ": "i m (p_μ - k_μ)",
        "AμAνΞ": "-i g_{μν} Ξ",
        "χχχχ": "-i λ_χ⁴",
        "Aμχχ": "-i e χ ∂μχ",
    }

def list_rules():
    return {
        "propagators": feynman_propagators(),
        "vertices": feynman_vertices()
    }

