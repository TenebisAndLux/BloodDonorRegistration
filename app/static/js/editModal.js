    // Asynchronously opens the modal and fills it with donor data
    async function openModal(event) {
        const selectedRow = document.querySelector('tr.selected');
        const donorId = parseInt(selectedRow.querySelector('td:first-child').innerText);
        try {
            const response = await fetch(`/donor/search/${donorId}`);
            const donor = await response.json();
            document.getElementById('editDonorFirstName').value = donor.first_name;
            document.getElementById('editDonorLastName').value = donor.last_name;
            document.getElementById('editDonorMiddleName').value = donor.middle_name;
            document.getElementById('editDonorDateOfBirth').valueAsDate = new Date(donor.date_of_birth);
            document.getElementById('editDonorGender').value = donor.gender;
            document.getElementById('editDonorAddress').value = donor.address;
            document.getElementById('editDonorPhoneNumber').value = donor.phone_number;
            document.getElementById('editDonorHospitalAffiliation').value = donor.hospital_affiliation;
            document.getElementById('editDonorPassportData').value = donor.passport_data;
            document.getElementById('editDonorInsuranceData').value = donor.insurance_data;
            document.getElementById('editDonorBloodType').value = donor.blood_type;
            document.getElementById('editDonorRhFactor').value = donor.rh_factor;
            document.getElementById('editDonorModal').style.display = 'block';
        } catch (error) {
            console.error('Error fetching donor data:', error);
        }
    }

    function closeEditModal() {
        document.getElementById('editDonorModal').style.display = 'none';
    }
    
    document.getElementById('editDonorForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        const selectedRow = document.querySelector('tr.selected');
        const donorId = parseInt(selectedRow.querySelector('td:first-child').innerText);
        const formData = new FormData(document.getElementById('editDonorForm'));
        const dateOfBirthInput = document.getElementById('editDonorDateOfBirth').valueAsDate;
        formData.set('editDonorDateOfBirth', dateOfBirthInput.toISOString().split('T')[0]);
        try {
            const response = await fetch(`/donor/edit/${donorId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    first_name: formData.get('editDonorFirstName'),
                    last_name: formData.get('editDonorLastName'),
                    middle_name: formData.get('editDonorMiddleName'),
                    date_of_birth: formData.get('editDonorDateOfBirth'),
                    gender: formData.get('editDonorGender'),
                    address: formData.get('editDonorAddress'),
                    phone_number: formData.get('editDonorPhoneNumber'),
                    hospital_affiliation: formData.get('editDonorHospitalAffiliation'),
                    passport_data: formData.get('editDonorPassportData'),
                    insurance_data: formData.get('editDonorInsuranceData'),
                    blood_type: formData.get('editDonorBloodType'),
                    rh_factor: formData.get('editDonorRhFactor')
                })
            });
            if (response.ok) {
                closeEditModal();
                getDonors();
                addMedicalHistory('edit')
            } else {
                throw new Error(`Ошибка при редактировании данных донора. donorID: ${donorId}`);
            }
        } catch (error) {
            console.error('Error editing donor data:', error);
        }
    });