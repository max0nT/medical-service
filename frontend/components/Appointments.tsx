import React, { useCallback, useState } from "react";
import {
  ActivityIndicator,
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useFocusEffect } from "@react-navigation/native";

import { ListRecordsRequest, ReserveRecordRequest } from "../api/record/crud";
import { RecordRead } from "../api/record/schemes";
import { MeRequest } from "../api/user/crud";
import { UserRead } from "../api/user/schemes";
import { extractApiErrorMessage } from "../api/error";
import { ErrorModal } from "./ErrorModal";
import { medicalTheme } from "../theme/medicalTheme";

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export function AppointmentsScreen({ navigation }: any) {
  const [profile, setProfile] = useState<UserRead | null>(null);
  const [records, setRecords] = useState<RecordRead[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [bookingId, setBookingId] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    const [profileStatus, profileBody] = await MeRequest();
    if (profileStatus >= 400) {
      navigation.navigate("Login");
      return;
    }

    const nextProfile = profileBody as UserRead;
    setProfile(nextProfile);

    const [recordsStatus, recordsBody] = await ListRecordsRequest();
    if (recordsStatus >= 400) {
      setErrorMessage(extractApiErrorMessage(recordsBody));
      return;
    }

    const sortedRecords = [...(recordsBody as RecordRead[])].sort((a, b) =>
      a.start.localeCompare(b.start),
    );
    setRecords(sortedRecords);
  }, [navigation]);

  useFocusEffect(
    useCallback(() => {
      const load = async () => {
        setLoading(true);
        await fetchData();
        setLoading(false);
      };

      void load();
    }, [fetchData]),
  );

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const handleReserve = async (recordId: number) => {
    setBookingId(recordId);
    const [statusCode, responseBody] = await ReserveRecordRequest(recordId);
    setBookingId(null);

    if (statusCode >= 400) {
      setErrorMessage(extractApiErrorMessage(responseBody));
      return;
    }

    await fetchData();
  };

  if (loading) {
    return (
      <View style={styles.loaderContainer}>
        <ActivityIndicator size="large" color={medicalTheme.colors.primary} />
      </View>
    );
  }

  const myRecords = records.filter(
    (record) => record.reserved_by_id === profile?.id,
  );
  const availableRecords = records.filter((record) => record.reserved_by_id === null);
  const canReserve = profile?.role === "client";

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={() => void onRefresh()}
          tintColor={medicalTheme.colors.primary}
        />
      }
    >
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <View style={styles.heroCard}>
        <Text style={styles.heroTitle}>Запись на приём</Text>
        <Text style={styles.heroText}>
          Отслеживайте подтверждённые записи и выбирайте ближайшее свободное окно для посещения клиники.
        </Text>
      </View>

      {!canReserve ? (
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>
            Бронирование доступно только пользователям с ролью client.
          </Text>
        </View>
      ) : null}

      <Text style={styles.sectionTitle}>Мои записи</Text>
      {myRecords.length === 0 ? (
        <View style={styles.emptyCard}>
          <Text style={styles.emptyText}>У вас пока нет подтверждённых записей.</Text>
        </View>
      ) : (
        myRecords.map((record) => (
          <View key={record.id} style={styles.card}>
            <Text style={styles.cardTitle}>{formatDate(record.start)}</Text>
            <Text style={styles.cardMeta}>Завершение: {formatDate(record.end)}</Text>
            <View style={styles.statusBadge}>
              <Text style={styles.statusText}>Подтверждено</Text>
            </View>
          </View>
        ))
      )}

      <Text style={styles.sectionTitle}>Свободные слоты</Text>
      {availableRecords.length === 0 ? (
        <View style={styles.emptyCard}>
          <Text style={styles.emptyText}>Свободных слотов пока нет.</Text>
        </View>
      ) : (
        availableRecords.map((record) => (
          <View key={record.id} style={styles.card}>
            <Text style={styles.cardTitle}>{formatDate(record.start)}</Text>
            <Text style={styles.cardMeta}>Окончание: {formatDate(record.end)}</Text>
            <Text style={styles.slotHint}>Идентификатор слота: {record.id}</Text>
            <TouchableOpacity
              style={[
                styles.reserveButton,
                !canReserve || bookingId === record.id ? styles.disabledButton : null,
              ]}
              disabled={!canReserve || bookingId === record.id}
              onPress={() => void handleReserve(record.id)}
              activeOpacity={0.85}
            >
              <Text style={styles.reserveButtonText}>
                {bookingId === record.id ? "Бронирую..." : "Записаться"}
              </Text>
            </TouchableOpacity>
          </View>
        ))
      )}
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
    paddingBottom: 32,
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
    marginBottom: 18,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: "700",
    color: "#FFFFFF",
    marginBottom: 8,
  },
  heroText: {
    fontSize: 15,
    lineHeight: 22,
    color: "#E6FEF8",
  },
  infoBox: {
    backgroundColor: medicalTheme.colors.warningBg,
    borderRadius: medicalTheme.radius.md,
    padding: 14,
    marginBottom: 18,
  },
  infoText: {
    color: medicalTheme.colors.warningText,
    fontSize: 14,
    lineHeight: 20,
  },
  sectionTitle: {
    fontSize: 21,
    fontWeight: "700",
    color: medicalTheme.colors.text,
    marginBottom: 12,
    marginTop: 6,
  },
  emptyCard: {
    backgroundColor: medicalTheme.colors.surface,
    borderRadius: medicalTheme.radius.md,
    padding: 18,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
  },
  emptyText: {
    color: medicalTheme.colors.textMuted,
    fontSize: 15,
    lineHeight: 21,
  },
  card: {
    backgroundColor: medicalTheme.colors.surface,
    borderRadius: medicalTheme.radius.md,
    padding: 18,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: medicalTheme.colors.border,
    ...medicalTheme.shadow,
  },
  cardTitle: {
    fontSize: 17,
    fontWeight: "700",
    color: medicalTheme.colors.text,
    marginBottom: 8,
  },
  cardMeta: {
    fontSize: 14,
    color: medicalTheme.colors.textMuted,
    marginBottom: 10,
  },
  slotHint: {
    fontSize: 13,
    color: medicalTheme.colors.textMuted,
    marginBottom: 12,
  },
  statusBadge: {
    alignSelf: "flex-start",
    backgroundColor: medicalTheme.colors.accent,
    borderRadius: medicalTheme.radius.pill,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  statusText: {
    color: medicalTheme.colors.primaryDark,
    fontSize: 13,
    fontWeight: "700",
  },
  reserveButton: {
    backgroundColor: medicalTheme.colors.primary,
    borderRadius: medicalTheme.radius.md,
    paddingVertical: 13,
    alignItems: "center",
  },
  reserveButtonText: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 15,
  },
  disabledButton: {
    opacity: 0.5,
  },
});
