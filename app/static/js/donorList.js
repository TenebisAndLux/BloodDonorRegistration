let selectedRow;

function getDonors() {
    fetch('/donor/list/get')
        .then(response => response.json())
        .then(donors => {
            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = '';
            for (const donor of donors) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${donor.id}</td>
                    <td>${donor.hospital_affiliation}</td>
                    <td>${donor.first_name} ${donor.last_name}${donor.middle_name ? ` ${donor.middle_name}` : ''}</td>
                    <td>${donor.date_of_birth}</td>
                    <td>${donor.address}</td>
                    <td>${donor.phone_number}</td>
                    <td>${donor.insurance_data}</td>
                    <td>${donor.blood_type}</td>
                    <td>${donor.rh_factor}</td>
                `;
                row.addEventListener('click', () => {
                    if (selectedRow) {
                        selectedRow.classList.remove('selected');
                    }
                    selectedRow = row;
                    row.classList.add('selected');
                });
                donorsTable.appendChild(row);
            }
        })
        .catch(error => console.error(error));
}

document.addEventListener('DOMContentLoaded', getDonors);
document.addEventListener('reload', getDonors);