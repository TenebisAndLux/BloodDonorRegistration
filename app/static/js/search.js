document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const searchParams = new URLSearchParams(formData);
        const queryString = searchParams.toString();
        try {
            const response = await fetch('/donor/list/search?' + queryString);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const donors = await response.json();

            const donorsTable = document.getElementById('donors');
            donorsTable.innerHTML = '';

            if (donors.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = `<td>Ничего не найдено</td>`;
                donorsTable.appendChild(row);
            }

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
                    const selectedRow = document.querySelector('.selected');
                    if (selectedRow) {
                        selectedRow.classList.remove('selected');
                    }
                    row.classList.add('selected');
                });

                donorsTable.appendChild(row);
            }
        } catch (error) {
            console.error('Error searching donors:', error);
        }
    });
});
