import React, { Component } from 'react'
import {StyleSheet, Text, View, Button, PushNotificationIOS} from 'react-native'
import TwitterAuth from 'tipsi-twitter'
import Amplify, { Analytics, API, Logger } from 'aws-amplify';
import aws_exports from './aws-exports';
import { PushNotification } from 'aws-amplify-react-native';

TwitterAuth.init({
  twitter_key: '<your key here>',
  twitter_secret: '<your secret here>',
})

export default class Root extends Component {
  state = {
    twitterUserName: '',
    errorMessage: '',
  }

  handleCustomLoginPress = async () => {
    try {
      const result = await TwitterAuth.login()
      console.log("result", result)

      const appConfig = {
        region: aws_exports.aws_project_region,
      }

      // manually configure analytics module because we want to set custom endpoint ID      
      Amplify.configure({
        Auth: {
            identityPoolId: aws_exports.aws_cognito_identity_pool_id, 
            region: aws_exports.aws_project_region
        },
        Analytics:
        {
          endpointId: result.userName,
          appId: aws_exports.aws_mobile_analytics_app_id,
          region: aws_exports.aws_project_region,
        }
      });

      Analytics.updateEndpoint({
          // Customized userId
          UserId: result.userName
      })

      PushNotification.configure(aws_exports);
      
      // get the registration token
      PushNotification.onRegister((token) => {
        console.log('in app registration', token);
      });

      this.setState({
        errorMessage: '',
        twitterUserName: result.userName,
      })
    }
    catch (error) {
      this.setState({
        errorMessage: error.message,
        twitterUserName: '',
      })
    }
  }

  render() {
    const { twitterUserName, errorMessage } = this.state

    return (
      <View style={styles.container}>
        <Button
          title="Login Button"
          accessible
          accessibilityLabel="loginButton"
          onPress={this.handleCustomLoginPress}
        />
        <Text
          accessibilityLabel="twitter_response"
          style={styles.instructions}>
          { twitterUserName !== '' ? `twitterUserName: ${twitterUserName}` : ''}
        </Text>
        <Text
          accessibilityLabel="error_message"
          style={styles.error}>
          {errorMessage}
        </Text>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
  error: {
    fontSize: 20,
    textAlign: 'center',
    color: '#FF0000',
  },
  button: {
    marginBottom: 20,
    padding: 20,
  },
})
