import React from 'react';
import { ImageBackground, Text } from 'react-native';

class TopologicalSpatialMentalModelItem extends React.Component {
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
                source={require('./TopologicalSpatialMentalModel.jpg')}
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
                        top: 26,
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
                        top: 108,
                        left: 122
                    }}
                >
                    {this.state.innerPart}
                </Text>
            </ImageBackground>
        );
    }
}

export default TopologicalSpatialMentalModelItem;