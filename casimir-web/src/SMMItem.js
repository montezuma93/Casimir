import React from 'react';
import { ImageBackground, Text } from 'react-native';
import ReactDOM from 'react-dom';

class SMMItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            innerNorth: this.props.smm.innerNorth,
            innerSouth: this.props.smm.innerSouth,
            innerWest: this.props.smm.innerWest,
            innerEast: this.props.smm.innerEast,
            outerNorth: '',
            outerSouth: '',
            outerWest: '',
            outerEast: '',
            middle: this.props.smm.middle
        }
    }

    render() {
        return (
            <ImageBackground
                source={require('./SMM.jpg')}
                style={{
                    height: 500,
                    width: 500,
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
                        top: 125,
                        left: 250
                    }}
                >
                    {this.state.innerNorth}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 375, 
                        left: 250
                    }}
                >
                    {this.state.innerSouth}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 250,
                        left: 125
                    }}
                >
                    {this.state.innerWest}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative', 
                        top: 250, 
                        left: 350
                    }}
                >
                    {this.state.innerEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 225,
                        left: 225
                    }}
                >
                    {this.state.middle}
                </Text>
            </ImageBackground>
        );
    }
}

export default SMMItem;