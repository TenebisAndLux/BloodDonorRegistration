const nameInput = document.getElementById("name");
const bloodTypeInput = document.getElementById("bloodType");
const donorsList = document.getElementById("donors");

function addDonor() {
    const name = nameInput.value;
    const bloodType = bloodTypeInput.value;

    if (name && bloodType) {
        fetch('http://127.0.0.1:3000/api/donors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, blood_type: bloodType }),
        })
        .then(response => response.json())
        .then(data => {
            alert("Donor added successfully.");
            getDonors();
        })
        .catch(error => alert(error));
    } else {
        alert("Please enter both name and blood type.");
    }
}

function getDonors() {
    fetch('http://127.0.0.1:3000/api/donors')
    .then(response => response.json())
    .then(data => {
        donorsList.innerHTML = "";
        data.donors.forEach(donor => {
            const donorItem = document.createElement("li");
            donorItem.textContent = `${donor.name} - ${donor.blood_type}`;
            donorsList.appendChild(donorItem);
        });
    })
    .catch(error => alert(error));
}

getDonors();
