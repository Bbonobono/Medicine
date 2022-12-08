import React from "react";
import { StyleSheet, View } from "react-native";

const LayoutContainer = ({children}) => {
    return <View style={styles.container}>{children}</View>;
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        borderWidth: 5,
        margin: 5,
    },
});

export default LayoutContainer;
