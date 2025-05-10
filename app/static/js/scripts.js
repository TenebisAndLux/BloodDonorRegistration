const nameInput = document.getElementById("name");
const bloodTypeInput = document.getElementById("bloodType");
const donorsList = document.getElementById("donors");

async function getDonors() {
    try {
        const response = await fetch('http://127.0.0.1:3000/donors');
        const data = await response.json();

        donorsList.innerHTML = "";
        Object.values(data.donors).forEach(donor => {
            const donorItem = document.createElement("li");
            donorItem.textContent = `${donor.name} - ${donor.blood_type}`;
            donorsList.appendChild(donorItem);
        });
    } catch (error) {
        alert(error);
    }
}

getDonors();

