import React, { useState } from "react";
import {
  KeyboardAvoidingView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

import { UserLogin } from "../api/user/schemes";
import { extractApiErrorMessage } from "../api/error";
import { ErrorModal } from "./ErrorModal";
import { loginRequest } from "../api/user/auth";
import { medicalTheme } from "../theme/medicalTheme";

export function LoginScreen({ navigation }: any) {
  const [login, setLogin] = useState<UserLogin>({
    email: "",
    password: "",
  });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleLogin = async () => {
    const [statusCode, requestBody] = await loginRequest(login);
    const response = requestBody as any;

    if (statusCode >= 400) {
      setErrorMessage(extractApiErrorMessage(response, "Ошибка авторизации"));
      return;
    }

    await AsyncStorage.setItem("access_token", response.access_token);
    navigation.navigate("Profile");
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior="height" keyboardVerticalOffset={0}>
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <View style={styles.hero}>
        <Text style={styles.heroBadge}>Medical Service</Text>
        <Text style={styles.heroTitle}>Вход в кабинет пользователя</Text>
        <Text style={styles.heroText}>
          Управляйте записями к врачу, профилем и медицинскими данными в одном месте.
        </Text>
      </View>

      <View style={styles.formCard}>
        <View style={styles.inputGroup}>
          <Text style={styles.inputLabel}>Электронная почта</Text>
          <TextInput
            style={styles.textInput}
            placeholder="patient@clinic.ru"
            placeholderTextColor={medicalTheme.colors.textMuted}
            value={login.email}
            onChangeText={(text: string) => setLogin((prevData) => ({ ...prevData, email: text }))}
            keyboardType="email-address"
            autoCapitalize="none"
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.inputLabel}>Пароль</Text>
          <TextInput
            style={styles.textInput}
            placeholder="Введите пароль"
            placeholderTextColor={medicalTheme.colors.textMuted}
            value={login.password}
            onChangeText={(text: string) => setLogin((prevData) => ({ ...prevData, password: text }))}
            secureTextEntry
            autoCapitalize="none"
          />
        </View>

        <TouchableOpacity
          style={styles.loginButton}
          onPress={() => void handleLogin()}
          activeOpacity={0.85}
        >
          <Text style={styles.loginButtonText}>Войти</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.registerButton}
          onPress={() => navigation.navigate("SignUp")}
          activeOpacity={0.85}
        >
          <Text style={styles.registerButtonText}>Создать аккаунт</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 20,
    backgroundColor: medicalTheme.colors.background,
  },
  hero: {
    backgroundColor: medicalTheme.colors.primary,
    borderRadius: medicalTheme.radius.lg,
    padding: 24,
    marginBottom: 18,
  },
  heroBadge: {
    alignSelf: "flex-start",
    color: "#DDF9F1",
    backgroundColor: "rgba(255,255,255,0.12)",
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: medicalTheme.radius.pill,
    fontSize: 12,
    fontWeight: "700",
    marginBottom: 14,
  },
  heroTitle: {
    fontSize: 29,
    lineHeight: 35,
    fontWeight: "700",
    color: "#FFFFFF",
    marginBottom: 10,
  },
  heroText: {
    color: "#E9FFFA",
    fontSize: 15,
    lineHeight: 21,
  },
  formCard: {
    backgroundColor: medicalTheme.colors.surface,
    borderRadius: medicalTheme.radius.lg,
    padding: 20,
    gap: 16,
    ...medicalTheme.shadow,
  },
  inputGroup: {
    gap: 8,
  },
  inputLabel: {
    fontSize: 15,
    color: medicalTheme.colors.text,
    fontWeight: "600",
  },
  textInput: {
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    borderRadius: medicalTheme.radius.md,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: medicalTheme.colors.text,
    backgroundColor: "#F9FFFD",
  },
  loginButton: {
    backgroundColor: medicalTheme.colors.primary,
    borderRadius: medicalTheme.radius.md,
    paddingVertical: 16,
    alignItems: "center",
    marginTop: 4,
  },
  loginButtonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "700",
  },
  registerButton: {
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    borderRadius: medicalTheme.radius.md,
    paddingVertical: 16,
    alignItems: "center",
    backgroundColor: medicalTheme.colors.surfaceMuted,
  },
  registerButtonText: {
    color: medicalTheme.colors.primaryDark,
    fontSize: 17,
    fontWeight: "700",
  },
});
