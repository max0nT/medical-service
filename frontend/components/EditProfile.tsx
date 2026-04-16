import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

import { MeRequest, UpdateProfileRequest } from "../api/user/crud";
import { UserRead, UserWrite } from "../api/user/schemes";
import { extractApiErrorMessage } from "../api/error";
import { ErrorModal } from "./ErrorModal";


export function EditProfileScreen({ navigation }: any) {
  const [userId, setUserId] = useState<number | null>(null);
  const [email, setEmail] = useState<string>("");
  const [form, setForm] = useState<UserWrite>({
    first_name: "",
    last_name: "",
    sync_with_google_calendar: false,
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      const [statusCode, responseBody] = await MeRequest();
      if (statusCode >= 400) {
        setLoading(false);
        navigation.navigate("Login");
        return;
      }

      const profile = responseBody as UserRead;
      setUserId(profile.id);
      setEmail(profile.email);
      setForm({
        first_name: profile.first_name ?? "",
        last_name: profile.last_name ?? "",
        sync_with_google_calendar: profile.sync_with_google_calendar,
      });
      setLoading(false);
    };

    void fetchProfile();
  }, [navigation]);

  const handleSave = async () => {
    if (!userId) {
      setErrorMessage("Пользователь не найден");
      return;
    }

    setSaving(true);
    const [statusCode, responseBody] = await UpdateProfileRequest(userId, form);
    setSaving(false);

    if (statusCode >= 400) {
      setErrorMessage(extractApiErrorMessage(responseBody));
      return;
    }

    navigation.goBack();
  };

  if (loading) {
    return (
      <View style={styles.loaderContainer}>
        <ActivityIndicator size="large" color="#2196F3" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <Text style={styles.header}>Редактирование профиля</Text>

      <View style={styles.field}>
        <Text style={styles.label}>Email</Text>
        <TextInput style={styles.inputDisabled} value={email} editable={false} />
      </View>

      <View style={styles.field}>
        <Text style={styles.label}>Имя</Text>
        <TextInput
          style={styles.input}
          value={form.first_name ?? ""}
          placeholder="Введите имя"
          onChangeText={(text: string) =>
            setForm((prev) => ({ ...prev, first_name: text }))
          }
        />
      </View>

      <View style={styles.field}>
        <Text style={styles.label}>Фамилия</Text>
        <TextInput
          style={styles.input}
          value={form.last_name ?? ""}
          placeholder="Введите фамилию"
          onChangeText={(text: string) =>
            setForm((prev) => ({ ...prev, last_name: text }))
          }
        />
      </View>

      <View style={styles.switchRow}>
        <Text style={styles.switchLabel}>Синхронизация с Google Calendar</Text>
        <Switch
          value={form.sync_with_google_calendar}
          onValueChange={(value: boolean) =>
            setForm((prev) => ({ ...prev, sync_with_google_calendar: value }))
          }
        />
      </View>

      <TouchableOpacity
        style={[styles.saveButton, saving ? styles.disabledButton : null]}
        onPress={handleSave}
        disabled={saving}
      >
        <Text style={styles.saveButtonText}>
          {saving ? "Сохраняю..." : "Сохранить"}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  loaderContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
  },
  header: {
    fontSize: 28,
    fontWeight: "700",
    color: "#111111",
    marginBottom: 24,
  },
  field: {
    marginBottom: 16,
  },
  label: {
    fontSize: 15,
    fontWeight: "500",
    marginBottom: 8,
    color: "#444444",
  },
  input: {
    borderWidth: 1,
    borderColor: "#DADADA",
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 16,
    backgroundColor: "#FAFAFA",
  },
  inputDisabled: {
    borderWidth: 1,
    borderColor: "#E5E5E5",
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 16,
    color: "#888888",
    backgroundColor: "#F2F2F2",
  },
  switchRow: {
    marginTop: 8,
    marginBottom: 24,
    paddingVertical: 10,
    paddingHorizontal: 4,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 16,
  },
  switchLabel: {
    flex: 1,
    fontSize: 15,
    color: "#333333",
  },
  saveButton: {
    backgroundColor: "#2196F3",
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: "center",
  },
  saveButtonText: {
    color: "#FFFFFF",
    fontSize: 17,
    fontWeight: "600",
  },
  disabledButton: {
    opacity: 0.6,
  },
});
