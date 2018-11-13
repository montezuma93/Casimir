import React from 'react';
import ReactDOM from 'react-dom';
import SMMItem from './SMMItem';
import SMMTItem from './SMMTItem';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';

class Simulation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      objectCategory1: 'City',
      objectName1: '',
      objectCategory2: 'City',
      objectName2: '',
      relationCategory: 'Cardinal',
      smm: []
    };
  }
  static defaultProps = {
    relationCategories: ['Cardinal', 'Topological'],
    objectCategories: ['City', 'Country', 'Continent']
  }

  render() {
    let SMMItems;
    if (this.state.smm) {
      SMMItems = this.state.smm.map((singleSmm, id) => {
        return this.mapToSMMComponent(singleSmm, id);
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
      <div>
        <h3>Starter</h3>
        <form onSubmit={this.onSubmit}>
          <div>
            <label>RelationCategory</label><br />
            <Select ref="relationCategory" value={relationCategory} onChange={this.onChange} name='relationCategory'>
              {relationOptions}
            </Select>
          </div>
          <div>
            <label>Objects</label><br />
            <Select ref="objectCategory1" value={objectCategory1} onChange={this.onChange} name='objectCategory1'>
              {objectCategoriesOptions}
            </Select>
            <TextField type="text" ref="objectName1" value={objectName1} onChange={this.onChange} name='objectName1' />
          </div>
          <div>
            <label>Objects</label><br />
            <Select ref="objectCategory2" value={objectCategory2} onChange={this.onChange} name='objectCategory2'>
              {objectCategoriesOptions}
            </Select>
            <TextField type="text" ref="objectName2" value={objectName2} onChange={this.onChange} name='objectName2' />
          </div>
          <br />
          <Button onClick={this.onClick} title="Start">Start</Button>
          <br />
        </form>
        {SMMItems}
      </div>
    );
  }

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }

  onClick = (e) => {
    e.preventDefault();
    const { relationCategory, objectCategory1, objectName1, objectCategory2, objectName2, objects, relations } = this.state;
    console.log("here")
    return fetch('http://127.0.0.1:5000/put', {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "context": [{
          "category": "Object",
          "name": objectName1,
          "type": objectCategory1
        },
        {
          "category": "Object",
          "name": objectName2,
          "type": objectCategory2
        },
        {
          "category": "RelationCategory",
          "type": relationCategory
        }
        ]
      })
    })
      .then((response) => response.json())
      .then((data) => this.setState({
        smm: data.smm
      }));
  }

  mapToSMMComponent(singleSmm, id) {
    if (singleSmm.outerPart) {
      return (
        <SMMTItem key={id} smm={singleSmm} />
      );
    } else {
      return (
        <SMMItem key={id} smm={singleSmm} />
      );
    }

  }
}

export default Simulation;