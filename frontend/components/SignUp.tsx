import React, { useState } from "react";
import {
  KeyboardAvoidingView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

import { UserSignUp } from "../api/user/schemes";
import { extractApiErrorMessage } from "../api/error";
import { ErrorModal } from "./ErrorModal";
import { signUpRequest } from "../api/user/auth";
import { medicalTheme } from "../theme/medicalTheme";

export function SignUpScreen({ navigation }: any) {
  const [signUp, setSignUp] = useState<UserSignUp>({
    email: "",
    password: "",
    password_repeat: "",
  });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSignUp = async () => {
    const [statusCode, requestBody] = await signUpRequest(signUp);
    const response = requestBody as any;

    if (statusCode >= 400) {
      setErrorMessage(extractApiErrorMessage(response, "Ошибка регистрации"));
      return;
    }

    navigation.navigate("Login");
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior="height">
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <View style={styles.hero}>
        <Text style={styles.heroTitle}>Регистрация пользователя</Text>
        <Text style={styles.heroText}>
          Создайте аккаунт, чтобы записываться на приём и управлять профилем в приложении клиники.
        </Text>
      </View>

      <View style={styles.formCard}>
        <View style={styles.field}>
          <Text style={styles.fieldLabel}>Электронная почта</Text>
          <TextInput
            style={styles.input}
            value={signUp.email}
            onChangeText={(text: string) => setSignUp((prevData) => ({ ...prevData, email: text }))}
            placeholder="patient@clinic.ru"
            placeholderTextColor={medicalTheme.colors.textMuted}
            keyboardType="email-address"
            autoCapitalize="none"
          />
        </View>

        <View style={styles.field}>
          <Text style={styles.fieldLabel}>Пароль</Text>
          <TextInput
            style={styles.input}
            value={signUp.password}
            onChangeText={(text: string) => setSignUp((prevData) => ({ ...prevData, password: text }))}
            secureTextEntry
            placeholder="Введите пароль"
            placeholderTextColor={medicalTheme.colors.textMuted}
          />
        </View>

        <View style={styles.field}>
          <Text style={styles.fieldLabel}>Повторите пароль</Text>
          <TextInput
            style={styles.input}
            value={signUp.password_repeat}
            onChangeText={(text: string) =>
              setSignUp((prevData) => ({ ...prevData, password_repeat: text }))
            }
            secureTextEntry
            placeholder="Повторите пароль"
            placeholderTextColor={medicalTheme.colors.textMuted}
          />
        </View>

        <TouchableOpacity style={styles.registerButton} onPress={() => void handleSignUp()}>
          <Text style={styles.registerButtonText}>Зарегистрироваться</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.loginButton} onPress={() => navigation.navigate("Login")}>
          <Text style={styles.loginButtonText}>Назад ко входу</Text>
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
    backgroundColor: medicalTheme.colors.surfaceMuted,
    borderRadius: medicalTheme.radius.lg,
    padding: 22,
    marginBottom: 18,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: "700",
    color: medicalTheme.colors.text,
    marginBottom: 10,
  },
  heroText: {
    color: medicalTheme.colors.textMuted,
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
  field: {
    gap: 8,
  },
  fieldLabel: {
    fontSize: 15,
    color: medicalTheme.colors.text,
    fontWeight: "600",
  },
  input: {
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    borderRadius: medicalTheme.radius.md,
    padding: 14,
    fontSize: 16,
    color: medicalTheme.colors.text,
    backgroundColor: "#F9FFFD",
  },
  registerButton: {
    backgroundColor: medicalTheme.colors.primary,
    borderRadius: medicalTheme.radius.md,
    padding: 16,
    alignItems: "center",
    marginTop: 4,
  },
  registerButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  loginButton: {
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    borderRadius: medicalTheme.radius.md,
    padding: 16,
    alignItems: "center",
    backgroundColor: medicalTheme.colors.surfaceMuted,
  },
  loginButtonText: {
    color: medicalTheme.colors.primaryDark,
    fontSize: 16,
    fontWeight: "700",
  },
});
