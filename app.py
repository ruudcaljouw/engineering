from flask import Flask, render_template, request

app = Flask(__name__)

# Homepage route
@app.route("/")
def home():
    return render_template("base.html")  # Render the base template for the homepage

# Fluid Dynamics calculators page route
@app.route("/fluid-dynamics")
def fluid_dynamics():
    return render_template("fluid_dynamics.html")  # Render the Fluid Dynamics page

# Reynolds Number Calculator page route
@app.route("/fluid-dynamics/reynolds-number", methods=["GET", "POST"])
def reynolds_number():
    result = None
    if request.method == "POST":
        try:
            # Retrieve inputs
            density = float(request.form["density"])  # ρ: Fluid density
            velocity = float(request.form["velocity"])  # v: Fluid velocity
            length = float(request.form["length"])  # L: Characteristic length
            viscosity = float(request.form["viscosity"])  # μ: Dynamic viscosity

            # Perform Reynolds number calculation
            result = (density * velocity * length) / viscosity
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    return render_template("reynolds_number.html", result=result)


# Wave Energy calculators page route
@app.route("/wave-energy")
def wave_energy():
    return render_template("wave_energy.html")  # Render the Wave Energy page

# Ocean Wave Energy Calculator page route
@app.route("/wave-energy/ocean-wave-energy", methods=["GET", "POST"])
def ocean_wave_energy():
    result = None
    if request.method == "POST":
        try:
            # Retrieve inputs
            density = float(request.form["density"])  # ρ: Density of seawater
            wave_height = float(request.form["wave_height"])  # H: Wave height
            
            # Perform the energy calculation
            g = 9.8  # Acceleration due to gravity (m/s²)
            result = (1/8) * density * g * wave_height**2
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    return render_template("ocean_wave_energy.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
