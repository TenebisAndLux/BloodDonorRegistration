function addBloodCollectionModal() {
    document.getElementById('bloodCollectionModal').style.display = 'block';
}

function closeBloodCollectionModal() {
    document.getElementById('bloodCollectionModal').style.display = 'none';
}

document.getElementById('donorSearch').addEventListener('input', function(e) {
    const query = e.target.value;
    if (query.length > 2) {
        fetch(`/donor/search?q=${query}`)
            .then(response => response.json())
            .then(data => {
                const results = document.getElementById('donorSearchResults');
                results.innerHTML = '';

                data.donors.forEach(donor => {
                    const div = document.createElement('div');
                    div.className = 'donor-result';
                    div.textContent = `${donor.secondName} ${donor.name} (${donor.passportData})`;
                    div.onclick = () => selectDonor(donor);
                    results.appendChild(div);
                });
            });
    }
});

function selectDonor(donor) {
    document.getElementById('donorSearch').value = `${donor.secondName} ${donor.name}`;
    document.getElementById('donorSearchResults').innerHTML = '';
    // Сохраняем выбранного донора для формы
    currentSelectedDonor = donor;
}

document.getElementById('bloodCollectionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const collectionData = {
        donorPassport: currentSelectedDonor.passportData,
        institutionCode: currentSelectedDonor.institutionCode,
        type: document.getElementById('collectionType').value,
        volume: document.getElementById('collectionVolume').value,
        date: document.getElementById('collectionDate').value,
        notes: document.getElementById('examinationResults').value
    };

    fetch('/blood_collection/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(collectionData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeBloodCollectionModal();
            alert('Забор крови успешно добавлен');
        }
    });
});