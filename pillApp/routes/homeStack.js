import React, { useState } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import Home from '../screens/Home'
import UploadImage from '../screens/UploadImage'
import Result from '../screens/Result'
import Detail from '../screens/Detail'

const Stack = createStackNavigator();

export default function HomeStack() {
    return (
        <Stack.Navigator>
            {/* <Stack.Screen name="Home" component={Home} options={{headerShown : false,}} /> */}
            <Stack.Screen name="UploadImage" component={UploadImage} options={{headerShown : false,}} />
            <Stack.Screen name="Result" component={Result} options={{headerShown : false,}}/>
            
            <Stack.Screen name="Detail" component={Detail} options={{headerShown : false,}}/>
        </Stack.Navigator>
    );
}