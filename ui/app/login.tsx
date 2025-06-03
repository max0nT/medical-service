import { ImageBackground, StyleSheet, Text, Button, TextInput } from "react-native";
import { useState } from "react";
import { Link, router } from "expo-router";
import { loginRequest } from "@/api/auth";
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function Login() {
    const [login, setLogin] = useState({
        email: '',
        password: '',
    });
    const [error, setError] = useState('');

    const handleLogin = async () => {
        const [status, response] = await loginRequest(login);
        console.log("Response:", response);

        if (status === 200) {
            await AsyncStorage.setItem("access_token", response.access_token);
            router.replace('/profile');
        } else {
            setError(response.detail?.detail || 'Ошибка авторизации');
        }
    };

    return (
        <ImageBackground
            source={require('@/assets/images/phone.png')}
            style={styles.container}
        >
            <Text style={styles.loginTitle}>Вход</Text>

            {error ? <Text style={styles.errorText}>{error}</Text> : null}

            <TextInput
                style={styles.input}
                placeholder="Введите вашу почту"
                value={login.email}
                onChangeText={text => setLogin({...login, email: text})}
                keyboardType="email-address"
                autoCapitalize="none"
            />

            <TextInput
                style={styles.input}
                placeholder="Введите пароль"
                secureTextEntry={true}
                value={login.password}
                onChangeText={text => setLogin({...login, password: text})}
            />

            <Button
                title="Войти"
                onPress={handleLogin}
            />

            <Link href="/sign_up" asChild>
                <Button title="Нет аккаунта?" />
            </Link>
        </ImageBackground>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
        height: "100%",
        resizeMode: "cover",
        padding: 20,
    },
    loginTitle: {
        fontSize: 30,
        marginBottom: 20,
        color: 'white',
    },
    input: {
        width: '100%',
        height: 40,
        backgroundColor: 'white',
        marginVertical: 10,
        padding: 10,
        borderRadius: 5,
    },
    errorText: {
        color: 'red',
        marginBottom: 10,
    }
});
