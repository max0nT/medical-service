import React, { useState } from 'react';
import {
  ImageBackground,
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView
} from "react-native";
import MapView, { Marker } from 'react-native-maps';

export default function WeatherMapApp() {
    const [city, setCity] = useState('');
    const [weather, setWeather] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showMap, setShowMap] = useState(false);
    const [markerPosition, setMarkerPosition] = useState({
        latitude: 55.7558,
        longitude: 37.6176,
    });

    // Замоканная функция получения погоды
    const fetchMockWeather = () => {
        if (!city.trim()) {
            setError('Введите название города');
            return;
        }

        setLoading(true);
        setError('');
        setShowMap(false);

        // Имитация задержки API
        setTimeout(() => {
            try {
                // Статические данные для летней погоды
                const summerWeatherOptions = [
                    { temp: 25, desc: "Солнечно ☀️", humidity: 45, wind: 2.5 },
                    { temp: 28, desc: "Ясно 🌤️", humidity: 50, wind: 3.0 },
                    { temp: 30, desc: "Жарко 🔥", humidity: 40, wind: 1.8 },
                    { temp: 22, desc: "Лёгкие облака ⛅", humidity: 55, wind: 4.2 },
                    { temp: 26, desc: "Тёплый ветер 🌬️", humidity: 48, wind: 5.0 },
                ];

                const randomWeather = summerWeatherOptions[
                    Math.floor(Math.random() * summerWeatherOptions.length)
                ];

                const mockWeatherData = {
                    city: city,
                    temperature: randomWeather.temp,
                    description: randomWeather.desc,
                    humidity: randomWeather.humidity,
                    wind: randomWeather.wind,
                };

                setWeather(mockWeatherData);

                // Слегка смещаем метку для "реализма"
                setMarkerPosition({
                    latitude: 56.0184 + (Math.random() * 0.02 - 0.01),
                    longitude: 92.8672 + (Math.random() * 0.02 - 0.01),
                });

                setShowMap(true);
            } catch (err) {
                setError('Ошибка при получении данных');
            } finally {
                setLoading(false);
            }
        }, 1500);
    };

    return (
        <ImageBackground
            source={require('@/assets/images/phone.png')}
            style={styles.container}
        >
            <ScrollView contentContainerStyle={styles.scrollContainer}>
                <View style={styles.content}>
                    <Text style={styles.title}>Погодное приложение</Text>

                    <View style={styles.searchContainer}>
                        <TextInput
                            style={styles.input}
                            placeholder="Введите город"
                            value={city}
                            onChangeText={setCity}
                            onSubmitEditing={fetchMockWeather}
                        />
                        <TouchableOpacity
                            style={styles.button}
                            onPress={fetchMockWeather}
                            disabled={loading}
                        >
                            <Text style={styles.buttonText}>Поиск</Text>
                        </TouchableOpacity>
                    </View>

                    {loading && <ActivityIndicator size="large" color="#0000ff" />}

                    {error ? (
                        <Text style={styles.error}>{error}</Text>
                    ) : weather && (
                        <>
                            <View style={styles.weatherContainer}>
                                <Text style={styles.weatherCity}>{weather.city}</Text>
                                <Text style={styles.weatherTemp}>{weather.temperature}°C</Text>
                                <Text style={styles.weatherDesc}>{weather.description}</Text>
                                <View style={styles.weatherDetails}>
                                    <Text>Влажность: {weather.humidity}%</Text>
                                    <Text>Ветер: {weather.wind} м/с</Text>
                                </View>
                            </View>

                            {showMap && (
                                <View style={styles.mapContainer}>
                                    <MapView
                                        style={styles.map}
                                        initialRegion={{
                                            latitude: markerPosition.latitude,
                                            longitude: markerPosition.longitude,
                                            latitudeDelta: 0.0922,
                                            longitudeDelta: 0.0421,
                                        }}
                                    >
                                        <Marker
                                            coordinate={markerPosition}
                                            title={weather.city}
                                            description={`${weather.temperature}°C, ${weather.description}`}
                                        />
                                    </MapView>
                                </View>
                            )}
                        </>
                    )}
                </View>
            </ScrollView>
        </ImageBackground>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        width: "100%",
        height: "100%",
    },
    scrollContainer: {
        flexGrow: 1,
        justifyContent: 'center',
    },
    content: {
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        padding: 20,
        borderRadius: 10,
        width: '90%',
        alignSelf: 'center',
        alignItems: 'center',
        marginVertical: 20,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    searchContainer: {
        flexDirection: 'row',
        width: '100%',
        marginBottom: 20,
    },
    input: {
        flex: 1,
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 5,
        padding: 10,
        marginRight: 10,
        backgroundColor: 'white',
    },
    button: {
        backgroundColor: '#007AFF',
        padding: 10,
        borderRadius: 5,
        justifyContent: 'center',
    },
    buttonText: {
        color: 'white',
        fontWeight: 'bold',
    },
    weatherContainer: {
        alignItems: 'center',
        marginTop: 20,
        width: '100%',
    },
    weatherCity: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 5,
    },
    weatherTemp: {
        fontSize: 48,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    weatherDesc: {
        fontSize: 18,
        marginBottom: 10,
    },
    weatherDetails: {
        marginTop: 10,
    },
    error: {
        color: 'red',
        marginTop: 10,
    },
    mapContainer: {
        width: '100%',
        height: 300,
        marginTop: 20,
        borderRadius: 10,
        overflow: 'hidden',
    },
    map: {
        ...StyleSheet.absoluteFillObject,
    },
});
