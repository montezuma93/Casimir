import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

export default class FormDialog extends React.Component {
  state = {
    open: false,
    base_activation_decay: 9,
    fraction_of_activation: 2,
    initial_activation_value: 1,
    noise: 0.5,
    dynamic_firing_threshold: 10,
    firing_threshold:10,
    noise_on: 0,
    spread_full_activation:0,
    use_only_complete_fragments:0
  };

  render() {
    return (
      <div>
        <Button variant="outlined" color="primary" onClick={this.handleClickOpen}>
          Adjust settings and start simulation
        </Button>
        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Subscribe</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Please set the settings for the simulation. 
              If you don't want to change something, just use the default values.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              value={this.state.base_activation_decay}
              onChange={this.onChange}
              id="name"
              name="base_activation_decay"
              ref="base_activation_decay"
              label="base_activation_decay"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              value={this.state.fraction_of_activation}
              id="name"
              name="fraction_of_activation"
              ref="fraction_of_activation"
              onChange={this.onChange}
              label="fraction_of_activation"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              name="initial_activation_value"
              ref="initial_activation_value"
              value={this.state.initial_activation_value}
              id="name"
              onChange={this.onChange}
              label="initial_activation_value"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              name="noise"
              ref="noise"
              value={this.state.noise}
              id="name"
              onChange={this.onChange}
              label="noise"
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              name="dynamic_firing_threshold"
              ref="dynamic_firing_threshold"
              value={this.state.dynamic_firing_threshold}
              id="name"
              onChange={this.onChange}
              label="dynamic_firing_threshold"
              fullWidth
            />
                        <TextField
              autoFocus
              margin="dense"
              name="firing_threshold"
              ref="firing_threshold"
              value={this.state.firing_threshold}
              id="name"
              onChange={this.onChange}
              label="firing_threshold"
              fullWidth
            />
                        <TextField
              autoFocus
              margin="dense"
              name="noise_on"
              ref="noise_on"
              value={this.state.noise_on}
              id="name"
              onChange={this.onChange}
              label="noise_on"
              fullWidth
            />
                        <TextField
              autoFocus
              margin="dense"
              name="spread_full_activation"
              ref="spread_full_activation"
              value={this.state.spread_full_activation}
              id="name"
              onChange={this.onChange}
              label="spread_full_activation"
              fullWidth
            />
                                    <TextField
              autoFocus
              margin="dense"
              name="use_only_complete_fragments"
              ref="use_only_complete_fragments"
              value={this.state.use_only_complete_fragments}
              id="name"
              onChange={this.onChange}
              label="use_only_complete_fragments"
              fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleClose} color="primary">
              Start Simulation
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
  
  handleClickOpen = () => {
    this.setState({ open: true });
  };



  

  handleClose = () => {
    this.setState({ open: false });
    console.log("here")
    return fetch('http://127.0.0.1:5000/create_mental_image', {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "context": [{
          "category": "Object",
          "name": this.props.data.objectName1,
          "type": this.props.data.objectCategory1
        },
        {
          "category": "Object",
          "name": this.props.data.objectName2,
          "type": this.props.data.objectCategory2
        },
        {
          "category": "RelationCategory",
          "type": this.props.data.relationCategory
        }
        ]
      })
    })
      .then((response) => response.json())
      .then((data) => this.props.setSMMs(data));
  }


  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }
}