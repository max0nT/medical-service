import { useEffect, useState } from 'react';
import { ImageBackground, StyleSheet, TextInput, TouchableOpacity, Text, View, Alert, Switch } from 'react-native';
import { meRequest, updateUserRequest } from '@/api/auth';
import { User, UserWrite } from '@/api/schemes';
import { Link, router } from "expo-router";


export default function Profile() {
    const [user, setUser] = useState<User | null>(null);
    const [editedUser, setEditedUser] = useState<Partial<UserWrite>>({});
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        async function fetchData() {
            try {
                const [status_code, response_body] = await meRequest();
                if (status_code === 200) {
                    setUser(response_body);
                    setEditedUser({
                        email: response_body.email,
                        first_name: response_body.first_name,
                        last_name: response_body.last_name,
                        sync_with_google_calendar: response_body.sync_with_google_calendar
                    });
                } else {
                    router.replace("/login");
                }
            } catch (error) {
                console.error("Ошибка при загрузке данных:", error);
                Alert.alert("Ошибка", "Не удалось загрузить данные пользователя");
            }
        }
        fetchData();
    }, []);

    const handleSave = async () => {
        try {
            if (editedUser) {
                const [status_code, updatedUser] = await updateUserRequest(
                    editedUser as UserWrite,
                    user.id,
                );
                if (status_code === 200) {
                    setUser(prev => ({ ...prev, ...updatedUser }));
                    setIsEditing(false);
                    Alert.alert("Успех", "Данные успешно обновлены");
                } else {
                    Alert.alert("Ошибка", "Не удалось обновить данные");
                }
            }
        } catch (error) {
            console.error("Ошибка при обновлении:", error);
            Alert.alert("Ошибка", "Произошла ошибка при обновлении данных");
        }
    };

    const handleReset = () => {
        setEditedUser({
            email: user?.email,
            first_name: user?.first_name,
            last_name: user?.last_name,
            sync_with_google_calendar: user?.sync_with_google_calendar
        });
        setIsEditing(false);
    };

    const formatDate = (dateString?: string) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU');
    };

    const handleShowBranches = () => {router.replace("/branches")};

    return (
        <ImageBackground
            source={require('@/assets/images/phone.png')}
            style={styles.container}
        >
            <View style={styles.formContainer}>
                <TextInput
                    style={styles.input}
                    value={editedUser?.email || ''}
                    onChangeText={(text) => setEditedUser({...editedUser, email: text})}
                    placeholder="Email"
                    editable={isEditing}
                    keyboardType="email-address"
                />
                <TextInput
                    style={styles.input}
                    value={editedUser?.first_name || ''}
                    onChangeText={(text) => setEditedUser({...editedUser, first_name: text})}
                    placeholder="Имя"
                    editable={isEditing}
                />
                <TextInput
                    style={styles.input}
                    value={editedUser?.last_name || ''}
                    onChangeText={(text) => setEditedUser({...editedUser, last_name: text})}
                    placeholder="Фамилия"
                    editable={isEditing}
                />

                <View style={styles.switchContainer}>
                    <Text style={styles.switchLabel}>Синхронизация с Google Календарём</Text>
                    <Switch
                        value={editedUser?.sync_with_google_calendar || false}
                        onValueChange={(value) => setEditedUser({ ...editedUser, sync_with_google_calendar: value })}
                        disabled={!isEditing}
                    />
                </View>

                <View style={styles.infoContainer}>
                    <Text style={styles.infoText}>Дата создания: {formatDate(user?.created)}</Text>
                    <Text style={styles.infoText}>Дата изменения: {formatDate(user?.modified)}</Text>
                    <Text style={styles.infoText}>Роль: {user?.role === 'client' ? 'Клиент' : 'Сотрудник'}</Text>
                </View>

                <View style={styles.buttonContainer}>
                    {isEditing ? (
                        <>
                            <TouchableOpacity style={[styles.button, styles.saveButton]} onPress={handleSave}>
                                <Text style={styles.buttonText}>Сохранить</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={[styles.button, styles.cancelButton]} onPress={handleReset}>
                                <Text style={styles.buttonText}>Отмена</Text>
                            </TouchableOpacity>
                        </>
                    ) : (
                        <TouchableOpacity style={[styles.button, styles.editButton]} onPress={() => setIsEditing(true)}>
                            <Text style={styles.buttonText}>Редактировать</Text>
                        </TouchableOpacity>
                    )}
                </View>

                <View style={styles.actionButtonsContainer}>
                    <TouchableOpacity style={[styles.actionButton, styles.branchButton]} onPress={handleShowBranches}>
                        <Text style={styles.buttonText}>Наши филиалы</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </ImageBackground>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
        height: '100%',
        resizeMode: 'cover',
    },
    formContainer: {
        width: '90%',
        maxWidth: 400,
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        padding: 25,
        borderRadius: 15,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
    },
    input: {
        height: 50,
        borderColor: '#ddd',
        borderWidth: 1,
        marginBottom: 15,
        paddingHorizontal: 15,
        borderRadius: 8,
        backgroundColor: '#fff',
        fontSize: 16,
    },
    switchContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: 15,
    },
    switchLabel: {
        fontSize: 16,
        color: '#333',
    },
    infoContainer: {
        marginVertical: 15,
        padding: 10,
        backgroundColor: '#f8f9fa',
        borderRadius: 8,
    },
    infoText: {
        fontSize: 14,
        color: '#555',
        marginBottom: 5,
    },
    buttonContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginTop: 10,
        marginBottom: 20,
    },
    actionButtonsContainer: {
        marginTop: 10,
    },
    button: {
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
        justifyContent: 'center',
        minWidth: '48%',
    },
    editButton: {
        backgroundColor: '#007AFF',
        width: '100%',
    },
    saveButton: {
        backgroundColor: '#34C759',
    },
    cancelButton: {
        backgroundColor: '#FF3B30',
    },
    actionButton: {
        padding: 15,
        borderRadius: 8,
        alignItems: 'center',
        marginBottom: 10,
    },
    bookButton: {
        backgroundColor: '#5856D6',
    },
    createButton: {
        backgroundColor: '#FF9500',
    },
    branchButton: {
        backgroundColor: '#5AC8FA',
    },
    buttonText: {
        color: 'white',
        fontWeight: '600',
        fontSize: 16,
    },
});
