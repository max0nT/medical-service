import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Dimensions,
} from 'react-native';

import AsyncStorage from '@react-native-async-storage/async-storage';

import { UserLogin } from '../api/user/schemes';
import { ErrorModal } from './ErrorModal';
import { loginRequest } from '../api/user/auth';

const { width, height } = Dimensions.get('window');

export function LoginScreen({ navigation }){
  const [login, setLogin] = useState<UserLogin>({
    email: "",
    password: "",
  })
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleLogin = async () => {
    let [statusCode, requestBody] = await loginRequest(login)
    if (statusCode >= 400) {
        setErrorMessage(requestBody.detail.detail)
    } else {
      console.log(requestBody)
      await AsyncStorage.setItem("access_token", requestBody.access_token)
      navigation.navigate("Profile")
    }
  };
  const handleRegister = () => {navigation.navigate("SignUp")};

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={'height'}
      keyboardVerticalOffset={0}
    >
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />
      <View style={styles.content}>
        <Text style={styles.screenTitle}>Вход</Text>

        <View style={styles.inputGroup}>
          <Text style={styles.inputLabel}>Введите почту</Text>
          <TextInput
            style={styles.textInput}
            placeholder="ваш@email.com"
            placeholderTextColor="#999"
            value={login.email}
            onChangeText={(text: string) => {setLogin(prevData => ({...prevData, email: text}))}}
            keyboardType="email-address"
            autoCapitalize="none"
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.inputLabel}>Введите пароль</Text>
          <TextInput
            style={styles.textInput}
            placeholder="••••••••"
            placeholderTextColor="#999"
            value={login.password}
            onChangeText={(text: string) => {setLogin(prevData => ({...prevData, password: text}))}}
            secureTextEntry
            autoCapitalize="none"
          />
        </View>

        <TouchableOpacity
          style={styles.loginButton}
          onPress={handleLogin}
          activeOpacity={0.7}
        >
          <Text style={styles.loginButtonText}>Войти</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.registerButton}
          onPress={handleRegister}
          activeOpacity={0.7}
        >
          <Text style={styles.registerButtonText}>Регистрация</Text>
        </TouchableOpacity>

      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    justifyContent: 'center',
    paddingTop: height * 0.1,
    paddingBottom: height * 0.05,
  },
  screenTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#000000',
    marginBottom: 40,
    textAlign: 'center',
  },
  inputGroup: {
    marginBottom: 24,
  },
  inputLabel: {
    fontSize: 16,
    color: '#333333',
    marginBottom: 8,
    fontWeight: '500',
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#E0E0E0',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: '#000000',
    backgroundColor: '#FAFAFA',
  },
  loginButton: {
    backgroundColor: '#2196F3',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 8,
    marginBottom: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 1.5,
  },
  loginButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
  registerButton: {
    borderWidth: 2,
    borderColor: '#2196F3',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    backgroundColor: 'transparent',
  },
  registerButtonText: {
    color: '#2196F3',
    fontSize: 18,
    fontWeight: '600',
  },
  footer: {
    marginTop: 40,
    paddingHorizontal: 20,
  },
  footerText: {
    fontSize: 12,
    color: '#666666',
    textAlign: 'center',
    lineHeight: 16,
  },
});
