import { User } from "@/api/schemes"
import { useEffect, useState } from "react"
import { ImageBackground, StyleSheet } from "react-native"
import { useNavigation } from '@react-navigation/native'
import { meRequest } from "@/api/auth"


export default function Profile() {
    const [user, setUser] = useState<User>()
    const navigator = useNavigation();
    useEffect(
        () => {
            async function fetch_data() {
                const [status_code, response_body] = await meRequest()
                switch (status_code) {
                    case 200:
                        setUser(response_body)
                    case 401:
                        console.log("Invalid token")
                        navigator.navigate("Login")
                    default:
                        console.log("Internal error")
                        navigator.navigate("Login")

                }
            }
            fetch_data()
        },
        []
    );
    return (
        <ImageBackground
            source={require('@/assets/images/phone.png')}
            style={styles.container}
        >

        </ImageBackground>
    )
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
