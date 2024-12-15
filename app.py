

""" to do
1. Format homepage ( panels)
2. Format calculator page (panels)
3. Publish on real page
4. License
5. Income model

"""

import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Homepage route
@app.route("/")
def home():
    return render_template("home.html")

# Fluid Dynamics category
@app.route("/fluid-dynamics")
def fluid_dynamics():
    return render_template("fluid_dynamics/overview.html")

@app.route("/fluid-dynamics/reynolds-number", methods=["GET", "POST"])
def reynolds_number():
    result = None
    if request.method == "POST":
        try:
            density = float(request.form["density"])
            velocity = float(request.form["velocity"])
            length = float(request.form["length"])
            viscosity = float(request.form["viscosity"])
            result = (density * velocity * length) / viscosity
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    return render_template("fluid_dynamics/reynolds.html", result=result)

@app.route("/fluid-dynamics/k-epsilon", methods=["GET", "POST"])
def k_epsilon():
    result = None
    if request.method == "POST":
        try:
            u_ref = float(request.form["u_ref"])
            turb_intensity = float(request.form["turb_intensity"]) / 100  # Convert percentage to fraction
            length_scale = float(request.form["length_scale"])
            
            # Calculations
            k = (3 / 2) * (u_ref * turb_intensity) ** 2
            C_mu = 0.09
            epsilon = (C_mu ** (3 / 4)) * (k ** (3 / 2)) / length_scale
            
            result = f"Turbulent kinetic energy (k): {round(k, 4)} m²/s² <br> Dissipation rate (ε): {round(epsilon, 4)} m²/s³"
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    return render_template("fluid_dynamics/k_epsilon.html", result=result)

@app.route("/fluid-dynamics/k-omega", methods=["GET", "POST"])
def k_omega():
    result = None
    if request.method == "POST":
        try:
            u_ref = float(request.form["u_ref"])
            turb_intensity = float(request.form["turb_intensity"]) / 100  # Convert percentage to fraction
            length_scale = float(request.form["length_scale"])
            
            # Calculations
            k = (3 / 2) * (u_ref * turb_intensity) ** 2
            omega = k / (length_scale ** 2)
            
            result = f"Turbulent kinetic energy (k): {round(k, 4)} m²/s² <br> Specific dissipation rate (ω): {round(omega, 4)} s⁻¹"
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    return render_template("fluid_dynamics/k_omega.html", result=result)


# Wave Energy category
@app.route("/wave-energy")
def wave_energy():
    return render_template("wave_energy/overview.html")

@app.route("/wave-energy/wave-energy", methods=["GET", "POST"])
def wave_energy_calculator():
    result = None
    default_density = 1025  # Prefilled water density
    default_gravity = 9.81  # Prefilled acceleration due to gravity
    if request.method == "POST":
        try:
            density = float(request.form.get("density", default_density))
            gravity = float(request.form.get("gravity", default_gravity))
            height = float(request.form["height"])  # H_s: Significant wave height
            # Wave energy calculation
            result = (1/8) * density * gravity * (height ** 2)  # Result in J/m²
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    return render_template("wave_energy/wave_energy.html", result=result, default_density=default_density, default_gravity=default_gravity)


@app.route("/wave-energy/wave-power", methods=["GET", "POST"])
def wave_power():
    result = None
    default_density = 1025  # Prefilled water density
    default_gravity = 9.81  # Prefilled acceleration due to gravity
    if request.method == "POST":
        try:
            density = float(request.form.get("density", default_density))
            gravity = float(request.form.get("gravity", default_gravity))
            period = float(request.form["period"])  # T_e: Energetic wave period
            height = float(request.form["height"])  # H_s: Significant wave height
            import math
            # Wave power calculation in watts (W)
            wave_power_watts = (density * (gravity ** 2) * period * (height ** 2)) / (64 * math.pi)
            # Convert to kilowatts (kW)
            result = wave_power_watts / 1000
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    return render_template("wave_energy/wave_power.html", result=result, default_density=default_density, default_gravity=default_gravity)


@app.route("/wave-energy/another-calculator")
def another_wave_energy_calculator():
    return render_template("wave_energy/another_calculator.html")




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



if __name__ == "__main__":
    app.run(debug=True)
