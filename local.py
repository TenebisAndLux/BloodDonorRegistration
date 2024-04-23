import requests


def get_data_from_server(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус-код ответа
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None


def process_data(data):
    if data:
        # Добавьте здесь вашу логику обработки данных
        print("Data received successfully:", data)
    else:
        print("No data received from the server")


if __name__ == "__main__":
    server_url = "http://127.0.0.1:3000/api/main"

    data = get_data_from_server(server_url)
    process_data(data)
