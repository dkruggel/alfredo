import React from 'react';
import { List, ListItem, ListItemText } from '@material-ui/core';

export default class Result extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <List component='nav'>
          <ListItem button>
            <ListItemText primary={this.props.business.name} />
            <ListItemText primary={this.props.business.city} />
            <ListItemText primary={this.props.business.state} />
            <ListItemText primary={this.props.business.rating} />
          </ListItem>
        </List>
      </div>
    );
  }
}
