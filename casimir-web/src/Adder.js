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
      <div>
        <div>
          <h3>Add KnowledgeFragment</h3>
          <div>
            <label>RelationCategory</label><br />
            <Select ref="relationName" value={relationName} onChange={this.onChange} name='relationName'>
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
          <Button onClick={this.onClick} title="Post Knowledge">Submit Data</Button>
        </div>
        <div>
          <Button onClick={this.getAllData} title="GetAllData">Get All Data</Button>
        </div>
      </div>
    );
  }
  getAllData = (e) => {
    e.preventDefault();
    const { objects, relations } = this.state;
    return fetch('http://127.0.0.1:5000/show_all_knowledge_fragments', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then((response) => response.json())
      .then((data) => this.setState({
        relations: data.relations,
        objects: data.objects
      }));
  }

  onClick = (e) => {
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