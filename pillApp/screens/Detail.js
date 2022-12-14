import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View, ActivityIndicator, Button, FlatList } from 'react-native';
import PillsDetail from '../components/PillsDetail';
import ScreenContainer from '../components/ScreenContainer';

export default function Detail({route, navigation}) {
    const pillItem = route.params;
    console.log(pillItem);

    return (
      <ScreenContainer>
        <PillsDetail 
          name = {pillItem.pillItem.NAME}
          effect = {pillItem.pillItem.EFFECT}
          usage = {pillItem.pillItem.USAGE}
          image = {pillItem.pillItem.IMAGE}
          style={styles.listItem}
        />
      </ScreenContainer>
    );
  }
  
  const styles = StyleSheet.create({
    listItem: {
      borderRadius: 0,
    },
  
  });