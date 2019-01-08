import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';

//BASE_ACTIVATION_DECAY = -0.2
//INITIAL_ACTIVATION_VALUE = 0.8
//BASE_ACTIVATION_DECAY = -0.86
//INITIAL_ACTIVATION_VALUE = 1.8

export default class FormDialog extends React.Component {
  state = {
    open: false,
    base_activation_decay: -0.5,
    fraction_of_activation: 0.6,
    initial_activation_value: 1,
    noise: 0.1,
    dynamic_firing_threshold: true,
    firing_threshold:0.01667,
    noise_on: false,
    spread_full_activation:false,
    use_only_complete_fragments:false
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
              label="Base activation decay (should be in between (-1,0)"
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
              label="Fraction of activation (should be in between (0,1)"
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
              label="Initial activation value Should be a positive value (tested in range 0.1 to 10)"
              fullWidth
            />
            <FormControlLabel
            control={
              <Switch
              label="noise_on"
              ref="noise_on"
              checked={this.state.noise_on}
              onChange={this.handleChange('noise_on')}
              value="Noise enabled or disabled"
              color="primary"
            />
            }
            label="Noise enabled or disabled"
            />
            <TextField
              autoFocus
              margin="dense"
              name="noise"
              ref="noise"
              disabled = {(this.state.noise_on)? "" : "disabled"}
              value={this.state.noise}
              id="name"
              onChange={this.onChange}
              label="Noise disturb values"
              fullWidth
            />
           <FormControlLabel
            control={
              <Switch
              checked={this.state.dynamic_firing_threshold}
              onChange={this.handleChange('dynamic_firing_threshold')}
              color="primary"
            />
            }
            label="Dynamic firing threshold or fix"
            />
                        <TextField
              autoFocus
              margin="dense"
              name="firing_threshold"
              ref="firing_threshold"
              disabled = {(this.state.dynamic_firing_threshold)? "" : "disabled"}
              value={this.state.firing_threshold}
              id="name"
              onChange={this.onChange}
              label="Fix firing threshold"
              fullWidth
            />
            <FormControlLabel
            control={
              <Switch
              checked={this.state.spread_full_activation}
              onChange={this.handleChange('spread_full_activation')}
              color="primary"
            />
            }
            label="Enable if the full initial activation value should be spread to its childs"
            />
             <FormControlLabel
            control={
              <Switch
              checked={this.state.use_only_complete_fragments}
              onChange={this.handleChange('use_only_complete_fragments')}
              value="Enable if you only want complete fragments to receive"
              color="primary"
            />
            }
            label="Enable if you only want complete fragments to receive"
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
        ],
        'base_activation_decay':this.state.base_activation_decay,
        'fraction_of_activation':this.state.fraction_of_activation,
        'initial_activation_value':this.state.initial_activation_value,
        'noise':this.state.noise,
        'dynamic_firing_threshold':this.state.dynamic_firing_threshold,
        'firing_threshold':this.state.firing_threshold,
        'noise_on':this.state.noise_on,
        'spread_full_activation':this.state.spread_full_activation,
        'use_only_complete_fragments':this.state.use_only_complete_fragments
      })
    })
      .then((response) => response.json())
      .then((data) => this.props.setSMMs(data));
  }

  handleChange = name => event => {
    this.setState({ [name]: event.target.checked });
  };

  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }
}
