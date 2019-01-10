import React from 'react';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';

class Adder extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      relationName: 'South',
      objectName1: '',
      objectCategory1: 'City',
      objectName2: '',
      objectCategory2: 'City',
      relations: [],
      objects: []
    };
  }

  static defaultProps = {
    relations: ['South', 'North', 'East', 'West', 'NorthWest', 'NorthEast', 'SouthWest', 'SouthEast', 'PartOf'],
    objectCategories: ['City', 'Country', 'Continent']
  }

  render() {
    const { relationName, objectCategory1, objectName1, objectCategory2, objectName2 } = this.state;
    let relationOptions = this.props.relations.map(relation => {
      return <option key={relation} value={relation}>{relation}</option>
    });
    let objectCategoriesOptions = this.props.objectCategories.map(category => {
      return <option key={category} value={category}>{category}</option>
    });
    return (
      <div style={{ marginLeft: '4rem' }}>
        <div>
          <h3>Add KnowledgeFragment</h3>
          <div style={{ marginTop: '1rem' }}>
            <label>Relation</label><br />
            <Select ref="relationName" value={relationName} onChange={this.onChange} name='relationName'>
              {relationOptions}
            </Select>
          </div>
          <div style={{ marginTop: '1rem' }}>
            <label>Object 1</label><br />
            <Select ref="objectCategory1" value={objectCategory1} onChange={this.onChange} name='objectCategory1'>
              {objectCategoriesOptions}
            </Select>
            <TextField type="text" ref="objectName1" value={objectName1} onChange={this.onChange} name='objectName1' style={{ marginLeft: '2rem' }} />
          </div>
          <div style={{ marginTop: '1rem' }}>
            <label>Object 2</label><br />
            <Select ref="objectCategory2" value={objectCategory2} onChange={this.onChange} name='objectCategory2'>
              {objectCategoriesOptions}
            </Select>
            <TextField type="text" ref="objectName2" value={objectName2} onChange={this.onChange} name='objectName2' style={{ marginLeft: '2rem' }} />
          </div>
          <Button onClick={this.onClick} variant="contained" title="Post Knowledge" style={{ marginTop: '1rem', color: '#00BFFF' }}>Submit Data</Button>
        </div>
      </div>
    );
  }

  onClick = (e) => {
    this.setState({ objectName1: '', objectName2: '' })
    const { relationName, objectCategory1, objectName1, objectCategory2, objectName2 } = this.state;
    console.log("submit")
    return fetch('http://127.0.0.1:5000/save_knowledge_fragment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "relation": relationName,
        "objects": [
          {
            "name": objectName1,
            "type": objectCategory1
          },
          {
            "name": objectName2,
            "type": objectCategory2,
          }
        ]
      })
    });
  }

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }
}

export default Adder;