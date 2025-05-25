import { View, ImageBackground, StyleSheet, Text, Button } from "react-native"
import { useNavigation } from '@react-navigation/native'

export default function Login() {
    const navigator = useNavigation();

    return (
        <ImageBackground
            source={require('../../assets/images/phone.png')}
            style={styles.container}
        >
            <Text style={styles.loginTitle}>
                Вход
            </Text>
            <View>

            </View>
            <Button
                title="Регистрация"
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
