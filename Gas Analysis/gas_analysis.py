def analyze_gas(gas_levels):
    predictions = {}
    for gas, level in gas_levels.items():
        if level > 100:
            predictions[gas] = "High levels detected, immediate action required."
        elif level > 50:
            predictions[gas] = "Moderate levels detected, monitor closely."
        else:
            predictions[gas] = "Levels are within safe limits."
    return predictions
