import React from 'react';
import ReactDOM from 'react-dom';
import Adder from './Adder'
import Simulation from './Simulation'

class Casimir extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render() {
        return (
            <div className="class" style={{marginLeft:'10rem'}}>
            <h1>UI for Casimir Simulation</h1>
            <Adder/>
            <Simulation/>
            </div>
        );
    }



}

export default Casimir;