import React from 'react';
import { ImageBackground, Text } from 'react-native';
import ReactDOM from 'react-dom';

class SMMTItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            outerPart: this.props.smm.outerPart ? this.props.smm.outerPart : '',
            innerPart: this.props.smm.innerPart ? this.props.smm.innerPart : ''
        }
    }

    render() {
        return (
            <ImageBackground
                source={require('./SMMTopology.jpg')}
                style={{
                    height: 250,
                    width: 250,
                    position: 'relative',
                    top: 7,
                    left: 5
                }}
            >
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 25,
                        left: 125
                    }}
                >
                    {this.state.outerPart}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 125,
                        left: 125
                    }}
                >
                    {this.state.innerPart}
                </Text>
            </ImageBackground>
        );
    }
}

export default SMMTItem;