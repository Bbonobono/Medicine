import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Button, Image, Alert, TouchableOpacity, Text} from 'react-native'
import * as ImagePicker from 'expo-image-picker';
import { Camera, CameraType, takePictureAsync } from 'expo-camera';
import * as MediaLibrary from 'expo-media-library';

// import { MobileModel } from 'react-native-pytorch-core';
const UploadImage = ({route, navigation}) => {
  const pressHandler = () => {
    navigation.goBack();
  }
  const pressHandler1 = () => {
    navigation.navigate('Result');
  }
  const pressCamera = () => {
    navigation.navigate('CameraPhoto');
  }
 

  // Image Upload
  
  const [hasPermission, setHasPermission] = useState(null);
  const [showCamera, setShowCamera] = useState(false);
  const [type, setType] = useState(CameraType.back);
  const [images, setImage] = useState(null);
  // camera ref to access camera
  const cameraRef = useRef(null);


  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  // useEffect(() => {
  //   fetch("http://172.30.1.60:5000/image", {
  //     method : 'GET'
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //       console.log(data)
  //       // setImage(data.uri);
  //     })
  // },[])

  const pickImage = async () => {
    // No permissions request is necessary for launching the image library
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });
    // const formData = new FormData();
    // formData.append('imageInfo', {
    //   uri: result.assets[0].uri,
    //   type: result.assets[0].type,
    //   name: result.assets[0].fileName,
    // })
    
    // console.log("image pick in Library: ", result.assets);

    if (!result.canceled) {
      setImage(result.assets[0].uri);
      
    //   let res = await fetch(
    //     'http://172.30.1.60:5000/image', {
    //       method: 'POST',
    //       headers:{
    //         Accept: 'application/json',
    //         'Content-Type':'application/json', 
    //       },
    //       body: JSON.stringify({
    //         uri: result.assets[0].uri,
    //         type: result.assets[0].type,
    //         name: result.assets[0].fileName,
    //       }),
    //     }
    //   )
    //   .then((response) => response.json())
    //   .then((responseData) => {
    //     console.log(responseData, 'responseJson')
    //     setImage(responseData.uri)
    //   })
    }
    
  };

  const takePhoto = async() => {
    if (cameraRef) {
      console.log("in take picture");
      try {
        let photo = await cameraRef.current.takePictureAsync({
          allowsEditing: true,
          aspect: [4,3],
          quality: 1,
        });
        const asset = await MediaLibrary.createAssetAsync(photo.uri);
        return photo;
      } catch (e) {
        console.log(e);
      }
    }
  };

  //   if (route.params){
  //     const img = route.params;
  //     // console.log("img: ",img)
  //     setImage(img.uri);
  //     console.log(img.uri)

  //     console.log(images)
  //   }
  // });

  return (
    <View style={{flex:1}}>
      {showCamera ? (<Camera style={{flex: 1,}} type={type} ref={cameraRef}>
        
        <View style={cam_styles.buttonContainer}>
        <View style = {
            { 
              "flexDirection": "row",
              "alignSelf": "flex-end",
              "alignItems": "center",
              "paddingTop": 5,
              "width": 390,
              "height": 100,
              "backgroundColor": "rgba(255, 255, 255, 255)"
            }
          } >
          <TouchableOpacity
            style={cam_styles.button}
            onPress={() => {
              setType(type === CameraType.back ? CameraType.front : CameraType.back);
            }}>
            
            <Image style = {
            {
              "width": 24,
              "height": 24,
              "marginBottom":60,
              "marginLeft":50
            }
            }
            source = {
              require('../assets/circle.png')
            }/>
          </TouchableOpacity>
          <TouchableOpacity
            style={cam_styles.button}
            onPress={async() => {
              const r = await takePhoto();
              setImage(r.uri)
              setShowCamera(false)
              // Alert.alert("DEBUG", JSON.stringify(r));
              // navigation.navigate('UploadImage',{'img':r})
            }}
            >
            <View style = {
              {
                "alignItems": "center",
                "paddingTop": 9,
                "marginBottom":50,
                "width": 100,
                "height": 42,
                "borderRadius": 21,
                "backgroundColor": "rgba(67, 175, 244, 255)"
              }
            } >
            <Image style = {
            {
              "width": 24,
              "height": 24,
              "marginBottom":60
            }
            }
            source = {
              require('../assets/camera.png')
            }/>
            </View>
          </TouchableOpacity>
          <TouchableOpacity
            style={cam_styles.button}
            onPress={async() => {
              setShowCamera(false);
            }}>
            <Image style = {
            {
              "width": 24,
              "height": 24,
              "marginBottom":60,
              "marginRight":50
            }
            }
            source = {
              require('../assets/back.png')
            }/>
          </TouchableOpacity>
        </View>
        </View>
      </Camera>
      ) : (
      <View style={styles.container}>
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center'}}>
        <Image style = {
        {
          // "marginStart": 20,
          "width": 180,
          "height": 101.25
        }
        }
        source = {
            require('../assets/pillm.png')
        }/>
          <TouchableOpacity onPress={() => setShowCamera(true)}>
            <View style = {
              {
                "alignItems": "center",
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
            } >Take Picture</Text>
            </View>
            </TouchableOpacity>
            <TouchableOpacity onPress={pickImage}>
            <View style = {
              {
                "alignItems": "center",
                "paddingTop": 12,
                "margin":0,
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
            } >Select Image</Text>
            </View>
            </TouchableOpacity>
          {images && <Image source={{ uri: images }} style={{ 
            marginTop: 20,
            width: 350, 
            height: 350,
            borderRadius: 30 }} onLoadEnd={() => alert('Image Loaded!!')} resizeMethod='contain'/>}
          
        </View>
        <View style={{marginBottom:30}}>
        <TouchableOpacity onPress={pressHandler1}>
          <View style = {
            {
              "alignItems": "center",
              "paddingTop": 12,
              "margin":20,
              "width": 212,
              "height": 42,
              "borderRadius": 21,
              "backgroundColor": "rgba(70, 83, 107, 255)"
            }
          } >
          
          <Text style = {
            {
              "fontFamily": "NanumSquareOTF",
              "fontSize": 16,
              "textAlign": "center",
              "color": "rgba(255, 255, 255, 255)"
            }
          } >Submit</Text>
          </View>
          </TouchableOpacity>
        </View>
      </View>
      )}
      
    </View>
    
  );
}
const cam_styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    // alignItems: 'center',
    // justifyContent: 'center',
  },
  buttonContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'row',
    margin: 0,
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
  }
});

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default UploadImage;