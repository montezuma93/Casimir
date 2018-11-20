import React from 'react';
import { ImageBackground, Text } from 'react-native';
import ReactDOM from 'react-dom';

class SMMItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            north: this.props.smm.north,
            south: this.props.smm.south,
            west: this.props.smm.west,
            east: this.props.smm.east,
            northEast: this.props.smm.northEast,
            northWest: this.props.smm.northWest,
            southWest: this.props.smm.southWest,
            southWest: this.props.smm.southWest,
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
                    {this.state.north}
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
                    {this.state.south}
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
                    {this.state.west}
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
                    {this.state.east}
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
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 125,
                        left: 350
                    }}
                >
                    {this.state.northEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 225,
                        left: 125
                    }}
                >
                    {this.state.northWest}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 375,
                        left: 350
                    }}
                >
                    {this.state.southEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'relative',
                        top: 375,
                        left: 125
                    }}
                >
                    {this.state.southWest}
                </Text>
            </ImageBackground>
        );
    }
}

export default SMMItem;