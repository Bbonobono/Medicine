import React, { useState } from 'react';
import Navigator from './routes/homeStack'
import { NavigationContainer } from '@react-navigation/native';
import * as Font from 'expo-font';
import AppLoading from 'expo-app-loading';

export default function App() {
  const [isReady, setIsReady] = useState(false);
 
  const getFonts = async () => {
    await Font.loadAsync({
    'NanumSquareOTF': require('./assets/fonts/NanumSquareR.otf'),
  });
  };  
  
  return isReady? (
     <NavigationContainer>
       <Navigator />
     </NavigationContainer>
  ) : (
    <AppLoading
            startAsync={getFonts}
              onFinish={() => setIsReady(true)}
              onError={() => {}}
        />
  );
  }