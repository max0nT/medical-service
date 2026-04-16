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
        <ActivityIndicator size="large" color="#2196F3" />
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
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <ErrorModal
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
        duration={5000}
      />

      <Text style={styles.header}>Запись на приём</Text>

      {!canReserve ? (
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>
            Бронирование доступно только пользователям с ролью client.
          </Text>
        </View>
      ) : null}

      <Text style={styles.sectionTitle}>Мои записи</Text>
      {myRecords.length === 0 ? (
        <Text style={styles.emptyText}>У вас пока нет записей.</Text>
      ) : (
        myRecords.map((record) => (
          <View key={record.id} style={styles.card}>
            <Text style={styles.cardTitle}>
              {formatDate(record.start)} - {formatDate(record.end)}
            </Text>
            <Text style={styles.cardMeta}>Статус: подтверждено</Text>
          </View>
        ))
      )}

      <Text style={styles.sectionTitle}>Свободные слоты</Text>
      {availableRecords.length === 0 ? (
        <Text style={styles.emptyText}>Свободных слотов пока нет.</Text>
      ) : (
        availableRecords.map((record) => (
          <View key={record.id} style={styles.card}>
            <Text style={styles.cardTitle}>
              {formatDate(record.start)} - {formatDate(record.end)}
            </Text>
            <Text style={styles.cardMeta}>ID слота: {record.id}</Text>
            <TouchableOpacity
              style={[
                styles.reserveButton,
                !canReserve || bookingId === record.id
                  ? styles.disabledButton
                  : null,
              ]}
              disabled={!canReserve || bookingId === record.id}
              onPress={() => handleReserve(record.id)}
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
    backgroundColor: "#F7F8FA",
  },
  content: {
    padding: 20,
    paddingBottom: 30,
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
    marginBottom: 16,
  },
  infoBox: {
    backgroundColor: "#FFF4E5",
    borderRadius: 10,
    padding: 12,
    marginBottom: 16,
  },
  infoText: {
    color: "#8A5300",
    fontSize: 14,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: "600",
    color: "#222222",
    marginBottom: 10,
    marginTop: 10,
  },
  emptyText: {
    color: "#777777",
    fontSize: 15,
    marginBottom: 10,
  },
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 14,
    marginBottom: 12,
    shadowColor: "#000000",
    shadowOpacity: 0.05,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 1 },
    elevation: 2,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#111111",
    marginBottom: 6,
  },
  cardMeta: {
    fontSize: 14,
    color: "#666666",
    marginBottom: 10,
  },
  reserveButton: {
    backgroundColor: "#2196F3",
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: "center",
  },
  reserveButtonText: {
    color: "#FFFFFF",
    fontWeight: "600",
    fontSize: 15,
  },
  disabledButton: {
    opacity: 0.5,
  },
});
