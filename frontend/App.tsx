import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { LoginScreen }  from "./components/Login"
import { SignUpScreen } from './components/SignUp';
import { ProfileScreen } from './components/Profile';
import { EditProfileScreen } from './components/EditProfile';
import { AppointmentsScreen } from './components/Appointments';
import { medicalTheme } from './theme/medicalTheme';


const Stack = createNativeStackNavigator();

export default function App() {

 return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Login"
        screenOptions={{
          headerShadowVisible: false,
          headerStyle: {
            backgroundColor: medicalTheme.colors.background,
          },
          headerTintColor: medicalTheme.colors.text,
          headerTitleStyle: {
            fontWeight: "700",
          },
          contentStyle: {
            backgroundColor: medicalTheme.colors.background,
          },
        }}
      >
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="SignUp" component={SignUpScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
        <Stack.Screen
          name="EditProfile"
          component={EditProfileScreen}
          options={{ title: 'Редактирование профиля' }}
        />
        <Stack.Screen
          name="Appointments"
          component={AppointmentsScreen}
          options={{ title: 'Запись на приём' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
