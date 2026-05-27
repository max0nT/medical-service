import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Image,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import * as ImagePicker from "expo-image-picker";

import { UploadFileRequest, UploadedS3File } from "../api/s3";
import { MeRequest, UpdateProfileRequest } from "../api/user/crud";
import { UserRead, UserWrite } from "../api/user/schemes";
import { extractApiErrorMessage } from "../api/error";
import { ErrorModal } from "./ErrorModal";
import { buildAvatarUri, getDisplayName, medicalTheme } from "../theme/medicalTheme";

const apiUrl = process.env.EXPO_PUBLIC_API_URL;
const placeholderAvatar = require("../assets/profile_placeholder.jpg");

export function EditProfileScreen({ navigation }: any) {
  const [userId, setUserId] = useState<number | null>(null);
  const [email, setEmail] = useState<string>("");
  const [form, setForm] = useState<UserWrite>({
    first_name: "",
    last_name: "",
    sync_with_google_calendar: false,
    avatar: null,
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [uploadingPhoto, setUploadingPhoto] = useState<boolean>(false);
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
        avatar: profile.avatar ?? null,
      });
      setLoading(false);
    };

    void fetchProfile();
  }, [navigation]);

  const handlePickPhoto = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
      setErrorMessage("Разрешите доступ к фотографиям, чтобы загрузить аватар.");
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
    });

    if (result.canceled || !result.assets.length) {
      return;
    }

    const asset = result.assets[0];
    setUploadingPhoto(true);

    const [statusCode, responseBody] = await UploadFileRequest({
      uri: asset.uri,
      name: asset.fileName ?? `avatar-${Date.now()}.jpg`,
      type: asset.mimeType ?? "image/jpeg",
    });

    setUploadingPhoto(false);

    if (statusCode >= 400) {
      setErrorMessage(extractApiErrorMessage(responseBody, "Не удалось загрузить фото"));
      return;
    }

    const uploadedPhoto = responseBody as UploadedS3File;
    setForm((prev) => ({
      ...prev,
      avatar: uploadedPhoto.name,
    }));
  };

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
        <ActivityIndicator size="large" color={medicalTheme.colors.primary} />
      </View>
    );
  }

  const avatarUri = buildAvatarUri(form.avatar, apiUrl);
  const fullName = getDisplayName(form.first_name, form.last_name);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <View style={styles.heroCard}>
        <Text style={styles.heroTitle}>Профиль пациента</Text>
        <Text style={styles.heroText}>
          Обновите личные данные и фотографию, чтобы ваш кабинет выглядел аккуратно и узнаваемо.
        </Text>
      </View>

      <View style={styles.card}>
        <View style={styles.avatarSection}>
          <Image
            source={avatarUri ? { uri: avatarUri } : placeholderAvatar}
            style={styles.avatar}
            defaultSource={placeholderAvatar}
          />
          <Text style={styles.avatarName}>{fullName}</Text>
          <TouchableOpacity
            style={[styles.photoButton, uploadingPhoto ? styles.disabledButton : null]}
            onPress={() => void handlePickPhoto()}
            disabled={uploadingPhoto}
            activeOpacity={0.8}
          >
            <Text style={styles.photoButtonText}>
              {uploadingPhoto ? "Загружаю фото..." : "Загрузить фото"}
            </Text>
          </TouchableOpacity>
        </View>

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
            placeholderTextColor={medicalTheme.colors.textMuted}
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
            placeholderTextColor={medicalTheme.colors.textMuted}
            onChangeText={(text: string) =>
              setForm((prev) => ({ ...prev, last_name: text }))
            }
          />
        </View>

        <View style={styles.switchCard}>
          <View style={styles.switchCopy}>
            <Text style={styles.switchTitle}>Синхронизация с Google Calendar</Text>
            <Text style={styles.switchDescription}>
              Получайте свои записи и напоминания в календаре.
            </Text>
          </View>
          <Switch
            value={form.sync_with_google_calendar}
            trackColor={{
              false: "#D7E7E2",
              true: "#7ED6C6",
            }}
            thumbColor={form.sync_with_google_calendar ? medicalTheme.colors.primary : "#FFFFFF"}
            onValueChange={(value: boolean) =>
              setForm((prev) => ({ ...prev, sync_with_google_calendar: value }))
            }
          />
        </View>
      </View>

      <TouchableOpacity
        style={[styles.saveButton, saving ? styles.disabledButton : null]}
        onPress={() => void handleSave()}
        disabled={saving}
        activeOpacity={0.85}
      >
        <Text style={styles.saveButtonText}>
          {saving ? "Сохраняю..." : "Сохранить изменения"}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: medicalTheme.colors.background,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
    gap: 18,
  },
  loaderContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: medicalTheme.colors.background,
  },
  heroCard: {
    backgroundColor: medicalTheme.colors.surfaceMuted,
    borderRadius: medicalTheme.radius.lg,
    padding: 22,
  },
  heroTitle: {
    fontSize: 26,
    fontWeight: "700",
    color: medicalTheme.colors.text,
    marginBottom: 8,
  },
  heroText: {
    fontSize: 15,
    color: medicalTheme.colors.textMuted,
    lineHeight: 22,
  },
  card: {
    backgroundColor: medicalTheme.colors.surface,
    borderRadius: medicalTheme.radius.lg,
    padding: 20,
    gap: 16,
    ...medicalTheme.shadow,
  },
  avatarSection: {
    alignItems: "center",
    marginBottom: 6,
  },
  avatar: {
    width: 116,
    height: 116,
    borderRadius: 58,
    backgroundColor: medicalTheme.colors.surfaceMuted,
    marginBottom: 12,
    borderWidth: 4,
    borderColor: medicalTheme.colors.accent,
  },
  avatarName: {
    fontSize: 18,
    fontWeight: "700",
    color: medicalTheme.colors.text,
    marginBottom: 12,
  },
  photoButton: {
    backgroundColor: medicalTheme.colors.accent,
    paddingVertical: 12,
    paddingHorizontal: 18,
    borderRadius: medicalTheme.radius.pill,
  },
  photoButtonText: {
    color: medicalTheme.colors.primaryDark,
    fontWeight: "700",
    fontSize: 14,
  },
  field: {
    gap: 8,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    color: medicalTheme.colors.text,
  },
  input: {
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    borderRadius: medicalTheme.radius.md,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: medicalTheme.colors.text,
    backgroundColor: "#F9FFFD",
  },
  inputDisabled: {
    borderWidth: 1,
    borderColor: "#DDECE7",
    borderRadius: medicalTheme.radius.md,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: medicalTheme.colors.textMuted,
    backgroundColor: "#F3F8F7",
  },
  switchCard: {
    marginTop: 8,
    padding: 16,
    borderRadius: medicalTheme.radius.md,
    backgroundColor: medicalTheme.colors.surfaceMuted,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 16,
  },
  switchCopy: {
    flex: 1,
    gap: 4,
  },
  switchTitle: {
    fontSize: 15,
    fontWeight: "700",
    color: medicalTheme.colors.text,
  },
  switchDescription: {
    fontSize: 13,
    lineHeight: 18,
    color: medicalTheme.colors.textMuted,
  },
  saveButton: {
    backgroundColor: medicalTheme.colors.primary,
    borderRadius: medicalTheme.radius.md,
    paddingVertical: 16,
    alignItems: "center",
    ...medicalTheme.shadow,
  },
  saveButtonText: {
    color: "#FFFFFF",
    fontSize: 17,
    fontWeight: "700",
  },
  disabledButton: {
    opacity: 0.6,
  },
});
