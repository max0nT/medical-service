import React, { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Image,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useFocusEffect } from "@react-navigation/native";

import { logoutRequest } from "../api/user/auth";
import { MeRequest } from "../api/user/crud";
import { UserRead } from "../api/user/schemes";
import { extractApiErrorMessage } from "../api/error";
import { ErrorModal } from "./ErrorModal";
import { buildAvatarUri, getDisplayName, medicalTheme } from "../theme/medicalTheme";

const placeholderAvatar = require("../assets/profile_placeholder.jpg");
const apiUrl = process.env.EXPO_PUBLIC_API_URL;

const EMPTY_PROFILE: UserRead = {
  id: 0,
  created: "",
  modified: "",
  email: "",
  first_name: "",
  last_name: "",
  sync_with_google_calendar: false,
  role: "",
  avatar: null,
};

export function ProfileScreen({ navigation }: any) {
  const [profile, setProfile] = useState<UserRead>(EMPTY_PROFILE);
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fetchProfile = useCallback(async () => {
    const [statusCode, responseBody] = await MeRequest();
    if (statusCode >= 400) {
      navigation.navigate("Login");
      return;
    }

    setProfile((responseBody as UserRead) ?? EMPTY_PROFILE);
  }, [navigation]);

  useFocusEffect(
    useCallback(() => {
      const load = async () => {
        setLoading(true);
        await fetchProfile();
        setLoading(false);
      };

      void load();
    }, [fetchProfile]),
  );

  const performLogout = async () => {
    const [statusCode, responseBody] = await logoutRequest();
    await AsyncStorage.removeItem("access_token");

    if (statusCode >= 400) {
      setErrorMessage(extractApiErrorMessage(responseBody));
    }

    navigation.navigate("Login");
  };

  const handleLogout = () => {
    Alert.alert("Выход", "Вы уверены, что хотите выйти?", [
      { text: "Отмена", style: "cancel" },
      {
        text: "Выйти",
        style: "destructive",
        onPress: () => {
          void performLogout();
        },
      },
    ]);
  };

  if (loading) {
    return (
      <View style={styles.loaderContainer}>
        <ActivityIndicator size="large" color={medicalTheme.colors.primary} />
      </View>
    );
  }

  const avatarUri = buildAvatarUri(profile.avatar, apiUrl);
  const avatarSource = avatarUri ? { uri: avatarUri } : placeholderAvatar;
  const fullName = getDisplayName(profile.first_name, profile.last_name);
  const initials = fullName
    .split(" ")
    .map((value) => value[0] ?? "")
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <View style={styles.heroCard}>
        <Text style={styles.kicker}>Личный кабинет пациента</Text>
        <Text style={styles.heroTitle}>Ваш профиль здоровья и записей</Text>
        <Text style={styles.heroText}>
          Храните данные профиля в актуальном состоянии, чтобы быстрее записываться на приём.
        </Text>
      </View>

      <View style={styles.profileCard}>
        <View style={styles.avatarFrame}>
          <Image
            source={avatarSource}
            style={styles.avatar}
            defaultSource={placeholderAvatar}
          />
          {avatarUri ? null : (
            <View style={styles.initialsBadge}>
              <Text style={styles.initialsText}>{initials}</Text>
            </View>
          )}
        </View>

        <Text style={styles.userName}>{fullName}</Text>
        <Text style={styles.userEmail}>{profile.email}</Text>

        <View style={styles.badgeRow}>
          <View style={styles.infoBadge}>
            <Text style={styles.infoBadgeLabel}>Роль</Text>
            <Text style={styles.infoBadgeValue}>{profile.role || "client"}</Text>
          </View>
          <View style={styles.infoBadge}>
            <Text style={styles.infoBadgeLabel}>Календарь</Text>
            <Text style={styles.infoBadgeValue}>
              {profile.sync_with_google_calendar ? "Подключён" : "Отключён"}
            </Text>
          </View>
        </View>
      </View>

      <View style={styles.menuContainer}>
        <TouchableOpacity
          style={styles.primaryButton}
          activeOpacity={0.8}
          onPress={() => navigation.navigate("Appointments")}
        >
          <Text style={styles.primaryButtonText}>Записаться на приём</Text>
          <Text style={styles.primaryButtonHint}>Посмотреть доступные слоты и свои записи</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.menuItem}
          activeOpacity={0.8}
          onPress={() => navigation.navigate("EditProfile")}
        >
          <View>
            <Text style={styles.menuItemText}>Редактировать профиль</Text>
            <Text style={styles.menuItemDescription}>
              Изменить данные пациента и фотографию профиля
            </Text>
          </View>
          <Text style={styles.menuItemArrow}>›</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.logoutButton}
          onPress={handleLogout}
          activeOpacity={0.8}
        >
          <Text style={styles.logoutButtonText}>Выйти из аккаунта</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: medicalTheme.colors.background,
  },
  contentContainer: {
    padding: 20,
    paddingBottom: 32,
    gap: 18,
  },
  loaderContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: medicalTheme.colors.background,
  },
  heroCard: {
    backgroundColor: medicalTheme.colors.primary,
    borderRadius: medicalTheme.radius.lg,
    padding: 24,
    paddingTop: 28,
    ...medicalTheme.shadow,
  },
  kicker: {
    color: "#DDF9F1",
    fontSize: 13,
    fontWeight: "700",
    letterSpacing: 1,
    textTransform: "uppercase",
    marginBottom: 10,
  },
  heroTitle: {
    color: "#FFFFFF",
    fontSize: 28,
    fontWeight: "700",
    lineHeight: 34,
    marginBottom: 10,
  },
  heroText: {
    color: "#E9FFFA",
    fontSize: 15,
    lineHeight: 22,
  },
  profileCard: {
    backgroundColor: medicalTheme.colors.surface,
    borderRadius: medicalTheme.radius.lg,
    padding: 24,
    alignItems: "center",
    ...medicalTheme.shadow,
  },
  avatarFrame: {
    position: "relative",
    marginBottom: 18,
  },
  avatar: {
    width: 124,
    height: 124,
    borderRadius: 62,
    borderWidth: 4,
    borderColor: medicalTheme.colors.accent,
    backgroundColor: medicalTheme.colors.surfaceMuted,
  },
  initialsBadge: {
    position: "absolute",
    right: -4,
    bottom: -4,
    width: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: medicalTheme.colors.secondary,
    borderWidth: 3,
    borderColor: medicalTheme.colors.surface,
    justifyContent: "center",
    alignItems: "center",
  },
  initialsText: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 14,
  },
  userName: {
    fontSize: 26,
    fontWeight: "700",
    color: medicalTheme.colors.text,
    textAlign: "center",
    marginBottom: 6,
  },
  userEmail: {
    fontSize: 15,
    color: medicalTheme.colors.textMuted,
    marginBottom: 18,
  },
  badgeRow: {
    width: "100%",
    flexDirection: "row",
    gap: 12,
  },
  infoBadge: {
    flex: 1,
    backgroundColor: medicalTheme.colors.surfaceMuted,
    borderRadius: medicalTheme.radius.md,
    padding: 14,
  },
  infoBadgeLabel: {
    fontSize: 12,
    color: medicalTheme.colors.textMuted,
    marginBottom: 6,
    textTransform: "uppercase",
    letterSpacing: 0.8,
  },
  infoBadgeValue: {
    fontSize: 14,
    color: medicalTheme.colors.text,
    fontWeight: "700",
  },
  menuContainer: {
    gap: 14,
  },
  primaryButton: {
    backgroundColor: medicalTheme.colors.surface,
    borderRadius: medicalTheme.radius.lg,
    padding: 20,
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    ...medicalTheme.shadow,
  },
  primaryButtonText: {
    fontSize: 18,
    fontWeight: "700",
    color: medicalTheme.colors.primaryDark,
    marginBottom: 6,
  },
  primaryButtonHint: {
    fontSize: 14,
    color: medicalTheme.colors.textMuted,
    lineHeight: 20,
  },
  menuItem: {
    backgroundColor: medicalTheme.colors.surface,
    borderRadius: medicalTheme.radius.md,
    padding: 18,
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  menuItemText: {
    fontSize: 17,
    fontWeight: "700",
    color: medicalTheme.colors.text,
    marginBottom: 4,
  },
  menuItemDescription: {
    fontSize: 14,
    color: medicalTheme.colors.textMuted,
    maxWidth: 240,
    lineHeight: 19,
  },
  menuItemArrow: {
    fontSize: 28,
    color: medicalTheme.colors.primary,
  },
  logoutButton: {
    paddingVertical: 18,
    alignItems: "center",
    borderRadius: medicalTheme.radius.md,
    backgroundColor: "#FFF3F3",
    borderWidth: 1,
    borderColor: "#F0D4D4",
  },
  logoutButtonText: {
    color: medicalTheme.colors.danger,
    fontSize: 16,
    fontWeight: "700",
  },
});
