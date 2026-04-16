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
        <ActivityIndicator size="large" color="#2196F3" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <View style={styles.header}>
        <Text style={styles.headerTitle}>Профиль</Text>
      </View>

      <View style={styles.profileSection}>
        <View style={styles.avatarContainer}>
          <Image
            source={require("../assets/profile_placeholder.jpg")}
            style={styles.avatar}
            defaultSource={require("../assets/profile_placeholder.jpg")}
          />
        </View>

        <Text style={styles.userName}>
          {(profile.first_name ?? "").trim()} {(profile.last_name ?? "").trim()}
        </Text>
        <Text style={styles.userEmail}>{profile.email}</Text>
      </View>

      <View style={styles.menuContainer}>
        <TouchableOpacity
          style={styles.primaryButton}
          activeOpacity={0.7}
          onPress={() => navigation.navigate("Appointments")}
        >
          <Text style={styles.primaryButtonText}>Записаться</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.menuItem}
          activeOpacity={0.7}
          onPress={() => navigation.navigate("EditProfile")}
        >
          <View style={styles.menuItemContent}>
            <Text style={styles.menuItemText}>Редактировать профиль</Text>
            <Text style={styles.menuItemArrow}>›</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.logoutButton}
          onPress={handleLogout}
          activeOpacity={0.7}
        >
          <Text style={styles.logoutButtonText}>Выйти</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F5F5",
  },
  contentContainer: {
    paddingBottom: 30,
  },
  loaderContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
  },
  header: {
    backgroundColor: "#FFFFFF",
    paddingTop: 60,
    paddingBottom: 20,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: "#E0E0E0",
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#000000",
    textAlign: "center",
  },
  profileSection: {
    backgroundColor: "#FFFFFF",
    alignItems: "center",
    paddingVertical: 30,
    marginBottom: 20,
  },
  avatarContainer: {
    marginBottom: 20,
    position: "relative",
  },
  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 3,
    borderColor: "#FFFFFF",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  userName: {
    fontSize: 24,
    fontWeight: "600",
    color: "#000000",
    marginBottom: 8,
    textAlign: "center",
    paddingHorizontal: 20,
  },
  userEmail: {
    fontSize: 16,
    color: "#666666",
    marginBottom: 4,
  },
  menuContainer: {
    backgroundColor: "#FFFFFF",
    marginHorizontal: 20,
    borderRadius: 12,
    paddingVertical: 10,
    marginBottom: 20,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 2,
  },
  primaryButton: {
    backgroundColor: "#2196F3",
    marginHorizontal: 16,
    marginVertical: 16,
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: "center",
    shadowColor: "#2196F3",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  primaryButtonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "600",
  },
  menuItem: {
    paddingVertical: 16,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#F0F0F0",
  },
  menuItemContent: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  menuItemText: {
    fontSize: 16,
    color: "#333333",
  },
  menuItemArrow: {
    fontSize: 24,
    color: "#999999",
  },
  logoutButton: {
    paddingVertical: 16,
    paddingHorizontal: 16,
  },
  logoutButtonText: {
    fontSize: 16,
    color: "#F44336",
    fontWeight: "500",
    textAlign: "center",
  },
});
