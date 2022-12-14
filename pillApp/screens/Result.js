import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, FlatList, Pressable, Image, SafeAreaView } from 'react-native';

export default function Result({navigation}) {
    const DetailPage = (props) => {
        navigation.navigate('Detail',{'pillItem':props});
    };
    
    
    const [isLoading, setLoading] = useState(false);
    const [data, setData] = useState({});

    useEffect(() => {
      fetch('http://172.30.1.51:8000/',{ // fast api 주소 따라서 변경해야함.
        Accept: 'application/json',
      })
      .then((response) => response.json())
      .then((json) => setData(json))
      .catch((error) => console.error(error))
      .finally(() => setLoading(false));
    },[])
    
    const ListItem = ({item, name, shape, color, image}) => {
      return (
        <Pressable style={styles.listItem} onPress={() => DetailPage(item)}>
          <View style={styles.pillContainer}>
            <Image
              source={{uri: image}}
              style={styles.listImage}
            />
            <View style={styles.pillContent}>
              <Text style={{fontSize: 30, fontWeight: '700', marginBottom: 5}}>{name}</Text>
              <Text style={{fontSize: 20, fontWeight: '300'}}>{shape} / {color}</Text>
            </View>
          </View>
          
        </Pressable>
      );
    };
    const ListHeaderComponent = (props) => {
      return (
        <View
          style={{
            height: 40,
            marginTop: 20,
          }}
        >
          <Text style={{marginLeft: 20,fontSize: 20}}>총 <Text style={{fontWeight: 'bold', fontSize: '30', color:'#3478F6'}}>{data.length}</Text>건의 검색결과가 있습니다.</Text>
        </View>
          
      )
    };
    return (
      <SafeAreaView>
        {isLoading ? <Text>Loading...</Text> :
        (<FlatList
          data={data}
          ListHeaderComponent={ListHeaderComponent}
          renderItem={({item}) => {
            return <ListItem 
                      item = {item}
                      name = {item.NAME}
                      shape = {item.MY}
                      color = {item.COLOR}
                      image = {item.IMAGE}
                    />;
          }}
          keyExtractor={item => item.PK}
        />)}
      </SafeAreaView>
    );
  }
  
  const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    listImage: {
      width: 120,
      height: '100%',
      borderRadius: 10,
      alignItems: 'center',
      justifyContent: 'center',
    },
    listItem:{
      height : '100%',
      marginBottom: 1,
      paddingHorizontal: 15,
      // flex: 1,
    },
    pillContainer: {
      flexDirection: 'row',
      alignContent: 'center',
      padding: 10,
      borderRadius: 10,
      backgroundColor: '#fff',
      // flex: 1,
    },
    pillContent:{
      marginLeft: 20,
      // marginRight: 20,
      justifyContent:'center',
      overflow: 'visible',
      flex: 1,
    },
  });