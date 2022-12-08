import React from "react"
import { SafeAreaView, ImageBackground, StyleSheet, Text, View, ScrollView } from "react-native"
import LayoutContainer from "./LayoutContainer";


const PillsDetail = ({image, name, effect, usage, style}) => {
    // const imageUrl = require(`../assets/images${image}`)
    return (
        <SafeAreaView style={[listItemStyle.container, style]}>
            <ImageBackground
                source={{uri:image}}
                style={listItemStyle.image}
            /> 

            <ScrollView style={{padding: 20}}>
                <View style={listItemStyle.menuView}>
                    <Text style={listItemStyle.menu}>의약품명</Text>
                    <Text style={listItemStyle.pillName}>{name}</Text>
                </View>
                <View style={listItemStyle.menuView}>
                    <Text style={listItemStyle.menu}>효능 및 효과</Text>
                    <Text style={listItemStyle.content}>
                        {effect}
                        
                    </Text>
                </View>
                <View style={listItemStyle.menuView}>
                    <Text style={listItemStyle.menu}>용법 및 용량</Text>
                    <Text style={listItemStyle.content}>
                        {usage}
                    </Text>
                </View>
            </ScrollView> 
        </SafeAreaView>
    );
};

const listItemStyle = StyleSheet.create({
    container: {
        marginBottom: 20,
        borderRadius: 10,
        overflow: 'scroll',
    },
    pillName: {
        fontSize: 40,
        fontWeight: '500',
        padding: 5,
    },
    image: {
        alignSelf: 'stretch',
        height: 200,
        padding: 20,
    },
    menuView:{
        paddingBottom: 15,
    },
    menu: {
        fontSize: 20,
        fontWeight: '700',
        color: '#3478F6',
    },
    content: {
        fontSize: 20,
        padding: 5,
    },
});

export default PillsDetail;