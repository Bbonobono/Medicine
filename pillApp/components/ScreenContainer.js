import React from "react";
import { SafeAreaView, Text } from "react-native";

const ScreenContainer = ({title, children}) => {
    return (
        <SafeAreaView style={{flex:1, flexDirection: 'column'}}>
            <Text style={{marginBottom: 10, textAlign: 'center', fontSize: 20}}>
                {title}
            </Text>
            {children}
        </SafeAreaView>
    );
}

export default ScreenContainer;
