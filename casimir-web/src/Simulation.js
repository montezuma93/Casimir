import React from 'react';
import CardinalSpatialMentalModelItem from './CardinalSpatialMentalModelItem';
import TopologicalSpatialMentalModelItem from './TopologicalSpatialMentalModelItem';
import Button from '@material-ui/core/Button';
import Select from '@material-ui/core/Select';
import TextField from '@material-ui/core/TextField';
import FormDialog from './FormDialog';

class Simulation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      objectCategory1: 'City',
      objectName1: '',
      objectCategory2: 'City',
      objectName2: '',
      relationCategory: 'Cardinal',
      spatialMentalModels: []
    };
  }
  static defaultProps = {
    relationCategories: ['Cardinal', 'Topological'],
    objectCategories: ['City', 'Country', 'Continent', 'Miscellaneous']
  }

  render() {
    let SpatialMentalModelItems;
    if (this.state.spatialMentalModels) {
      SpatialMentalModelItems = this.state.spatialMentalModels.map((spatialMentalModel, id) => {
        return this.mapToSpatialMentalModelComponent(spatialMentalModel, id);
      });
    }

    const { relationCategory, objectCategory1, objectName1, objectCategory2, objectName2 } = this.state;
    let relationOptions = this.props.relationCategories.map(relation => {
      return <option key={relation} value={relation}>{relation}</option>
    });
    let objectCategoriesOptions = this.props.objectCategories.map(category => {
      return <option key={category} value={category}>{category}</option>
    });

    return (
      <div style={{ marginLeft: '4rem', marginTop: '4rem' }}>
        <Button onClick={this.resetSimulation} variant="contained" title="Reset Simulation" style={{ marginBottom: '2rem', color: '#8B0000' }}>
          Reset Simulation</Button>
        <h3>Starter</h3>
        <form onSubmit={this.onSubmit}>
          <div>
            <label>RelationCategory</label><br />
            <Select ref="relationCategory" value={relationCategory} onChange={this.onChange} name='relationCategory' style={{ width: '9rem' }}>
              {relationOptions}
            </Select>
          </div>
          <div style={{ marginTop: '1rem' }}>
            <label>Object 1</label><br />
            <Select ref="objectCategory1" value={objectCategory1} onChange={this.onChange} name='objectCategory1' style={{ width: '9rem' }}>
              {objectCategoriesOptions}
            </Select>
            <TextField type="text" ref="objectName1" value={objectName1} onChange={this.onChange} name='objectName1' style={{ marginLeft: '2rem' }} />
          </div>
          <div style={{ marginTop: '1rem' }}>
            <label>Object 2</label><br />
            <Select ref="objectCategory2" value={objectCategory2} onChange={this.onChange} name='objectCategory2' style={{ width: '9rem' }}>
              {objectCategoriesOptions}
            </Select>
            <TextField type="text" ref="objectName2" value={objectName2} onChange={this.onChange} name='objectName2' style={{ marginLeft: '2rem' }} />
          </div>
          <br />
          <FormDialog data={this.state} setSpatialMentalModels={this.handleSpatialMentalModels} style={{ height: '1000rem' }} />
          <br />
        </form>
        <div style={{ display: 'inline-block' }}>{SpatialMentalModelItems}</div>

      </div>
    );
  }

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleSpatialMentalModels = (data) => {
    this.setState({ spatialMentalModels: data.smm })
  }

  resetSimulation = (e) => {
    this.setState({ objectName1: '', objectName2: '', spatialMentalModel: [] })
    return fetch('http://127.0.0.1:5000/reset_simulation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      })
    });
  }

  mapToSpatialMentalModelComponent(spatialMentalModel, id) {
    if (spatialMentalModel.outerPart !== null) {
      return (
        <TopologicalSpatialMentalModelItem key={id} spatialMentalModel={spatialMentalModel} />
      );
    } else {
      return (
        <CardinalSpatialMentalModelItem key={id} spatialMentalModel={spatialMentalModel} />
      );
    }

  }
}

export default Simulation;