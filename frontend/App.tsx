import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { LoginScreen }  from "./components/Login"
import { SignUpScreen } from './components/SignUp';
import { ProfileScreen } from './components/Profile';
import { EditProfileScreen } from './components/EditProfile';
import { AppointmentsScreen } from './components/Appointments';


const Stack = createNativeStackNavigator();

export default function App() {

 return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
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
