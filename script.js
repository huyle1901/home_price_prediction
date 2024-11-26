console.log("Script is running!"); 

async function loadLocations() {
    try {
        console.log("Fetching locations...");

        const response = await fetch("http://127.0.0.1:8000/locations");
        console.log("Fetch response:", response);

        if (!response.ok) {
            throw new Error(`Failed to fetch locations: ${response.status}`);
        }

        const data = await response.json();
        console.log("Locations data received:", data);

        const locationSelect = document.getElementById("location");
        locationSelect.innerHTML = "";

        
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Select a location";
        locationSelect.appendChild(defaultOption);

        // Add options From API
        data.locations.forEach(location => {
            const option = document.createElement("option");
            option.value = location;
            option.textContent = location;
            locationSelect.appendChild(option);
        });

        console.log("Locations added to dropdown successfully!");
    } catch (error) {
        console.error("Error loading locations:", error);
    }
}


document.getElementById("predictForm").addEventListener("submit", async function (event) {
    event.preventDefault(); 

   
    const location = document.getElementById("location").value;
    const sqft = parseFloat(document.getElementById("sqft").value);
    const bath = parseInt(document.getElementById("bath").value);
    const bhk = parseInt(document.getElementById("bhk").value);

    console.log("Form submitted with data:", { location, sqft, bath, bhk });

    try {
        // Send request to API /predict
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ location, sqft, bath, bhk })
        });

        console.log("Predict response:", response);

        if (!response.ok) {
            throw new Error(`Prediction failed: ${response.status}`);
        }

        const result = await response.json();
        console.log("Prediction result received:", result);

        // Display the result
        document.getElementById("result").textContent = `${result.predicted_price.toFixed(2)}`;
    } catch (error) {
        console.error("Error predicting price:", error);
        document.getElementById("result").textContent = "Error predicting price.";
    }
});


loadLocations();