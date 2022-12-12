import { StatusBar } from 'expo-status-bar';
import { Button, StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';

export default function Home({navigation}){
  const pressHandler = () => {
      navigation.navigate('UploadImage');
  }

  return (
    <View style={styles.container}>
      <Image style = {
        {
          // "marginStart": 20,
          "width": 180,
          "height": 101.25
        }
        }
        source = {
            require('../assets/pillm.png')
        }
      />
      <TouchableOpacity onPress={pressHandler}>
      <View style = {
        {
          "alignItems": "center",
          // "paddingStart": 61,
          "paddingTop": 12,
          "margin":20,
          "width": 212,
          "height": 42,
          "borderRadius": 21,
          "backgroundColor": "rgba(67, 175, 244, 255)"
        }
      } >
      
      <Text style = {
        {
          "fontFamily": "NanumSquareOTF",
          "fontSize": 16,
          "textAlign": "center",
          "color": "rgba(255, 255, 255, 255)"
        }
      } >Start</Text>
      </View>
      </TouchableOpacity>
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
