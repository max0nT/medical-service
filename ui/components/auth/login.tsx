import { ImageBackground, StyleSheet, Text, Button, TextInput } from "react-native"
import { useState } from "react";
import { useNavigation } from '@react-navigation/native'
import { loginRequest } from "../../api/auth"

export default function Login() {
    const navigator = useNavigation();
    const [login, setLogin] = useState(
        {
            email: '',
            password: '',
        }
    )
    const [error, setError] = useState("")

    return (
        <ImageBackground
            source={require('@/assets/images/phone.png')}
            style={styles.container}
        >
            <Text style={styles.loginTitle}>
                Вход
            </Text>
            <TextInput
                placeholder="Введите вашу почту"
                value={login.email}
                onChangeText={
                    text => {
                    setLogin({
                        ...login,
                        email: text,
                    });
                    }
                }
            />
            <TextInput
            placeholder="Введите пароль"
            secureTextEntry={true}
            value={login.password}
            onChangeText={
                text => {
                setLogin({
                    ...login,
                    password: text
                })
                }
            }
            />
            <Button
                title="Войти"
                onPress={
                    async () => {
                        const [status, response] = await loginRequest(login)
                        console.log(response)
                        console.log(status)
                        if (status != 200){
                            setError(response.detail.detail)
                            return
                        }
                        navigator.navigate("Profile")
                        setError("Успешный вход")
                    }
                }
            >
            </Button>

            <Button
                title="Нет аккаунта?"
                onPress={() => {navigator.navigate("SignUp")}}
            >
            </Button>

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
    },
    loginTitle: {
        fontSize: 30,
    }
})
