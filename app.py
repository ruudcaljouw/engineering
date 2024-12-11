from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/calculator/<calc>', methods=['GET', 'POST'])
def calculator(calc):
    # Define calculators with descriptions, inputs, and the calculation logic
    calculators = {
        "k-epsilon": {
            "name": "k-epsilon Calculator",
            "description": "Calculate turbulent kinetic energy (k) and dissipation rate (ε) using the k-epsilon turbulence model.",
            "inputs": [
                {"id": "u_ref", "label": "Reference Velocity (m/s)", "name": "u_ref"},
                {"id": "turb_intensity", "label": "Turbulence Intensity (%)", "name": "turb_intensity"},
                {"id": "length_scale", "label": "Length Scale (m)", "name": "length_scale"},
            ],
            "action_url": "/calculator/k-epsilon",
            "calculation": lambda data: calculate_k_epsilon(data),
        },
        "k-omega": {
            "name": "k-omega Calculator",
            "description": "Compute turbulent kinetic energy (k) and specific dissipation rate (ω) using the k-omega model.",
            "inputs": [
                {"id": "u_ref", "label": "Reference Velocity (m/s)", "name": "u_ref"},
                {"id": "turb_intensity", "label": "Turbulence Intensity (%)", "name": "turb_intensity"},
                {"id": "length_scale", "label": "Length Scale (m)", "name": "length_scale"},
            ],
            "action_url": "/calculator/k-omega",
            "calculation": lambda data: calculate_k_omega(data),
        },
        "reynolds": {
            "name": "Reynolds Number Calculator",
            "description": "Determine the Reynolds number for your flow conditions.",
            "inputs": [
                {"id": "density", "label": "Density (kg/m³)", "name": "density"},
                {"id": "velocity", "label": "Velocity (m/s)", "name": "velocity"},
                {"id": "diameter", "label": "Diameter (m)", "name": "diameter"},
                {"id": "viscosity", "label": "Viscosity (Pa·s)", "name": "viscosity"},
            ],
            "action_url": "/calculator/reynolds",
            "calculation": lambda data: calculate_reynolds(data),
        },
    }

    # Validate the requested calculator
    if calc not in calculators:
        return "Calculator not found", 404

    calculator = calculators[calc]

    if request.method == 'POST':
        # Extract form data
        data = {field["name"]: float(request.form[field["name"]]) for field in calculator["inputs"]}
        # Perform calculation
        result = calculator["calculation"](data)
        return render_template('calculator.html', **calculator, result=result)

    return render_template('calculator.html', **calculator, result=None)


# Calculation Functions
def calculate_k_epsilon(data):
    u_ref = data["u_ref"]
    turb_intensity = data["turb_intensity"] / 100  # Convert percentage to fraction
    length_scale = data["length_scale"]

    # Turbulent kinetic energy (k)
    k = (3 / 2) * (u_ref * turb_intensity) ** 2

    # Dissipation rate (ε)
    C_mu = 0.09
    epsilon = (C_mu ** (3 / 4)) * (k ** (3 / 2)) / length_scale

    return f"Turbulent kinetic energy (k): {round(k, 4)} m²/s² <br> Dissipation rate (ε): {round(epsilon, 4)} m²/s³"


def calculate_k_omega(data):
    u_ref = data["u_ref"]
    turb_intensity = data["turb_intensity"] / 100  # Convert percentage to fraction
    length_scale = data["length_scale"]

    # Turbulent kinetic energy (k)
    k = (3 / 2) * (u_ref * turb_intensity) ** 2

    # Specific dissipation rate (ω)
    omega = k / (length_scale ** 2)

    return f"Turbulent kinetic energy (k): {round(k, 4)} m²/s² <br> Specific dissipation rate (ω): {round(omega, 4)} s⁻¹"


def calculate_reynolds(data):
    density = data["density"]
    velocity = data["velocity"]
    diameter = data["diameter"]
    viscosity = data["viscosity"]

    # Reynolds number
    reynolds_number = (density * velocity * diameter) / viscosity

    return f"Reynolds number: {round(reynolds_number, 4)}"


@app.route('/update_hook', methods=['POST'])
def update_code():
    """
    Webhook endpoint for GitHub. Pulls the latest code when triggered.
    """
    # Verify the request (optional but recommended)
    secret = "testing"  # Use the same secret you set in the webhook
    if not request.headers.get('X-Hub-Signature-256'):
        return "Unauthorized", 403

    # Run the update script
    os.system("/home/roadrunner38/update_engineering_app.sh")
    return "Code updated", 200


if __name__ == '__main__':
    app.run(debug=True)
