const getCsrfToken = () => {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.content : '';
};

function searchBloodSupplies() {
    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'block';

    const bloodGroup = document.getElementById('blood-group').value;
    const rhFactor = document.getElementById('rh-factor').value;
    const bestBefore = document.getElementById('best-before').value;

    const params = new URLSearchParams();
    if (bloodGroup) params.append('blood_group', bloodGroup);
    if (rhFactor) params.append('rh_factor', rhFactor);
    if (bestBefore) params.append('best_before', bestBefore);

    fetch(`/blood_bank/search?${params.toString()}`, {
        headers: {
            'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
        },
        credentials: 'include'
    })
    .then(response => {
        if (response.status === 403) {
            window.location.href = '/login';
            return;
        }
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        renderBloodSupplies(data);
    })
    .catch(error => {
        console.error('Search error:', error);
        alert('Ошибка при загрузке данных: ' + error.message);
    })
    .finally(() => {
        loadingElement.style.display = 'none';
    });
}

function renderBloodSupplies(supplies) {
    const tbody = document.getElementById('blood-supplies');
    if (!tbody) {
        console.error('Element #blood-supplies not found');
        return;
    }

    tbody.innerHTML = '';

    if (!supplies || supplies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="no-data">Нет данных</td></tr>';
        return;
    }

    try {
        supplies.forEach(supply => {
            const tr = document.createElement('tr');
            tr.className = 'blood-supply-row';
            tr.innerHTML = `
                <td>${escapeHtml(supply.blood_group || '-')}</td>
                <td>${escapeHtml(supply.rh_factor || '-')}</td>
                <td>${escapeHtml(supply.blood_volume || '-')}</td>
                <td>${escapeHtml(supply.procurement_date || '-')}</td>
                <td>${escapeHtml(supply.best_before_date || '-')}</td>
                <td>${escapeHtml(supply.collection_type || '-')}</td>
                <td>
                    <button onclick="writeOffSupply(${supply.collectiontypecode}, ${supply.institutioncode}, ${supply.numberstock})" 
                            class="write-off-button">Списано</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error rendering blood supplies:', error);
        tbody.innerHTML = '<tr><td colspan="7" class="no-data">Ошибка отображения данных</td></tr>';
    }
}

function writeOffSupply(collectionTypeCode, institutionCode, numberStock) {
    if (!confirm('Вы уверены, что хотите списать эту запись? Это действие нельзя отменить.')) {
        return;
    }

    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'block';

    fetch('/blood_bank/write_off', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': getCsrfToken()
        },
        body: JSON.stringify({
            collectiontypecode: collectionTypeCode,
            institutioncode: institutionCode,
            numberstock: numberStock
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errData => {
                throw new Error(errData.error || 'Ошибка сервера');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showSuccess('Запись успешно списана');
            searchBloodSupplies();
        } else {
            throw new Error(data.error || 'Неизвестная ошибка');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Ошибка при списании: ' + error.message);
    })
    .finally(() => {
        loadingElement.style.display = 'none';
    });
}

function requestBlood() {
    const bloodGroup = document.getElementById('blood-group').value;
    const rhFactor = document.getElementById('rh-factor').value;

    if (!bloodGroup || !rhFactor) {
        showError('Пожалуйста, укажите группу крови и резус-фактор для поиска');
        return;
    }

    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'block';

    fetch('/blood_bank/request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': getCsrfToken()
        },
        body: JSON.stringify({
            blood_group: bloodGroup,
            rh_factor: rhFactor
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errData => {
                throw new Error(errData.error || 'Ошибка сервера');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        if (data.hospitals && data.hospitals.length > 0) {
            // Используем адрес текущего учреждения из ответа сервера
            findNearestHospital(data.current_hospital_address, data.hospitals);
        } else {
            showInfo('Подходящая кровь не найдена в ближайших больницах');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Ошибка при запросе крови: ' + error.message);
    })
    .finally(() => {
        loadingElement.style.display = 'none';
    });
}

function findNearestHospital(currentAddress, hospitals) {
    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'block';

    // Геокодируем адрес текущего учреждения
    ymaps.geocode(currentAddress, {
        results: 1
    }).then(
        function(res) {
            const currentLocation = res.geoObjects.get(0);
            if (!currentLocation) {
                loadingElement.style.display = 'none';
                throw new Error('Не удалось определить местоположение вашей больницы');
            }

            const currentCoords = currentLocation.geometry.getCoordinates();
            const promises = [];

            // Собираем промисы для геокодирования всех больниц
            hospitals.forEach(hospital => {
                promises.push(
                    ymaps.geocode(hospital.address, {
                        results: 1
                    }).then(function(res) {
                        const hospitalLocation = res.geoObjects.get(0);
                        if (hospitalLocation) {
                            return {
                                hospital: hospital,
                                coords: hospitalLocation.geometry.getCoordinates()
                            };
                        }
                        return null;
                    }, function(error) {
                        console.error('Geocoding error:', error);
                        return null;
                    })
                );
            });

            // Когда все геокодирования завершены
            Promise.all(promises).then(results => {
                loadingElement.style.display = 'none';
                const validResults = results.filter(r => r !== null);
                if (validResults.length === 0) {
                    throw new Error('Не удалось определить местоположение больниц');
                }

                // Находим ближайшую больницу
                let nearestHospital = null;
                let minDistance = Infinity;

                validResults.forEach(result => {
                    const distance = ymaps.coordSystem.geo.getDistance(
                        currentCoords,
                        result.coords
                    );

                    if (distance < minDistance) {
                        minDistance = distance;
                        nearestHospital = {
                            hospital: result.hospital,
                            coords: result.coords
                        };
                    }
                });

                // Отображаем маршрут до ближайшей больницы
                if (nearestHospital) {
                    showRouteOnMap(
                        currentCoords,
                        currentAddress,
                        nearestHospital.coords,
                        nearestHospital.hospital
                    );
                } else {
                    throw new Error('Не удалось найти ближайшую больницу');
                }
            }).catch(error => {
                loadingElement.style.display = 'none';
                console.error('Error:', error);
                showError('Ошибка поиска больниц: ' + error.message);
            });
        },
        function(error) {
            loadingElement.style.display = 'none';
            console.error('Geocoding error:', error);
            showError('Ошибка определения вашего местоположения: ' + error.message);
        }
    );
}ц

function showRouteOnMap(fromCoords, fromAddress, toCoords, hospital) {
    try {
        // Открываем модальное окно
        openMapModal();

        // Устанавливаем заголовок
        document.getElementById('hospital-title').textContent =
            `Маршрут до больницы: ${hospital.name}`;

        // Инициализируем карту
        const map = new ymaps.Map('map', {
            center: fromCoords,
            zoom: 10,
            controls: ['zoomControl', 'typeSelector']
        });

        // Создаем маршрут
        const multiRoute = new ymaps.multiRouter.MultiRoute({
            referencePoints: [
                fromCoords,
                toCoords
            ],
            params: {
                routingMode: 'auto'
            }
        }, {
            boundsAutoApply: true,
            wayPointStartIconColor: '#00FF00',
            wayPointFinishIconColor: '#FF0000'
        });

        // Добавляем маршрут на карту
        map.geoObjects.add(multiRoute);

        // Добавляем метки
        const fromPlacemark = new ymaps.Placemark(fromCoords, {
            hintContent: 'Ваше учреждение',
            balloonContent: fromAddress
        }, {
            preset: 'islands#greenDotIcon'
        });

        const toPlacemark = new ymaps.Placemark(toCoords, {
            hintContent: hospital.name,
            balloonContent: `Адрес: ${hospital.address}<br>Наличие крови: ${hospital.blood_volume} мл`
        }, {
            preset: 'islands#redIcon'
        });

        map.geoObjects.add(fromPlacemark).add(toPlacemark);

        // Обработчик завершения построения маршрута
        multiRoute.model.events.add('requestsuccess', function() {
            try {
                const activeRoute = multiRoute.getActiveRoute();
                if (activeRoute) {
                    const distance = activeRoute.properties.get('distance').text;
                    const duration = activeRoute.properties.get('duration').text;

                    document.getElementById('route-info').innerHTML = `
                        <p><strong>Адрес больницы:</strong> ${hospital.address}</p>
                        <p><strong>Расстояние:</strong> ${distance}</p>
                        <p><strong>Примерное время в пути:</strong> ${duration}</p>
                        <p><strong>Объем крови:</strong> ${hospital.blood_volume} мл</p>
                    `;
                }
            } catch (e) {
                console.error('Route info error:', e);
            }
        });

        multiRoute.model.events.add('requesterror', function() {
            showError('Не удалось построить маршрут');
        });

    } catch (error) {
        console.error('Map initialization error:', error);
        showError('Ошибка инициализации карты: ' + error.message);
        closeMapModal();
    }
}

// Вспомогательные функции
function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return unsafe;
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function showError(message) {
    alert('Ошибка: ' + message);
}

function showSuccess(message) {
    alert('Успех: ' + message);
}

function showInfo(message) {
    alert('Информация: ' + message);
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('blood-supplies')) {
        searchBloodSupplies();
    }
});