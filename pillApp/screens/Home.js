import { StatusBar } from 'expo-status-bar';
import { Button, StyleSheet, Text, View } from 'react-native';

export default function Home({navigation}){
  const pressHandler = () => {
      navigation.navigate('UploadImage');
  }

  return (
    <View style={styles.container}>
      <Text style = {styles.TitleText}>Pillm</Text>
      <Button
        title='Start'
        onPress={pressHandler}
      ></Button>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  TitleText: {
    textAlign : 'center',
    marginVertical : 8,
    fontSize: 40
  },

});
