import React from 'react';
import { ImageBackground, Text } from 'react-native';

class CardinalSpatialMentalModelItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            north: this.props.spatialMentalModel.north ? this.props.spatialMentalModel.north : '',
            south: this.props.spatialMentalModel.south ? this.props.spatialMentalModel.south : '',
            west: this.props.spatialMentalModel.west ? this.props.spatialMentalModel.west : '',
            east: this.props.spatialMentalModel.east ? this.props.spatialMentalModel.east : '',
            northEast: this.props.spatialMentalModel.northEast ? this.props.spatialMentalModel.northEast : '',
            northWest: this.props.spatialMentalModel.northWest ? this.props.spatialMentalModel.northWest : '',
            southEast: this.props.spatialMentalModel.southEast ? this.props.spatialMentalModel.southEast : '',
            southWest: this.props.spatialMentalModel.southWest ? this.props.spatialMentalModel.southWest : '',
            middle: this.props.spatialMentalModel.middle ? this.props.spatialMentalModel.middle : ''
        }
    }

    render() {
        return (
            <ImageBackground
                source={require('./CardinalSpatialMentalModel.jpg')}
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
                        position: 'absolute',
                        top: 58,
                        left: 125
                    }}
                >
                    {this.state.north}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 172,
                        left: 125
                    }}
                >
                    {this.state.south}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 110,
                        left: 58
                    }}
                >
                    {this.state.west}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 110,
                        left: 180
                    }}
                >
                    {this.state.east}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 112,
                        left: 122
                    }}
                >
                    {this.state.middle}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 58,
                        left: 180
                    }}
                >
                    {this.state.northEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 58,
                        left: 58
                    }}
                >
                    {this.state.northWest}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 172,
                        left: 180
                    }}
                >
                    {this.state.southEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 172,
                        left: 58
                    }}
                >
                    {this.state.southWest}
                </Text>
            </ImageBackground>
        );
    }
}

export default CardinalSpatialMentalModelItem;