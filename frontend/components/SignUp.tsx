import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { UserSignUp } from '../api/user/schemes';
import { extractApiErrorMessage } from '../api/error';
import { ErrorModal } from './ErrorModal';
import { signUpRequest } from '../api/user/auth';

export function SignUpScreen({ navigation }: any){
  const [singUp, setSignUp] = useState<UserSignUp>({
    email: "",
    password: "",
    password_repeat: "",
  })
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleLogin = () => {navigation.navigate("Login")}
  const handleSignUp = async () => {
    let [statusCode, requestBody] = await signUpRequest(singUp)
        const response = requestBody as any
        if (statusCode >= 400) {
            console.log(response)
            setErrorMessage(extractApiErrorMessage(response, "Ошибка регистрации"))
        } else {
            navigation.navigate("Login")
        }
  }

  return (
    <View style={styles.container}>
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
        />
      <Text style={styles.header}>Регистрация</Text>

      <View style={styles.field}>
        <Text style={styles.fieldLabel}>Введите почту</Text>
        <TextInput
          style={styles.input}
          value={singUp.email}
          onChangeText={(text: string) => {setSignUp(prevData => ({...prevData, email: text}))}}
          keyboardType="email-address"
        />
      </View>

      <View style={styles.field}>
        <Text style={styles.fieldLabel}>Введите пароль</Text>
        <TextInput
          style={styles.input}
          value={singUp.password}
          onChangeText={(text: string) => {setSignUp(prevData => ({...prevData, password: text}))}}
          secureTextEntry
        />
      </View>

      <View style={styles.field}>
        <Text style={styles.fieldLabel}>Повторите пароль</Text>
        <TextInput
          style={styles.input}
          value={singUp.password_repeat}
          onChangeText={(text: string) => {setSignUp(prevData => ({...prevData, password_repeat: text}))}}
          secureTextEntry
        />
      </View>

      <TouchableOpacity style={styles.registerButton} onPress={handleSignUp}>
        <Text style={styles.registerButtonText}>Зарегистрироваться</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
        <Text style={styles.loginButtonText}>Войти</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  header: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 40,
    color: '#000',
  },
  field: {
    marginBottom: 20,
  },
  fieldLabel: {
    fontSize: 16,
    marginBottom: 8,
    color: '#333',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  registerButton: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 16,
  },
  registerButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  loginButton: {
    borderWidth: 1,
    borderColor: '#007AFF',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  loginButtonText: {
    color: '#007AFF',
    fontSize: 16,
    fontWeight: '600',
  },
});
