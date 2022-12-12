import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, FlatList, Pressable, Image } from 'react-native';


// const pills = [
//   {
//     id: 1,
//     name: "엘스테인캡슐",
//     shape: "장방형",
//     color: "초록",
//     image: "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/1Mxwka5v1Ov",
//     effect: '급ㆍ만성 호흡기질환에서의 점액용해 및 거담',
//     usage: '성인: 에르도스테인으로서 1회 300 mg을 1일 2～3회 경구투여한다.\n급성 호흡기질환에 투여 시 연속으로 10일 이상 투여하지 않는다.',
//   },
// ];

const pills = [
  {
    'id': 1,
    'name': "엘스테인캡슐",
    'shape': "장방형",
    'color': "초록",
    'image': "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/1Mxwka5v1Ov",
    'effect': '급ㆍ만성 호흡기질환에서의 점액용해 및 거담',
    'usage': '성인: 에르도스테인으로서 1회 300 mg을 1일 2～3회 경구투여한다.\n급성 호흡기질환에 투여 시 연속으로 10일 이상 투여하지 않는다.',
  },
  // {
  //   id: 2,
  //   name: "그린엠캡슐",
  //   shape: "장방형",
  //   color: "초록",
  //   image: "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/147428243808800017",
  //   effect: '비만 또는 과체중시 체중감량(줄임) 보조제',
  //   usage: '성인 : 1회 1 ∼ 2캡슐, 1일 3회 식사 중에 큰 컵으로 물 한 컵과 함께 복용한다.',
  // },
  // {
  //   id: 3,
  //   name: "뉴에르도테캡슐",
  //   shape: "장방형",
  //   color: "초록",
  //   image: "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/148362082166500066",
  //   effect: '급ㆍ만성 호흡기질환에서의 점액용해 및 거담',
  //   usage: '성인: 에르도스테인으로서 1회 300 mg을 1일 2～3회 경구투여한다.\n급성 호흡기질환에 투여 시 연속으로 10일 이상 투여하지 않는다.',
  // },
];

export default function Result({navigation}) {
    const pressHandler = () => {
      navigation.goBack();
    }
    const DetailPage = (props) => {
        navigation.navigate('Detail',{'pillItem':props});
    };
    
    
    const [isLoading, setLoading] = useState(false);
    const [data, setData] = useState({});

    useEffect(() => {
      fetch('http://172.30.1.20:8000/',{
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
      <View>
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