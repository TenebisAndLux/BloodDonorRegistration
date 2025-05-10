document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('blood-search-form');
    const bloodList = document.getElementById('blood-list');
    const requestBtn = document.getElementById('request-blood-btn');
    const mapContainer = document.getElementById('map');

    // Обработка поиска крови
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(searchForm);
        fetch('/blood/search', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            bloodList.innerHTML = '';
            if (data.length === 0) {
                bloodList.innerHTML = '<p>Кровь с указанными параметрами не найдена.</p>';
            } else {
                data.forEach(blood => {
                    const bloodItem = document.createElement('div');
                    bloodItem.textContent = `${blood.blood_group} ${blood.rh_factor} - ${blood.volume} мл`;
                    bloodList.appendChild(bloodItem);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка поиска:', error);
            bloodList.innerHTML = '<p>Произошла ошибка при поиске.</p>';
        });
    });

    // Обработка запроса крови
    requestBtn.addEventListener('click', function() {
        const bloodGroup = document.querySelector('input[name="blood_group"]').value;
        const rhFactor = document.querySelector('input[name="rh_factor"]').value;

        if (!bloodGroup || !rhFactor) {
            alert('Пожалуйста, заполните поля поиска перед запросом.');
            return;
        }

        fetch('/blood/request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ blood_group: bloodGroup, rh_factor: rhFactor })
        })
        .then(response => response.json())
        .then(data => {
            if (data.hospital) {
                bloodList.innerHTML = `<p>Найдена подходящая кровь в больнице: ${data.hospital.name}</p>`;
                mapContainer.style.display = 'block';
                initMap(data.hospital.coordinates);
            } else {
                bloodList.innerHTML = '<p>Подходящая кровь не найдена в ближайших больницах.</p>';
            }
        });
    });

    // Инициализация карты Yandex
    function initMap(coordinates) {
        ymaps.ready(function () {
            const myMap = new ymaps.Map('map', {
                center: coordinates, // Координаты ближайшей больницы
                zoom: 10
            });

            // Добавление метки для больницы
            const hospitalPlacemark = new ymaps.Placemark(coordinates, {
                hintContent: 'Больница с подходящей кровью',
                balloonContent: 'Здесь доступна запрошенная кровь'
            });
            myMap.geoObjects.add(hospitalPlacemark);

            // Пример маршрута от текущей позиции (нужны реальные координаты пользователя)
            ymaps.route([
                [55.76, 37.64], // Замените на текущие координаты пользователя
                coordinates
            ]).then(function (route) {
                myMap.geoObjects.add(route);
            });
        });
    }
});

    let currentPage = 1;
    const itemsPerPage = 10;
    let totalItems = 0;

    function searchBloodSupplies() {
        const bloodGroup = document.getElementById('blood-group-search').value;
        const rhFactor = document.getElementById('rh-factor-search').value;
        const bestBeforeDate = document.getElementById('best-before-date-search').value;

        const params = new URLSearchParams();
        if (bloodGroup) params.append('blood_group', bloodGroup);
        if (rhFactor) params.append('rh_factor', rhFactor);
        if (bestBeforeDate) params.append('best_before_date', bestBeforeDate);
        params.append('page', currentPage);
        params.append('per_page', itemsPerPage);

        fetch(`/blood_bank/search?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                totalItems = data.total;
                updatePagination();
                renderBloodSupplies(data.items);
            })
            .catch(error => console.error('Error:', error));
    }

    function renderBloodSupplies(supplies) {
        const tbody = document.getElementById('blood-supplies-body');
        tbody.innerHTML = '';

        if (supplies.length === 0) {
            const tr = document.createElement('tr');
            tr.innerHTML = '<td colspan="7" class="no-data">Нет данных</td>';
            tbody.appendChild(tr);
            return;
        }

        supplies.forEach(supply => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${supply.blood_group || '-'}</td>
                <td>${supply.rh_factor || '-'}</td>
                <td>${supply.blood_volume || '-'}</td>
                <td>${supply.procurement_date || '-'}</td>
                <td>${supply.best_before_date || '-'}</td>
                <td>${supply.collection_type || '-'}</td>
                <td>
                    <button onclick="writeOffSupply(${supply.collectiontypecode}, ${supply.institutioncode}, ${supply.numberstock})" class="write-off-button">Списано</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    function writeOffSupply(collectionTypeCode, institutionCode, numberStock) {
        if (confirm('Вы уверены, что хотите списать эту запись? Это действие нельзя отменить.')) {
            fetch(`/blood_bank/write_off`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
                },
                body: JSON.stringify({
                    collectiontypecode: collectionTypeCode,
                    institutioncode: institutionCode,
                    numberstock: numberStock
                })
            })
            .then(response => {
                if (response.ok) {
                    searchBloodSupplies();
                } else {
                    alert('Ошибка при списании записи');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }

    function clearSearch() {
        document.getElementById('blood-group-search').value = '';
        document.getElementById('rh-factor-search').value = '';
        document.getElementById('best-before-date-search').value = '';
        currentPage = 1;
        searchBloodSupplies();
    }

    function updatePagination() {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        document.getElementById('page-info').textContent = `Страница ${currentPage} из ${totalPages}`;
        document.getElementById('prev-page').disabled = currentPage === 1;
        document.getElementById('next-page').disabled = currentPage === totalPages || totalPages === 0;
    }

    function prevPage() {
        if (currentPage > 1) {
            currentPage--;
            searchBloodSupplies();
        }
    }

    function nextPage() {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            searchBloodSupplies();
        }
    }

    // Инициализация при загрузке
    document.addEventListener('DOMContentLoaded', searchBloodSupplies);