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
            outer_north: this.props.spatialMentalModel.outer_north ? this.props.spatialMentalModel.outer_north : '',
            outer_south: this.props.spatialMentalModel.outer_south ? this.props.spatialMentalModel.outer_south : '',
            outer_west: this.props.spatialMentalModel.outer_west ? this.props.spatialMentalModel.outer_west : '',
            outer_east: this.props.spatialMentalModel.outer_east ? this.props.spatialMentalModel.outer_east : '',
            outer_northEast: this.props.spatialMentalModel.outer_northEast ? this.props.spatialMentalModel.outer_northEast : '',
            outer_northWest: this.props.spatialMentalModel.outer_northWest ? this.props.spatialMentalModel.outer_northWest : '',
            outer_southEast: this.props.spatialMentalModel.outer_southEast ? this.props.spatialMentalModel.outer_southEast : '',
            outer_southWest: this.props.spatialMentalModel.outer_southWest ? this.props.spatialMentalModel.outer_southWest : '',
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
                        top: 76,
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
                        top: 35,
                        left: 125
                    }}
                >
                    {this.state.outer_north}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 154,
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
                        top: 196,
                        left: 125
                    }}
                >
                    {this.state.outer_south}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 110,
                        left: 78
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
                        left: 36
                    }}
                >
                    {this.state.outer_west}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 110,
                        left: 160
                    }}
                >
                    {this.state.east}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 110,
                        left: 204
                    }}
                >
                    {this.state.outer_east}
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
                        top: 76,
                        left: 160
                    }}
                >
                    {this.state.northEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 35,
                        left: 204
                    }}
                >
                    {this.state.outer_northEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 76,
                        left: 78
                    }}
                >
                    {this.state.northWest}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 35,
                        left: 36
                    }}
                >
                    {this.state.outer_northWest}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 154,
                        left: 160
                    }}
                >
                    {this.state.southEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 196,
                        left: 204
                    }}
                >
                    {this.state.outer_southEast}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 154,
                        left: 78
                    }}
                >
                    {this.state.southWest}
                </Text>
                <Text
                    style={{
                        fontWeight: 'bold',
                        color: 'black',
                        position: 'absolute',
                        top: 196,
                        left: 36
                    }}
                >
                    {this.state.outer_southWest}
                </Text>
            </ImageBackground>
        );
    }
}

export default CardinalSpatialMentalModelItem;