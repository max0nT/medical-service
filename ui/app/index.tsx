import { NavigationContainer, NavigationIndependentTree } from "@react-navigation/native";
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import Login from "../components/auth/login"
import SignUp from "@/components/auth/sign_up";

const Stack = createNativeStackNavigator();

export default function Index() {
  return (
    <NavigationIndependentTree>
      <NavigationContainer>
          <Stack.Navigator
          >
            <Stack.Screen
              options={{ headerShown: false }}
              name="Login"
              component={Login}
            >
            </Stack.Screen>
            <Stack.Screen
              options={{ headerShown: false }}
              name="SignUp"
              component={SignUp}
            >
            </Stack.Screen>
          </Stack.Navigator>
      </NavigationContainer>
    </NavigationIndependentTree>
  );
}
