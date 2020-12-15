import React from 'react';
import { List, ListItem, ListItemText } from '@material-ui/core';

export default class Result extends React.Component {
  render() {
    return (
      <div>
        <List component='nav'>
          <ListItem button alignItems='flex-start'>
            <ListItemText
              primary={this.props.business.name}
              secondary={
                <>
                  {/* Rating: {this.props.business.rating}&emsp; */}
                  Categories: {this.props.business.categories}
                </>
              }
            />
            {/* <ListItemText primary={this.props.business.rating} /> */}
            {/* <ListItemText primary={this.props.business.hours} /> */}
            {/* <ListItemText primary={this.props.business.categories} /> */}
          </ListItem>
        </List>
      </div>
    );
  }
}
