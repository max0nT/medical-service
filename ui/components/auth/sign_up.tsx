import { useState } from "react";
import { Text, ImageBackground, StyleSheet, Button, TextInput } from "react-native"
import { useNavigation } from '@react-navigation/native'
import { signUpRequest } from "../../api/auth"


export default function SignUp() {
  const navigator = useNavigation();
  const [signUp, setSignUp] = useState(
    {
      email: '',
      password: '',
      password_repeat: '',
    },
  )
  const [error, setError] = useState("")

  return (
    <ImageBackground
        source={require('@/assets/images/phone.png')}
        style={styles.container}
    >
      <Text style={styles.loginTitle}>
          Регистрация
      </Text>
      <Text>
        {error}
      </Text>
          <TextInput
            placeholder="Введите вашу почту"
            value={signUp.email}
            onChangeText={
              text => {
                setSignUp({
                  ...signUp,
                  email: text,
                });
              }
            }
          />
          <TextInput
            placeholder="Придумайте пароль"
            secureTextEntry={true}
            value={signUp.password}
            onChangeText={
              text => {
                setSignUp({
                  ...signUp,
                  password: text
                })
              }
            }
          />
          <TextInput
            placeholder="Введите пароль заново"
            secureTextEntry={true}
            value={signUp.password_repeat}
            onChangeText={
              text => {
                setSignUp({
                  ...signUp,
                  password_repeat: text
                })
              }
            }
          />
          <Button
            title="Зарегистрироваться"
            onPress={
             async () => {
                const [status, response] = await signUpRequest(signUp)
                console.log(status)
                if (status != 201){
                  setError(response.detail.detail)
                }
                else {
                  setError("Успешная регистрация")
                }
              }
            }
          >
          </Button>


      <Button
          title="Уже есть аккаунт?"
          onPress={() => {navigator.navigate("Login")}}
      >
      </Button>


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
